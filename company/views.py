from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth import login, get_user_model
from django.http import HttpResponse
from django_tables2 import SingleTableView

import time

from .models import Company, Program
from .forms import CompanyCreationForm, ProgramCreationForm
from contracts.contracts import Contract, CompanyInterface
from .tables import SubmissionTable, ProgramTable
from submission.models import Submission

# Create your views here.
class CompanySignUpView(CreateView):
    model         = Company
    form_class    = CompanyCreationForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'company'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(index)


class ProgramCreationView(CreateView):
    model         = Program
    form_class    = ProgramCreationForm
    template_name = 'create_program_form.html'

    def form_valid(self, form):
        program_data = form.cleaned_data

        new_contract = Contract(self.request.user.address)

        new_contract.construct(program_data['baseBounty'], ",".join(program_data['scope']), program_data['notice'])
        estimate_gas = new_contract.eth_contract.estimateGas()

        self.request.session['program_data'] = program_data

        return render(self.request, "review_program.html", {"program": program_data, "gas": estimate_gas})


def DeployProgramView(request):
    program_data = request.session['program_data']
    company = Company.objects.get(username=request.user.username)

    new_contract = Contract(company.address)
    
    constructed  = new_contract.construct(program_data['baseBounty'], ",".join(program_data['scope']), program_data['notice'])
    constractAddress = new_contract.deploy()

    program_form = ProgramCreationForm(program_data)
    program = program_form.save(company, new_contract.abi, constractAddress)
    program.save()

    ct = CompanyInterface(request.user.address)
    ct.topUpContract(constractAddress, 20000000000)

    return redirect('my_programs')


# def MyProgramView(request):
#     company = Company.objects.get(username=request.user.username)
#     program = Program.objects.get(company=company)

#     return render(request, "detail_program.html", {"program": program})


class MyProgramsView(SingleTableView):
    model = Program
    paginate_by = 5
    table_class = ProgramTable
    template_name = "my_programs.html"

    def get_queryset(self):
        company = Company.objects.get(username=self.request.user.username)
        programs = Program.objects.filter(company=company)

        return programs


class ProgramDetailView(SingleTableView):
    model = Submission
    # context_object_name = "program"
    table_class = SubmissionTable
    template_name = "detail_program.html"

    def get_context_data(self, **kwargs):
        context = super(ProgramDetailView, self).get_context_data(**kwargs)
        table = SubmissionTable(Submission.objects.filter(program__address=self.kwargs['addr']))
        if Submission.objects.filter(program__address=self.kwargs['addr'], resolved=False).exists():
            context['processing'] = True
        else:
            context['processing'] = False
        context['table'] = table
        context['program_address'] = self.kwargs['addr']
        return context


def RewardBountyView(request, addr, submissionId):
    if request.method == "POST":
        bounty = int(request.POST.get('bounty'))
        comment = request.POST.get('reason')
        if comment is None:
            comment = ''
        submission = Submission.objects.get(program__address=addr, submissionId=submissionId)
        program = submission.program
        contract = CompanyInterface(request.user.address)
        contract.rewardBounty(bounty, comment, program.address, program.abi)

        submission.resolved = True
        submission.bounty = bounty
        submission.save()

        return redirect('my_programs')


def RejectSubmissionView(request, addr, submissionId):
    if request.method == "POST":
        comment = request.POST.get('reason')
        if comment is None:
            comment = ''
        submission = Submission.objects.get(program__address=addr, submissionId=submissionId)
        program = submission.program
        contract = CompanyInterface(request.user.address)
        contract.rejectSubmission(comment, program.address, program.abi)

        submission.resolved = True
        submission.save()

        return redirect('my_programs')


def index(request):
    return redirect('my_programs')