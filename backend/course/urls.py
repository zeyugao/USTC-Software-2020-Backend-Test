from django.urls import path
from . import views


urlpatterns = [
    path('result',views.listUserResult,name='revResult'),
    path('choose',views.chooseCourse,name='revChoose'),
    path('setLearnStatus',views.setLearnStatus,name='revSetLearnStatus'),
    path('exitCourse',views.exitCourse,name='revExitCourse'),
    path('list',views.listAllCourse,name='revList'),
    path('prefix',views.listPrefix,name='revPrefix'),
    path('haveLearntCourse',views.haveLearntCourse,name='revHaveLearntCourse')
]