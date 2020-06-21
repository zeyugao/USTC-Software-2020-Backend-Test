from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.password_validation import password_changed, validate_password
from .validate import usernameValidation, gradeValidation, requiredArgumentPOST
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login, logout
from .wrapper import loginPermission, unLogPermission, methodFilter
# Create your views here.
userModel = get_user_model()

'''
    Register function
    注册账户
    method: POST
        POST parameter:
            username<str> : 用户名
            password<str> : 密码
            grade<str> : 年级

        JSON response:
            status<int> : 状态码
            含义
                200 : 成功注册
                400 : 缺少某些参数 （具体参数会在msg中给出）
                401 : 用户名不符合要求
                402 : 密码不符合要求
                403 : 年级设定不符合要求
                405 : 已登陆
            
            msg<str> : 状态码相关解释
'''
@methodFilter(['POST'])
@unLogPermission
@requiredArgumentPOST(['username','password','grade'])
def userRegistration(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        grade = request.POST.get('grade')
        # Validate the username.
        try:
            usernameValidation(username, regFlag=True)
        except ValidationError as e:
            return JsonResponse({"status": 401, "msg": e.messages})
        # Validate the password.
        try:
            validate_password(password, request.user)
        except ValidationError as e:
            return JsonResponse({"status": 402, "msg": e.messages})
        # Validate the grade.
        try:
            gradeValidation(grade)
        except ValidationError as e:
            return JsonResponse({"status": 403, "msg": e.messages})
        # Create a new user.
        userModel.objects.create_user(
            username=username, password=password, grade=grade)
        return JsonResponse({"status": 200, "msg": "Register successfully."})


'''
    Login function
    用户登陆
    用户在使用时应当处于未登陆状态
    method: POST
        POST parameter:
            username<str> : 用户名
            password<str> : 密码

        JSON response:
            status<int> : 状态码
            含义
                200 : 成功登陆
                400 : 缺少某些参数 （具体参数会在msg中给出）
                401 : 用户名不符合要求
                405 : 已登陆
                407 : 用户名或密码错误
            
            msg<str> : 状态码相关解释
'''
@methodFilter(['POST'])
@unLogPermission
@requiredArgumentPOST(['username','password'])
def userLogin(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Validate username
        try:
            usernameValidation(username)
        except ValidationError as e:
            return JsonResponse({"status": 401, "msg": e.messages})
        userInstance = authenticate(
            request, username=username, password=password)
        if userInstance:
            login(request, userInstance)
            return JsonResponse({"status": 200, "msg": "Login successfully."})
        else:
            return JsonResponse({"status": 407, "msg": "Wrong username or password."})

'''
    Logout function
    用户登出
    要求首先登陆
    method : GET
        GET parameter: 无
        JSON response:
            status<int> : 状态码
            含义:
                200 : 成功登出
                406 : 尚未登陆
            msg<str> : 状态码相关解释
'''
@methodFilter(['GET'])
@loginPermission
def userLogout(request):
    if request.method=='GET':
        logout(request)
        return JsonResponse({"status": 200, "msg": "Logout successfully."})

'''
    Change password function
    用户修改密码
    要求首先登陆
    method: POST
        POST parameter:
            oldPassword<str> : 旧密码
            newPassword<str> : 新密码

        JSON response:
            status<int> : 状态码
            含义
                200 : 成功修改密码
                400 : 缺少某些参数 （具体参数会在msg中给出）
                404 : 新旧密码相同
                406 : 尚未登陆
                408 : 新密码不符合要求
                409 : 旧密码错误
            
            msg<str> : 状态码相关解释
'''
@methodFilter(['POST'])
@loginPermission
@requiredArgumentPOST(['oldPassword','newPassword'])
def userChangePassword(request):
    if request.method=='POST':
        oldPassword = request.POST.get('oldPassword')
        newPassword = request.POST.get('newPassword')
        if oldPassword==newPassword:
            return JsonResponse({"status": 404, "msg": "Unchanged password."})
        try:
            validate_password(newPassword, request.user)
        except ValidationError as e:
            return JsonResponse({"status": 408, "msg": e.messages})
        userInstance = authenticate(
            request, username=request.user.username, password=oldPassword)
        if userInstance:
            userInstance.set_password(newPassword)
            userInstance.save()
            login(request, userInstance)
            return JsonResponse({"status": 200, "msg": "Update password successfully."})
        else:
            return JsonResponse({"status": 409, "msg": "Old password is wrong."})

'''
    Set grade function
    用户设定年级
    要求首先登陆
    method: POST
        POST parameter:
            grade<str> : 年级

        JSON response:
            status<int> : 状态码
            含义
                200 : 成功修改年级
                400 : 缺少某些参数 （具体参数会在msg中给出）
                403 : 年级不符合要求
                406 : 尚未登陆
            msg<str> : 状态码相关解释
'''
@methodFilter(['POST'])
@loginPermission
@requiredArgumentPOST(['grade'])
def userSetGrade(request):
    if request.method=='POST':
        grade=request.POST.get('grade')
        try:
            gradeValidation(grade)
        except ValidationError as e:
            return JsonResponse({"status":403,"msg":e.messages})
        request.user.grade=int(grade)
        request.user.save()
        return JsonResponse({"status":200,"msg":"Update grade successfully."})
