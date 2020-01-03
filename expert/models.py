from django.db import models
from users.models import CustomUser

# Create your models here.
class Expert(CustomUser):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)