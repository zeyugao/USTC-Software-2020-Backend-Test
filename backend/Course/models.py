from django.db import models
from account.models import Account

# Create your models here.
#Course
class Course(models.Model):
    coursename = models.CharField(max_length = 50,null = True,blank = True)
    grade = models.IntegerField()
    #student = models.ManyToManyField(Account,through = 'ACRelationship')

#relationship between Account and Course
class ACRelationship(models.Model):
    course = models.ForeignKey(Course,on_delete = models.CASCADE,related_name='account')
    account = models.ForeignKey(Account,on_delete = models.CASCADE,related_name='course')
    selection = models.BooleanField(default = False)#if student choose the course
    finished = models.BooleanField(default = False)#if student have already finished the course

#relationship between course and Course
class CCRelationship(models.Model):
    course = models.ForeignKey(Course,on_delete = models.CASCADE,related_name='preparatorycourse')
    preparatorycourse = models.ForeignKey(Course,on_delete = models.CASCADE,related_name='course')#peparatory course