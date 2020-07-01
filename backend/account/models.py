from django.db import models
from django.contrib.auth.models import AbstractUser

#User
class Account(AbstractUser):
    grade = models.IntegerField()
    