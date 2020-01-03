from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.contrib.auth import login
from django.http import HttpResponse
from django_tables2 import SingleTableView, RequestConfig

from .models import Hacker
from .forms import HackerCreationForm, SubmitBugForm
from .tables import ProgramListTable, ProgramDetailTable, MySubmissionsTable
from company.models import Program
from submission.models import Submission
from contracts.contracts import HackerInterface

# Create your views here.
class HackerSignUpView(CreateView):
    model = Hacker
    form_class = HackerCreationForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'hacker'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(index)


class ProgramListView(SingleTableView):
    model = Program
    # context_object_name = "program"
    table_class = ProgramListTable
    template_name = "all_programs.html"
    # ordering = ['id']

    # def get_context_data(self, **kwargs):
    #     context = super(ProgramListView, self).get_context_data(**kwargs)
    #     context['nav_customer'] = True
    #     table = ProgramListTable(Program.objects.all())
    #     table.render_status()
    #     RequestConfig(self.request, paginate={'per_page': 5}).configure(table)
    #     context['table'] = table
    #     return context


class ProgramDetail(SingleTableView):
    model = Program
    # context_object_name = "program"
    table_class = ProgramDetailTable
    template_name = "program_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProgramDetail, self).get_context_data(**kwargs)
        table = ProgramDetailTable(Program.objects.filter(address=self.kwargs['addr']))
        context['table'] = table
        context['address'] = self.kwargs['addr']
        return context


class MySubmissionsView(SingleTableView):
    model = Submission
    # context_object_name = "program"
    table_class = MySubmissionsTable
    template_name = "my_submissions.html"

    def get_context_data(self, **kwargs):
        context = super(MySubmissionsView, self).get_context_data(**kwargs)
        table = MySubmissionsTable(Submission.objects.filter(hacker=self.request.user))
        context['table'] = table
        # context['address'] = self.kwargs['addr']
        return context


class SubmitBugView(CreateView):
    model = Submission
    form_class = SubmitBugForm
    template_name = 'submit_bug.html'

    def form_valid(self, form):
        program = Program.objects.get(address=self.kwargs['addr'])
        hacker = Hacker.objects.get(username=self.request.user.username)
        form_data = form.cleaned_data
        
        caller = HackerInterface(self.request.user.address)
        submissionId = caller.submitBug(form_data['name'], form_data['severity'], program.address, program.abi)
        form.save(submissionId, program, hacker)
        return redirect('submission_detail', submissionId=submissionId,addr=program.address)


def index(request):
    return redirect('all_programs')