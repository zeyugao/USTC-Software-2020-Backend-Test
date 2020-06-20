from django.urls import path
from . import views


urlpatterns = [
    path('userCourseResult',views.listUserResult,name='revResult'),
    path('chooseCourse',views.chooseCourse,name='revChooseCourse'),
    path('setLearnStatus',views.setLearnStatus,name='revSetLearnStatus'),
    path('exitCourse',views.exitCourse,name='revExitCourse'),
    path('listAllCourse',views.listAllCourse,name='revListAllCourse'),
    path('listPrefix',views.listPrefix,name='revListPrefix'),
    path('haveLearntCourse',views.haveLearntCourse,name='revHaveLearntCourse')
]