from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django.db import transaction

from .models import Hacker
from submission.models import Submission, Comment

class HackerCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Hacker
        fields = ('email', 'username', 'address')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = "HACKER"
        user.save()
        return user
        
class HackerChangeForm(UserChangeForm):

    class Meta:
        model = Hacker
        fields = ('email', 'username',)

class SubmitBugForm(ModelForm):

    class Meta:
        model = Submission
        fields = ['name', 'poc', 'severity']

    @transaction.atomic
    def save(self, _submissionId, _program, _hacker):
        submission = super().save(commit=False)
        submission.submissionId = _submissionId
        submission.hacker = _hacker
        submission.program = _program
        submission.save()
        return submission
