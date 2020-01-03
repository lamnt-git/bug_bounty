from django.contrib import admin
from .models import Submission, Comment

# Register your models here.
admin.site.register(Submission)
admin.site.register(Comment)