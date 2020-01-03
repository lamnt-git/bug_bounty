from django.db import models
from company.models import Program
from hacker.models import Hacker
from users.models import CustomUser
from django.utils import timezone

# Create your models here.
class Submission(models.Model):
    submissionId = models.IntegerField(blank=True)
    hacker = models.ForeignKey(Hacker, on_delete=models.CASCADE, blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=50, blank=True)
    poc = models.CharField(max_length=200, blank=True)
    severity = models.CharField(max_length=10, blank=True)
    resolved = models.BooleanField(default=False)
    bounty = models.BigIntegerField(default=0)

    def __str__(self):
        return self.name

class Comment(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, blank=True, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text