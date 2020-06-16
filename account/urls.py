from django.urls import path
from account import views

urlpatterns = [
    path('register/', views.account_register),
    path('login/', views.account_login),
    path('logout/', views.account_logout),
    path('allcourse/', views.all_course),
    path('choose/', views.choose_course),
    path('mycourse/', views.my_course),
    path('delete/', views.delete_course),

]
