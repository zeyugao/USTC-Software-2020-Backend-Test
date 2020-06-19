from django.db import models
from django.contrib.auth import get_user_model
userModel=get_user_model()

class course(models.Model):
    name=models.CharField(max_length=30)
    courseID=models.CharField(max_length=30,primary_key=True)
    grade=models.IntegerField()
    
    def __str__(self):
        return self.courseID+" "+self.name

class courseResult(models.Model):
    learner=models.ForeignKey(userModel,on_delete=models.CASCADE,related_name="resultSet")
    result=models.ForeignKey(course,on_delete=models.CASCADE,related_name="learnerSet")
    haveLearnt=models.BooleanField()

class coursePrefix(models.Model):
    prefix=models.ForeignKey(course,on_delete=models.CASCADE,related_name='suffixSet')
    suffix=models.ForeignKey(course,on_delete=models.CASCADE,related_name='prefixSet')

# Create your models here.
