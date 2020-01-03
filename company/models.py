from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from users.models import CustomUser

# Create your models here.
class Company(CustomUser):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50, blank=True)

class Program(models.Model):
    company    = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True)

    scope      = ArrayField(models.URLField(max_length=50))
    baseBounty = models.IntegerField(null=True)
    notice     = models.CharField(max_length=250, null=True)

    abi        = JSONField()
    address    = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.company.user.username
        

# class Contract(models.Model):
#     program = models.ForeignKey(Program, on_delete=models.CASCADE, blank=True)
#     abi     = JSONField(null=True)
