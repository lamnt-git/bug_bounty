from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('all_programs', login_required(views.ProgramListView.as_view()), name='all_programs'),
    path('program_detail/<str:addr>', login_required(views.ProgramDetail.as_view()), name='hacker_program_detail'),
    path('submit_bug/<str:addr>', login_required(views.SubmitBugView.as_view()), name='submit_bug'),
    path('my_submissions', login_required(views.MySubmissionsView.as_view()), name='my_submissions')
]