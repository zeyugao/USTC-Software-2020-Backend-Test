from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.serializers.json import json
from django import forms
from django.urls import reverse
from django.views.generic.base import View

def index(request):
    '''
    获得所有的课程, 课程名：教师
    code<int>: 返回代码
    可能值及其含义
    | 返回值 | 含义              |
    | ------ | ----------------|
    | 200    | 列出课程成功      |
    | 301    | 未登录           |
    message<str>:  返回代码相应的解释或展示的文本
    '''
    #未登录重定向至login
    if not request.session.get('is_login', None):
        message = '只有登陆后才能查看主页信息'
        return render(request, 'Choose_Courses/login.html',
                     {'code': 301,
                      'message': message})
    #列出所有课程
    courses = Course.objects.all()
    output = {}
    for course in courses:
        output[course.name] = course.id
    return render(request, 'Choose_Courses/index.html',
                 {'code': 200,
                  'message': 'list all courses successfully',
                  'output':output}
                 )
    
        
def get_details(request, course_id):
    '''
    根据course_id列出课程详细内容
    code<int>: 返回代码
    可能值及其含义
    | 返回值 | 含义             |
    | ------ | ---------------- |
    | 200    | 列出成功         |
    | 301    | 未登录           |
    | 311    | 对应pk的课程不存在 |
    message<str>:  返回代码相应的解释或展示的文本
    '''
    #未登录重定向至login
    if not request.session.get('is_login', None):
        message = '你还没有登录'
        return render(request, 'Choose_Courses/login.html',
                     {'code': 301,
                      'message': message})
    #尝试获取课程
    try:
        course = Course.objects.get(pk=course_id)
    except (KeyError, Course.DoesNotExist):
        return JsonResponse({
            'code': 311,
            'message':'course does not exist'
        })
    #列出课程详细信息
    output = {
            '课程编号': course.id,
            '课程名称': course.name,
            '授课教师': course.teacher,
            '课程内容': course.content,
        }
    return JsonResponse({
        'code': 200,
        'message':output
        }, json_dumps_params={'ensure_ascii': False})

def choose(request, course_id):
    '''
    用户根据course_id(pk)选课
    code<int>: 返回代码
    可能值及其含义
    | 返回值 | 含义             |
    | ------ | ---------------- |
    | 200    | 选课成功         |
    | 301    | 未登录           |
    | 310    | 对应pk课程已选中   |
    | 311    | 对应pk的课程不存在 |
    message<str>:  返回代码相应的解释或展示的文本
    '''
    #未登录重定向至login
    if not request.session.get('is_login', None):
        message = '你还没有登录'
        return render(request, 'Choose_Courses/login.html',
                     {'code': 301,
                      'message': message})
    #尝试获取课程
    try:
        course = Course.objects.get(pk=course_id)
    except (KeyError, Course.DoesNotExist):
        return JsonResponse({
            'code': 311,
            'message':'course does not exist'
        })
    #选课
    if (request.method == 'GET'):  #POST？
        user_name = request.session['user_name']
        user = User.objects.get(name=user_name)
        #如果已经选中课程
        if (course in user.courses.all()):
            message = '你已经选中了这门课！'
            return render(request, 'Choose_Courses/choose.html',
                     {'code': 310,
                      'message': message})
        #选课
        user.courses.add(course)
        message = '选课成功'
        return render(request, 'Choose_Courses/choose.html',
                     {'code': 200,
                      'message': message})

def cancel(request, course_id):
    '''
    用户根据course_id(pk)退课
    code<int>: 返回代码
    可能值及其含义
    | 返回值 | 含义             |
    | ------ | ---------------- |
    | 200    | 退课成功         |
    | 301    | 未登录           |
    | 311    | 对应pk的课程不存在 |
    | 312    | 对应pk课程还没选中  |
    message<str>:  返回代码相应的解释或展示的文本
    '''
    #未登录重定向至login
    if not request.session.get('is_login', None):
        message = '你还没有登录'
        return render(request, 'Choose_Courses/login.html',
                     {'code': 301,
                      'message': message})
    #尝试获取课程
    try:
        course = Course.objects.get(pk=course_id)
    except (KeyError, Course.DoesNotExist):
        return JsonResponse({
            'code': 311,
            'message':'course does not exist'
        })
    #退课
    if (request.method == 'GET'):   #POST ？
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)
        #如果用户退的课还没有被用户选中
        if (course not in user.courses.all()):
            message = '你还没有选这门课'
            return JsonResponse({
            'code': 312,
            'message':message
        }, json_dumps_params={'ensure_ascii': False})
        #退课
        user.courses.remove(course)
        message = "退课成功"
        return JsonResponse({
            'code': 200,
            'message':message
        }, json_dumps_params={'ensure_ascii': False})

