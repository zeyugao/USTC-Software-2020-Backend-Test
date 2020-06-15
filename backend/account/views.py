from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.

def loginPage(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'login successful')
            return redirect('home')
        else:
            messages.info(request, 'username or password invalid, please try again')
    return render(request, 'enrollmentSystem/login.html', context)

def registerPage(request):
    form = UserForm()
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.clean_data['username']
            grade = form.clean_data['grade']
            Student.objects.create(
                user = user, 
                grade = grade
            )
            messages.success(request, 'Student ' + username + ' added successfully')
            return redirect('login')
    return render(request, 'enrollmentSystem/register.html', context)

def logoutPage(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

