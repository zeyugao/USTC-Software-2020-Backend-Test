from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
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
            Student.objects.create(
                user = user, 
                name = username
            )
            messages.success(request, 'Student ' + username + ' added successfully')
            return redirect('login')
    return render(request, 'enrollmentSystem/register.html', context)

def logoutPage(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

@login_required
def course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    context = { 'course': course }
    if request.method == 'POST':
        student = request.user.student
        course.student.add(student)
    return render(request, 'enrollmentSystem/course.html', context)

def allCourses(request):
    queryset = Course.objects.all()
    context = { 'queryset': queryset }
    return render(request, 'enrollmentSystem/all_courses.html', context)

@login_required
def availableCourses(request):
    my_grade = request.user.student.grade
    queryset = Course.objects.filter(grade=my_grade)
    context = { 'queryset': queryset }
    return render(request, 'enrollmentSystem/available_courses.html', context)

@login_required
def myCourse(request):
    courses = request.user.student.course_set.all()
    context = { 'courses': courses }
    return render(request, 'enrollmentSystem/my_course.html', context)

@login_required
def dropCourse(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        request.user.student.course_set.remove(course)
        return redirect('my_course')