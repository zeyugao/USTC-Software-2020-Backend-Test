from django.urls import path
from account import views
app_name = 'account'

urlpatterns = [
    path('login',views.Login,name = 'login'),
    path('register',views.Register,name = 'register'),
    path('logout',views.Logout,name = 'logout'),
]