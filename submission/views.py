from django.shortcuts import render
from django.shortcuts import render, redirect
from django_tables2 import SingleTableView

from .models import Submission, Comment
from .tables import SubmissionTable
from .forms import CommentForm

# Create your views here.

class SubmissionView(SingleTableView):
    model = Submission
    table_class = SubmissionTable
    template_name = "submission_detail.html"

    def get_context_data(self, **kwargs):
        context = super(SubmissionView, self).get_context_data(**kwargs)
        submission = Submission.objects.get(program__address=self.kwargs['addr'], submissionId=self.kwargs['submissionId'])
        table = SubmissionTable(Submission.objects.filter(program__address=self.kwargs['addr'], submissionId=self.kwargs['submissionId']))
        if submission.resolved is True:
            context['isResolved'] = True
        
        if self.request.user.user_type == "COMPANY":
            context['isCompany'] = True

        comments = Comment.objects.filter(submission=submission)
        context['comments'] = comments

        context['table'] = table
        context['address'] = self.kwargs['addr']
        return context


def AddCommentView(request, addr, submissionId):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            author = request.user
            submission = Submission.objects.get(program__address=addr, submissionId=submissionId)
            form.save(author, submission)
            back = request.META.get('HTTP_REFERER')
            return redirect(back)
        else:
            return redirect('my_submissions')


def index(request):
    return redirect('my_submissions')