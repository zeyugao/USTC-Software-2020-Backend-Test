from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course
from account.models import Student
# Create your views here.
@login_required
def enroll(request, pk):
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