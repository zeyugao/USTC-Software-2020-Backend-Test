from . import models, forms
from django import forms
from django.db import models
from django.contrib.auth import logout, authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .forms import UserForm, RegisterForm, SelectForm, DelCourseForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.http.response import JsonResponse


def index(request):
    """
    处理用户对于```/index```的请求
    将未登录的用户定向到首页

    @return in JSON
        code<int>: 返回代码
                   可能值及其含义
                   | 返回值 | 含义             |
                   | ------ | ---------------- |
                   | 200    | 未登录，定向到首页   |
                   | 100    | 用户已登录         |
        msg<dict>:  返回代码相应的解释
        :param request:
    """

    if request.session.get('is_login', None):
        message = 'you have already logged in.'
        return JsonResponse({
            'code': 100,
            'msg': message
        })
    return JsonResponse({
            'code': 200,
            'msg': 'Hello, please login.'
        })


class LoginView(View):
    """
    处理用户对于```/login```的post请求
    处理用户提交的登录信息，若用户名和密码符合要求，用户登录

    @param in POST
        username<str>:  用户名
        password<str>:  密码

    @return in JSON
        code<int>: 返回代码
                   可能值及其含义
                   | 返回值 | 含义             |
                   | ------ | ---------------- |
                   | 200    | 登录成功         |
                   | 410    | 提交格式不符合要求 |
                   | 400    | 未查找到该用户    |
        msg<dict>:  返回代码相应的解释
    """
    http_method_names = ['post', 'get']

    def get(self, request):
        pass

    def post(self, request):
        if request.user.is_authenticated():
            message = 'you have already logged in!'
            return JsonResponse({
                'code': 100,
                'msg': message
            })

        login_form = UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                return JsonResponse({
                    'code': 200,
                    'msg': 'log in successfully!'
                })
            else:
                return JsonResponse({
                    'code': 400,
                    'msg': 'nonexistent account!'
                })
        else:
            return JsonResponse({
                'code': 410,
                'msg': ValidationError.messages
            })


class LogoutView(View):
    """
    处理用户对于```/logout```的get请求
    处理用户退出请求，若用户已登录，将用户登出

    @return in JSON
        code<int>: 返回代码
                   可能值及其含义
                   | 返回值 | 含义             |
                   | ------ | ----------------|
                   | 200    | 登出成功         |
        msg<dict>:  返回代码相应的解释
    """
    http_method_names = ['get']

    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return JsonResponse({
            'code': 200,
            'msg': 'logout successfully'
        })


class RegisterView(View):
    """
    处理用户对于```/register```的post请求
    处理用户注册提交的注册信息，若用户名和密码符合要求，将用户添加至系统中

    @param in POST
        username<str>:  请求注册的用户名
        password<str>:  相应的密码
        name<str>:  学生真实姓名
        gender<str>:  学生性别 choices=(('M', 'Man'), ('F', 'Woman'))
        grade<int>:  学生年级 choices=((1, 'freshman'), (2, 'sophomore'), (3, 'junior'), (4, 'senior'))
        email<str>:  学生邮箱

    @return in JSON
        code<int>: 返回代码
                   可能值及其含义
                   | 返回值 | 含义             |
                   | ------ | ---------------- |
                   | 200    | 注册成功             |
                   | 100    | 用户已登录，请登出后注册|
                   | 410    | 输入格式不符合要求     |
                   | 420    | 该邮箱已被注册        |
        msg<dict>:  返回代码相应的解释
    """
    http_method_names = ['get', 'post']

    def get(self, request):
        pass

    def post(self, request):
        if request.user.is_authenticated():
            message = 'you have already logged in!'
            return JsonResponse({
                'code': 100,
                'msg': message
            })

        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            same_email_user = models.User.objects.filter(email=register_form.cleaned_data['email'])
            if same_email_user:
                message = 'The email has been registered, please try another one'
                return JsonResponse({
                    'code': 420,
                    'msg': message
                })
            else:
                User.objects.create_user(
                    name=register_form.cleaned_data['name'],
                    gender=register_form.cleaned_data['gender'],
                    grade=register_form.cleaned_data['grade'],
                    username=register_form.cleaned_data['username'],
                    email=register_form.cleaned_data['email'],
                    password=register_form.cleaned_data['password']
                )
                return JsonResponse({
                    'code': 200,
                    'msg': 'register successfully!'
                })
        else:
            return JsonResponse({
                'code': 410,
                'msg': ValidationError.messages
            })


