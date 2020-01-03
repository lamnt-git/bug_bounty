from django.shortcuts import redirect
from django.views.generic import TemplateView

import company.views
import expert.views
import hacker.views

class SignUp(TemplateView):
    template_name = 'registration/signup.html'

def LoginSuccess(request):
    if request.user.user_type == "COMPANY":
        return redirect(company.views.index)
    elif request.user.user_type == "EXPERT":
        return redirect(expert.views.index)
    else:
        return redirect(hacker.views.index)