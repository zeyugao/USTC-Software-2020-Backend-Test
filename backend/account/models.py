from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class student(AbstractUser):
    grade=models.IntegerField()

    def __str__(self):
        return None