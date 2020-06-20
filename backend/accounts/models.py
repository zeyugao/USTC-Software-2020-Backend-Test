from django.db import models
from django.contrib.auth.models import User


class Stu(models.Model):
    grade = models.PositiveIntegerField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Ke(models.Model):
    name = models.CharField(max_length=256)
    grade = models.PositiveIntegerField(null=True, blank=True)
    stus = models.ManyToManyField(Stu)
