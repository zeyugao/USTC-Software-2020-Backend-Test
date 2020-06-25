from django import forms
from .models import User, Course

"""
一些接受数据的表单，对应不同的视图。表单给出了对应视图需要用户提交的变量
"""


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'gender', 'grade', 'username', 'email', 'password')


class UserForm(forms.Form):
    username = forms.CharField(label='username', max_length=128, widget=forms.TextInput)
    password = forms.CharField(label='password', max_length=256, widget=forms.PasswordInput)


class SelectForm(forms.Form):
    course_id = forms.UUIDField()


class DelCourseForm(forms.Form):
    course_id = forms.UUIDField()
