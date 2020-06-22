from django.urls import path
from . import views

app_name = "Choose_Courses"

urlpatterns = [
    path('index/', views.index, name="index"),
    path('detail/<int:course_id>', views.get_details, name='detail'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('choose/<int:course_id>', views.choose, name='choose'),
    path('cancel/<int:course_id>', views.cancel, name='cancel'),
    path('show/', views.show, name='show'),
    
]
