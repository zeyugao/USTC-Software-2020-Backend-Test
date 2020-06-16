from django.db import models
from account.models import Student
# Create your models here.
class Course(models.Model):
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    GRADUATE = 'GR'
    GRADE = [
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
        (GRADUATE, 'Graduate'),
    ]
    grade = models.CharField(max_length = 2, choices = GRADE, default = FRESHMAN)
    name = models.CharField(max_length = 255, null = True)
    description = models.CharField(max_length = 1000, null = True)
    student = models.ManyToManyField(Student)