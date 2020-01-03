from django.urls import path

from company.views import CompanySignUpView
from expert.views import ExpertSignUpView
from hacker.views import HackerSignUpView

from . import views

urlpatterns = [
    path('login_success', views.LoginSuccess, name='login_success'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('signup/company/', CompanySignUpView.as_view(), name='company_signup'),
    path('signup/expert/', ExpertSignUpView.as_view(), name='expert_signup'),
    path('signup/hacker/', HackerSignUpView.as_view(), name='hacker_signup'),
]