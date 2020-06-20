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


@unLogPermission
@methodFilter(['POST'])
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
            return JsonResponse({"status": 411, "msg": e.messages})
        # Create a new user.
        userModel.objects.create_user(
            username=username, password=password, grade=grade)
        return JsonResponse({"status": 200, "msg": "Register successfully."})


@unLogPermission
@methodFilter(['POST'])
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
            return JsonResponse({"status": 403, "msg": "Wrong username or password."})


@loginPermission
@methodFilter(['GET'])
def userLogout(request):
    if request.method=='GET':
        logout(request)
        return JsonResponse({"status": 200, "msg": "Logout successfully."})


@loginPermission
@methodFilter(['POST'])
@requiredArgumentPOST(['oldPassword','newPassword'])
def userChangePassword(request):
    if request.method=='POST':
        oldPassword = request.POST.get('oldPassword')
        newPassword = request.POST.get('newPassword')
        try:
            validate_password(newPassword, request.user)
        except ValidationError as e:
            return JsonResponse({"status": 409, "msg": e.messages})
        userInstance = authenticate(
            request, username=request.user.username, password=oldPassword)
        if userInstance:
            userInstance.set_password(newPassword)
            userInstance.save()
            login(request, userInstance)
            return JsonResponse({"status": 200, "msg": "Update password successfully."})
        else:
            return JsonResponse({"status": 410, "msg": "Old password is wrong."})


@loginPermission
@methodFilter(['POST'])
@requiredArgumentPOST(['grade'])
def userSetGrade(request):
    if request.method=='POST':
        grade=request.POST.get('grade')
        try:
            gradeValidation(grade)
        except ValidationError as e:
            return JsonResponse({"status":417,"msg":e.messages})
        request.user.grade=int(grade)
        request.user.save()
        return JsonResponse({"status":200,"msg":"Update grade successfully."})
