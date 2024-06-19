from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass 

class Usage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usage")
    cause = models.TextField(max_length=64)
    cost = models.FloatField()
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()