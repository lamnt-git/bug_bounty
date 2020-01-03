from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction

from .models import Expert

class ExpertCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Expert
        fields = ('email', 'username', 'address')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = "EXPERT"
        user.save()
        return user

class ExpertChangeForm(UserChangeForm):

    class Meta:
        model = Expert
        fields = ('email', 'username',)