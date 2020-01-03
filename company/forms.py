from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction
from django.utils.text import slugify

from .models import Company, Program

import hashlib

class CompanyCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Company
        fields = ('email', 'username', 'name', 'address')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = "COMPANY"
        user.save()
        return user

class CompanyChangeForm(UserChangeForm):

    class Meta:
        model = Company
        fields = ['email', 'username']

class ProgramCreationForm(ModelForm):

    class Meta:
        model = Program
        fields = ['scope', 'baseBounty', 'notice']

    @transaction.atomic
    def save(self, _company, _abi, _constractAddress):
        program         = super().save(commit=False)
        program.company = _company
        program.abi     = _abi
        program.address = _constractAddress
        
        program.save()
        return program
