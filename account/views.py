from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from account import models
from .models import Course
from django.contrib import auth
# Auth模块是Django自带的用户认证模块
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def account_register(request):
    # request这是前端请求发来的请求，携带的所有数据，django给我们做了一些列的处理，封装成一个对象传过来
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        re_pwd = request.POST.get('re_pwd')
        if name and pwd and re_pwd:
            if pwd == re_pwd:
                for x in User.objects.all():
                    if x.username == name:
                    #  循环数据库
                    # 查找用户名是否已存在，这里username是类属性，name是刚刚赋值的用户名
                    # 不能用auth.authenticate(request, username=name)，它还需要password参数
                        return JsonResponse({"key": "401", "msg": "the username exists"})
                User.objects.create_user(username=name, password=pwd)  # 创建普通用户
                return JsonResponse({"key": "402", "msg": "register successfully"})
            else:
                return JsonResponse({"key": "403", "msg": "please input the same password"})

        else:
            return JsonResponse({"key": "404", "msg": "blank input is not allowed"})


def account_login(request):
    # 注意不要和方法login()重名了
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        for x in User.objects.all():
            if x.username == name:
                user_obj2 = auth.authenticate(request, username=name, password=pwd)
                """使用 authenticate() 来验证用户。它使用 username 和 password 作为参数来验证，
                对每个身份验证后端( authentication backend ` )进行检查。
                如果后端验证有效，则返回一个 :class:`~django.contrib.auth.models.User 对象。
                如果后端引发 PermissionDenied 错误，将返回 None。
                """
                if user_obj2:
                    login(request, user_obj2)
                    return JsonResponse({"key": "501", "msg": "login successfully "})
                else:
                    return JsonResponse({"key": "502", "msg": "pwd error"})
        else:
            return JsonResponse({"key": "503", "msg": "username doesn't exist"})


def account_logout(request):
    # 注意，如果用户未登录，logout()不会报错。
    if not request.user.is_authenticated:
        # 判断是否登录
        return JsonResponse({"key": "601", "msg": "please login first"})
    else:
        logout(request)
        return JsonResponse({"key": "602", "msg": "logout successfully"})


def all_course(request):
    if not request.user.is_authenticated:
        # 判断是否登录
        return JsonResponse({"key": "601", "msg": "please login first"})
    else:
        if request.method == "GET":
            course = models.Course.objects.all()
            # return render(request, 'allcourse.html', context={"course": course})
            # 注释内容可以实现列表展示信息
            resp = {"key": "603", "msg": "Get all courses successfully"}
            for x in course:
                resp.setdefault(x.course_id, x.course_name)
                # (key,d),若key在字典中，返回对应值，d无效；否则添加key-d键值对
            return JsonResponse(resp)
    # Json返回内容的写法



def choose_course(request):
    if not request.user.is_authenticated:
        # 判断是否登录
        return JsonResponse({"key": "601", "msg": "please login first"})
    else:
        if request.method == 'GET':
            course = models.Course.objects.all()
            return render(request, 'choose.html',context={"course": course})
        if request.method == 'POST':
            choice = request.POST.get('choice')
            if not choice:
                # 没有选课
                return JsonResponse({"key": "604", "msg": "you didn't make a choice"})
            else:
                a = Course.objects.get(course_id=choice)
                a.course_student.add(request.user)
                a.save()

                return JsonResponse({"key": "605", "msg": Course.objects.all()[0].course_student})



def my_course(request):
    if not request.user.is_authenticated:
        # 判断是否登录
        return JsonResponse({"key": "601", "msg": "please login first"})
    else:
        if request.method == "GET":
            course = User.objects.get(username=request.user.username).Course_set.all()
            resp = {"key": "606", "msg": "Get you courses successfully"}
            for x in course:
                resp.setdefault(x.course_id, x.course_name)
                # (key,d),若key在字典中，返回对应值，d无效；否则添加key-d键值对
    return JsonResponse(resp)


def delete_course(request):
    if not request.user.is_authenticated:
        # 判断是否登录
        return JsonResponse({"key": "601", "msg": "please login first"})
    else:
        if request.method == 'GET':
            course = User.objects.get(username=request.user.username).Course_set.all()
            # 获取用户所有课程
            return render(request, 'delete.html',context={"course": course})
        if request.method == 'POST':
            delete = request.POST.get('delete')
            if not delete:
                return JsonResponse({"key": "604", "msg": "you didn't make a choice"})
            else:
                a = User.objects.get(username=request.user.username).Course_set.all()
                b = Course.objects.get(course_id=delete)
                a.remove(b)
                a.save()
                return JsonResponse({"key": "607", "msg": "delete course successfully"})


# Create your views here.