def show(request):
    '''
    展示用户选择的所有课程
    code<int>: 返回代码
    可能值及其含义
    | 返回值 | 含义             |
    | ------ | ---------------- |
    | 200    | 展示成功         |
    | 301    | 未登录           |
    | 313    | 用户没有任何选课   |
    message<str>:  返回代码相应的解释或展示的文本
    '''
    #未登录重定向至login
    if not request.session.get('is_login', None):
        message = '你还没有登录'
        return render(request, 'Choose_Courses/login.html',
                     {'code': 301,
                      'message': message})
    user_id = request.session['user_id']
    user = User.objects.get(pk=user_id)
    chosen_courses = user.courses.all()
    if not chosen_courses:
        message = "你还没有选中的课"
        return JsonResponse({
            'code': 313,
            'message':message
        }, json_dumps_params={'ensure_ascii': False})
    output = {}
    for course in chosen_courses:
        detail = {}
        detail['授课教师'] = course.teacher
        detail['课程内容'] = course.content
        output[course.name] = detail
    message = '展示成功'
    return render(request, 'Choose_Courses/show.html',
                     {'code': 200,
                      'message': message,
                      'output':output})


'''
以下为注册，登录，登出系统
策略：
    未登录-->全部跳转login
    已登录-->访问login自动跳转index
    登出-->自动跳转到login
'''
class RegisterView(View):
    '''
    返回用户注册页面
    '''
    def get(self, request):
        return render(request, 'Choose_Courses/register.html')
        
    def post(self, request):
        '''
        处理用户注册请求，/register的post请求
        注册信息符合要求后即添加至系统中

        @param in POST
            username<str>: 请求处理的用户名
            password1<str>: 请求处理的密码1
            password2<str>: 请求处理的密码2
        
        @return in JSON
            code<int>: 返回代码
                       可能值及其含义
                       |返回值|     含义     |
                       |-----|-------------|
                       |200  |注册成功       |
                       |410  |用户名不符合要求|
                       |420  |密码不符合要求  |  
            message<dict>: 返回代码相应解释
        '''
        #获取用户名和密码，需要输入两次密码
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        #判断用户名是否合法
        if not username.strip(): 
            return JsonResponse({
                'code': 410,
                'message':'Username invalid'
            })
        if User.objects.filter(name=username).exists():
            return JsonResponse({
                'code': 410,
                'message':'Username already exist'
            })
        #判断密码是否相同
        if password1 != password2:
            return JsonResponse({
                'code': 420,
                'message':'Two passwords are not same'
            })
        #创建新用户
        new_user = User()
        new_user.name = username
        new_user.password = password1
        new_user.save()
        return render(request, 'Choose_Courses/login.html',
                     {'message': 'register successfully'})
    
class LoginView(View):
    '''
    返回用户登录时的界面以及处理用户提交的登录请求
    '''
    def get(self, request):
        #如果已经登录，就重定向到index
        if request.session.get('is_login', None):
            return render(request, 'Choose_Course/index.html')
        return render(request, 'Choose_Courses/login.html')

    def post(self, request):
        '''
        处理用户登录请求，/login的post请求
        登录信息正确后可登录，并重定向至/index

        @param in POST
            username<str>: 请求处理的用户名
            password<str>: 请求处理的密码
        
        @return in JSON
            code<int>: 返回代码
                       可能值及其含义
                       |返回值|     含义       |
                       |-----|---------------|
                       |200  |登录成功        |
                       |411  |用户名不存在     |
                       |400  |用户名与密码不匹配|  
            message<dict>: 返回代码相应解释
        '''
        #获取用户输入的用户名和密码
        username = request.POST.get('username')
        password = request.POST.get('password')
        #判断用户名是否存在
        try:
            user = User.objects.get(name=username)
        except User.DoesNotExist:
            return JsonResponse({
                'code': 410,
                'message': 'username does not exist'
            })
        #验证用户名和密码是否匹配
        if user.password != password:
            return JsonResponse({
                'code': 400,
                'message': 'Username or password is not correct'
            })
        #进行登录
        request.session['is_login'] = True
        request.session['user_id'] = user.id
        request.session['user_name'] = user.name
        return render(request, 'Choose_Courses/choose.html',
                     {'code': 200,
                      'message': 'login successfully'})

def logout(request):
    '''
    处理用户的登出请求
    如果没有登录则直接重定向到index
    否则登出后再重定向至login
    code<int>: 返回代码
    可能值及其含义
    | 返回值 | 含义             |
    | ------ | ---------------- |
    | 201    | 登出成功         |
    | 301    | 未登录           |
    message<str>:  返回代码相应的解释或展示的文本
    '''
    #如果没有登录
    if not request.session.get('is_login'): 
        return render(request, 'Choose_Courses/index.html',
                     {'code': 301,
                      'message': 'login successfully'})
    #删除会话
    request.session.flush()  
    return render(request, 'Choose_Courses/choose.html',
                 {'code': 201,
                  'message': 'logout successfully'})

    