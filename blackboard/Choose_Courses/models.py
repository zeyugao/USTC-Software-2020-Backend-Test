from django.db import models

# Create your models here.

class Category(models.Model):
    #以年级为依据对博客分类
    name = models.CharField("年级", max_length=50)
    class Meta:
        verbose_name = "年级"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
    
class Course(models.Model):
    #课程信息
    name = models.CharField("课程名称", max_length=50)
    teacher = models.CharField("授课教师", max_length=50)
    content = models.TextField("课程内容")
    category = models.ForeignKey(Category, verbose_name="年级", on_delete=models.CASCADE)
    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class User(models.Model):
    #用户信息
    name = models.CharField("姓名", max_length=50)
    password = models.CharField("密码", max_length=50)
    created_time = models.DateTimeField(auto_now_add=True)
    courses = models.ManyToManyField("Course")  #学生与课程多对多
    
    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name