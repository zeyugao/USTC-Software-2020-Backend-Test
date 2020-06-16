from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
# Create your views here.

class Login(View):
    def get(self, request):
        pass
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                'status': 200,
                'msg': 'Login Successfully'
            })
        else:
            return JsonResponse({
                'status': 401,
                'msg': 'Login Failed'
            })

class Register(View):
    def get(self, request):
        pass
    def post(self, request, *args, **kwargs):
        grade_dict = {
            'Freshman': 'FR',
            'Sophmore': 'SO',
            'Junior': 'JR',
            'Senior': 'SR',
            'Graduate': 'GR',
        }
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        try:#TO DO!!
            validate(username)
        except ValidationError as e:
            return JsonResponse({
                'status': 410,
                'msg': e.messages
            })
        try:#TO DO!!
            validate(password1)
        except ValidationError as e:
            return JsonResponse({
                'status': 410,
                'msg': e.messages
            })
        try:
            grade = grade_dict[request.POST.get('grade')]
        except KeyError:
            return JsonResponse({
                'status': 410,
                'msg': 'Key does not exist'
            })
        user = User.objects.create(username=username, password=password1)
        Student.objects.create(
            user = user,
            grade = grade
        )
        return JsonResponse({
            'status': 200,
            'msg': 'Student Created Successfully'
        })

class Logout(View):
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
        return JsonResponse({
            'status': 200,
            'msg': 'Logout Successfully'
        })