from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import login
from django.http import HttpResponse

from .models import Expert
from .forms import ExpertCreationForm

# Create your views here.
class ExpertSignUpView(CreateView):
    model = Expert
    form_class = ExpertCreationForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'expert'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(index)


def index(request):
    return HttpResponse("Expert index")