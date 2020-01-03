from django.db import models
from users.models import CustomUser
from company.models import Program

# Create your models here.
class Hacker(CustomUser):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
