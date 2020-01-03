from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=10)
    address = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.email