# Create your models here.
from django.db import models


class Course(models.Model):
    course_name = models.CharField(max_length=30, unique=True)
    course_grade = models.IntegerField(blank=False)

    class Meta:
        db_table = 't_course'

    def __str__(self):
        return 'Course:%s' % self.course_name

# 学生类
class Student(models.Model):
   # stu_email = models.EmailField(unique=True)
    stu_name = models.CharField(max_length=30, unique=True)
    stu_password = models.CharField(max_length=30)
    stu_grade = models.IntegerField()
    courses = models.ManyToManyField(Course, blank=True)

    class Meta:
        db_table = 't_student'

    def __str__(self):
        return 'Student:%s' % self.stu_name

