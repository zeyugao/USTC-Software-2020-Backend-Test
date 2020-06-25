from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

"""
两个模型：用户User和课程Course,年级作为User的一个属性.
"""


class User(AbstractUser):
    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=10, choices=(('M', 'Man'), ('F', 'Woman')))
    grade = models.IntegerField(choices=((1, 'freshman'), (2, 'sophomore'), (3, 'junior'), (4, 'senior')))

    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'


class Course(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100, unique=True)
    course_id = models.UUIDField(primary_key=True)
    learning_students = models.ManyToManyField(settings.AUTH_USER_MODEL)
