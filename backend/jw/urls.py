from django.urls import path
from jw import views


urlpatterns = [
    path('getall/', views.GetAllView.as_view(), name='getall_view'),
]

