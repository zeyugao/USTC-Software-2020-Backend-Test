from django import forms
from .models import  Student, Course

# learn this method form igem_2019_be_test_pr_lbc

class RegistrationForm(forms.Form):
    """
        Registration needs a format to strict: username, password, profile.
    """
    stu_name = forms.CharField(label='用户名', max_length=100, required='用户名不为空')
    stu_password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(render_value=True), required='密码不少于6位')
    stu_password_re = forms.CharField(label='确认密码', min_length=6, widget=forms.PasswordInput(render_value=True), required='确认密码不少于6位')
    stu_grade = forms.IntegerField(label='年级', max_value=4, min_value=1,)
    # Use clean methods to restrict input values

    def clean_stu_name(self):
        """
            Stu_name must be longer than 3 words and shorter than 20 words, no format restriction.
        """
        stu_name = self.cleaned_data.get('stu_name')
        if len(stu_name) < 3:
            raise forms.ValidationError("001,Your username must be longer than 3 words.")
        elif len(stu_name) > 20:
            raise forms.ValidationError("002,Your username must be shorter than 20 words.")
        else:

            # To check whether the username already exists

            checkresult = Student.objects.filter(stu_name=stu_name)
            if len(checkresult) > 0:  # >0数据库中已经存在
                raise forms.ValidationError("003,Your username already exists.")
        return stu_name

    def clean_stu_password(self):
        """
            Password must be longer than 6 words and must contain numbers.
        """
        password = self.cleaned_data.get('stu_password')
        if len(password) < 6:
            raise forms.ValidationError("004,Your password must be longer than 6 words.")
        else:
            password_c = list(password)
            flag = 0
            for c in password_c:
                if ord(c) > 47 and ord(c) < 58:
                    flag = 1
                    break
            if flag == 1:
                return password
            else:
                raise forms.ValidationError("005,Your password must contain numbers.")

    def clean_password_re(self):
        password = self.cleaned_data.get('stu_password')
        password_re = self.cleaned_data.get('stu_password_re')
        if password_re != password:
            raise forms.ValidationError("006,Two passwords mismatch. Please try again.")
        else:
            return password_re


class LoginForm(forms.Form):
    """
        Registration needs a format to strict: username, password, profile.
    """
    stu_name = forms.CharField(label='用户名', max_length=100, required='用户名不为空')
    stu_password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(render_value=True), required='密码不少于6位')


    def clean_stu_name(self):
        """
            Stu_name must be longer than 3 words and shorter than 20 words, no format restriction.
        """
        stu_name = self.cleaned_data.get('stu_name')
        if len(stu_name) < 2:
            raise forms.ValidationError("001,Your username must be longer than 2words.")
        elif len(stu_name) > 20:
            raise forms.ValidationError("002,Your username must be shorter than 20 words.")
        else:

            # To check whether the username already exists

            checkresult = Student.objects.filter(stu_name=stu_name)
            if not checkresult:
                raise forms.ValidationError("007,Your account doesn't exist.")
        return stu_name

    def clean_stu_password(self):
        """
            Password must be longer than 6 words and must contain numbers.
        """
        password = self.cleaned_data.get('stu_password')
        if len(password) < 6:
            raise forms.ValidationError("004,Your password must be longer than 6 words.")
        else:
            password_c = list(password)
            flag = 0
            for c in password_c:
                if ord(c) > 47 and ord(c) < 58:
                    flag = 1
                    break
            if flag == 1:
                return password
            else:
                raise forms.ValidationError("005,Your password must contain numbers.")

