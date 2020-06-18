from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.password_validation import password_changed, validate_password
from .validate import usernameValidation, validationErr
from django.core.exceptions import ValidationError as sysValiErr
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login, logout
from .wrapper import loginPermission,unLogPermission
# Create your views here.
userModel = get_user_model()


@unLogPermission
def userRegistration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username:
            return JsonResponse({"status": 401,"msg": "Please input username."})
        if not password:
            return JsonResponse({"status": 402,"msg": "Please input password."})
        # Validate username
        try:
            usernameValidation(username, regFlag=True)
        except validationErr as e:
            return JsonResponse({"status": 401,"msg": e.msg})
        # Validate password
        try:
            validate_password(password, request.user)
        except sysValiErr as e:
            return JsonResponse({"status": 402,"msg": e.messages})
        # create new user
        userModel.objects.create_user(
            username=username, password=password,grade=0,)
        return JsonResponse({"status": 200,"msg": "Register successfully."})

    else:
        return JsonResponse({"status": 400,"msg": "Request method mismatch."})

@unLogPermission
def userLogin(request):
    if request.user.is_authenticated:
        return JsonResponse({"status": 404,"msg": "You have login."})
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username:
            return JsonResponse({"status": 401,"msg": "Please input username."})
        if not password:
            return JsonResponse({"status": 402,"msg": "Please input password."})
        # Validate username
        try:
            usernameValidation(username)
        except validationErr as e:
            return JsonResponse({"status": 401,"msg": e.msg})
        userInstance = authenticate(
            request, username=username, password=password)
        if userInstance:
            login(request, userInstance)
            return JsonResponse({"status": 200,"msg": "Login successfully."})
        else:
            return JsonResponse({"status": 403,"msg": "Wrong username or password."})

    else:
        return JsonResponse({"status": 400,"msg": "Request method mismatch."})

@loginPermission
def userLogout(request):
    logout(request)
    return JsonResponse({"status": 200,"msg": "Logout successfully."})

@loginPermission
def userChangePassword(request):
    if request.method == 'POST':
        oldPassword = request.POST.get('oldPassword')
        newPassword = request.POST.get('newPassword')
        if not oldPassword:
            return JsonResponse({"status": 407,"msg": "Please input old password."})
        if not newPassword:
            return JsonResponse({"status": 408,"msg": "Please input new password."})
        try:
            validate_password(newPassword, request.user)
        except sysValiErr as e:
            return JsonResponse({"status": 409,"msg": e.messages})
        userInstance = authenticate(
            request, username=request.user.username, password=oldPassword)
        if userInstance:
            userInstance.set_password(newPassword)
            userInstance.save()
            login(request,userInstance)
            return JsonResponse({"status": 200,"msg": "Update password successfully."})
        else:
            return JsonResponse({"status": 410,"msg": "Old password is wrong."})
    else:
        return JsonResponse({"status": 400,"msg": "Request method mismatch."})
