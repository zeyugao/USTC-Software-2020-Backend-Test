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
        user_form = UserForm()
        student_form = StudentForm()
        context = {
            'user_form': user_form,
            'student_form': student_form,
        }
        return JsonResponse({
            'status': 200,
            'msg': '2 forms'
        })
    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        student_form = StudentForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            return JsonResponse({
                'status': 200,
                'msg': 'Student Created Successfully'
            })
        elif not user_form.is_valid():
            return JsonResponse({
                'status': 410,
                'msg': user_form.errors
            })

class Logout(View):
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({
                'status': 200,
                'msg': 'Logout Successfully'
            })
        else:
            return JsonResponse({
                'status': 401,
                'msg': 'Not logged in'
            })