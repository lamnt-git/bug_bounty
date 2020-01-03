from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_program', login_required(views.ProgramCreationView.as_view()), name='create_program'),
    path('deploy_program', login_required(views.DeployProgramView), name='deploy_program'),
    path('my_programs', login_required(views.MyProgramsView.as_view()), name='my_programs'),
    path('program_detail/<str:addr>', login_required(views.ProgramDetailView.as_view()), name='company_program_detail')
]