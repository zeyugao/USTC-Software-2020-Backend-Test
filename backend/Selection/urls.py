from django.urls import path
from Selection import views


urlpatterns = [
    path('index/', views.index),
    path('login/', views.LoginView.as_view),
    path('register/', views.RegisterView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('account/', views.AccountView.as_view()),
    path('select/', views.SelectView.as_view()),
    path('delete/', views.DelCourseView.as_view()),
]