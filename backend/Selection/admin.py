from django.contrib import admin
from . import models


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'gender')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_id')


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Course, CourseAdmin)