class AccountView(View):
    """
    处理用户对于```/account```的get请求
    列出用户已选课程以及个人信息

    @return in JSON
        code<int>: 返回代码
                   可能值及其含义
                   | 返回值 | 含义             |
                   | ------ | ---------------- |
                   | 200    | 导出成功           |
        msg<dict>:  返回代码相应的解释
    """
    http_method_names = ['get']

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        return JsonResponse({
            'code': 200,
            'username': user.username,
            'name': user.name,
            'grade': user.grade,
            'gender': user.gender,
            'email': user.email,
            'selected_course_list': user.course.all()
        })


class SelectView(View):
    """
    处理用户对于```/select```的get 或 post请求
    get：列出所有课程
    post：处理用户选课请求，进行选课

    @param in POST
        course_id<str>:  待选课程的course_id

    @return in JSON
        code<int>: 返回代码
                   可能值及其含义
                   | 返回值 | 含义             |
                   | ------ | ---------------- |
                   | 200    | 选课/列课成功         |
                   | 410    | 输入格式不符合要求     |
                   | 420    | 该学生已选上该课程     |
        msg<dict>:  返回代码相应的解释
    """
    http_method_names = ['get', 'post']

    @method_decorator(login_required)
    def get(self, request):
        return JsonResponse({
            'code': 200,
            'course_list': models.Course.objects.all()
        })

    @method_decorator(login_required)
    def post(self, request):
        select_form = forms.SelectForm(request.POST)
        if select_form.is_valid():
            course_id = select_form.cleaned_data['course_id']
            course = models.Course.objects.filter(course_id=course_id)
            user = request.user
            have_selected = user.course.filter(course_id=course_id)
            if have_selected:
                message = 'you have selected this course, please try another one'
                return JsonResponse({
                    'code': 420,
                    'msg': message
                })
            else:
                course.learning_students.add(user)
                return JsonResponse({
                    'code': 200,
                    'msg': 'select successfully!'
                })
        else:
            return JsonResponse({
                'code': 410,
                'msg': ValidationError.messages
            })


class DelCourseView(View):
    """
    处理用户对于```/delete```的get 或 post请求
    get：列出所有已选课程
    post：处理用户退课请求

    @param in POST
        course_id<str>:  待退课程的course_id

    @return in JSON
        code<int>: 返回代码
                   可能值及其含义
                   | 返回值 | 含义             |
                   | ------ | ---------------- |
                   | 200    | 退课/列课成功         |
                   | 410    | 输入格式不符合要求     |
                   | 420    | 该学生还未选该课程     |
        msg<dict>:  返回代码相应的解释
    """
    http_method_names = ['get', 'post']

    @method_decorator(login_required)
    def get(self, request):
        return JsonResponse({
            'code': 200,
            'course_list': request.user.course.all()
        })

    @method_decorator(login_required)
    def post(self, request):
        del_course_form = forms.DelCourseForm(request.POST)
        if del_course_form.is_valid():
            course_id = del_course_form.cleaned_data['course_id']
            course = models.Course.objects.filter(course_id=course_id)
            user = request.user
            have_selected = user.course.filter(course_id=course_id)
            if have_selected:
                message = 'you have not selected this course yet!'
                return JsonResponse({
                    'code': 420,
                    'msg': message
                })
            else:
                course.learning_students.delete(user)
                return JsonResponse({
                    'code': 200,
                    'msg': 'delete successfully!'
                })
        else:
            return JsonResponse({
                'code': 410,
                'msg': ValidationError.messages
            })
