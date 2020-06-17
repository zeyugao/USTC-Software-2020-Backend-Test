from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Course
from account.models import Student
from django.views import View
from django.utils.decorators import method_decorator
# Create your views here.

@method_decorator(login_required, name = 'dispatch')
class Enroll(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        try:
            course = Course.objects.get(pk = pk)
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

class AllCourses(View):
    def get(self, request, *args, **kwargs):
        queryset = Course.objects.all()
        context = { 'queryset': queryset }
        return JsonResponse({
            'status': 200,
            'msg': 'Success'
        })

@method_decorator(login_required, name = 'dispatch')
class AvailableCourses(View):
    def get(self, request, *args, **kwargs):
        my_grade = request.user.student.grade
        queryset = Course.objects.filter(grade=my_grade)
        context = { 'queryset': queryset }
        return JsonResponse({
            'status': 200,
            'msg': 'Success'
        })

@login_required
class MyCourse(View):
    def get(self, request, *args, **kwargs):
        courses = request.user.student.course_set.all()
        context = { 'courses': courses }
        return JsonResponse({
            'status': 200,
            'msg': 'Success'
        })

@method_decorator(login_required, name = 'dispatch')
class DropCourse(View):
    def get(self, request, *args, **kwargs):
        pass
    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'msg': 'Course not found'
            })
        try:
            request.user.student.course_set.remove(course)
        except ValueError:
            return JsonResponse({
                'status': 409,
                'msg': 'Course Not Enrolled in'
            })
        return JsonResponse({
            'status': 200,
            'msg': 'Course Dropped'
        })