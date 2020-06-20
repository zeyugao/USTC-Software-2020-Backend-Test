from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'grade', 'password1', 'password2']

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['user']