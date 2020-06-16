from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    course_id = models.CharField(max_length=10, primary_key=True)
    # 如果你想自己指定主键， 在你想要设置为主键的字段上设置参数 primary_key=True。
    # 如果 Django 看到你显式地设置了 Field.primary_key，
    # 将不会自动在表（模型）中添加id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=20)  # 课程名称
    course_student = models.ManyToManyField(User, blank=True)  # 课程学生 与学生类多对多

    def __str__(self):
        return self.course_name
    # __str__方法的作用是让字符串转换函数str（）可以对任何对象进行转换
    # 用于返回一个良好的、人类可读的模型表示
    # 显示出name，记得要改account/admin.py 文件才能在管理页面看到




# Create your models here.
