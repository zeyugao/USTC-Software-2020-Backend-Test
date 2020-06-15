from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Course
from account.models import Student
# Create your views here.
@login_required
def enroll(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return JsonResponse({
            'status': 404,
            'msg': 'Course not found'
        })
    context = { 'course': course }
    if request.method == 'POST':
        student = request.user.student
        course.student.add(student)
        return JsonResponse({
            'status': 200,
            'msg': 'Added Successfully'
        })

def allCourses(request):
    queryset = Course.objects.all()
    context = { 'queryset': queryset }
    return JsonResponse({
        'status': 200,
        'msg': 'Success'
    })

@login_required
def availableCourses(request):
    my_grade = request.user.student.grade
    queryset = Course.objects.filter(grade=my_grade)
    context = { 'queryset': queryset }
    return JsonResponse({
        'status': 200,
        'msg': 'Success'
    })

@login_required
def myCourse(request):
    courses = request.user.student.course_set.all()
    context = { 'courses': courses }
    return JsonResponse({
        'status': 200,
        'msg': 'Success'
    })

@login_required
def dropCourse(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return JsonResponse({
            'status': 404,
            'msg': 'Course not found'
        })
    if request.method == 'POST':
        request.user.student.course_set.remove(course)
        return JsonResponse({
            'status': 200,
            'msg': 'Course Dropped'
        })