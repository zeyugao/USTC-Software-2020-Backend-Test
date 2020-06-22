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
        return JsonResponse({
            'status': 200,
            'msg': course
        })
    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        course = Course.objects.get(pk = pk)
        student = request.user.student
        if student in course.student:
            return JsonResponse({
                'status': 200,
                'msg': 'Already Enrolled in'
            })
        course.student.add(student)
        return JsonResponse({
            'status': 200,
            'msg': 'Added Successfully'
        })

class AllCourses(View):
    def get(self, request, *args, **kwargs):
        queryset = Course.objects.all()
        return JsonResponse({
            'status': 200,
            'msg': queryset
        })

@method_decorator(login_required, name = 'dispatch')
class MyCourse(View):
    def get(self, request, *args, **kwargs):
        courses = request.user.student.course_set.all()
        return JsonResponse({
            'status': 200,
            'msg': courses
        })

@method_decorator(login_required, name = 'dispatch')
class DropCourse(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'msg': 'Course not found'
            })
        return JsonResponse({
            'status': 200,
            'msg': course
        })
    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
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