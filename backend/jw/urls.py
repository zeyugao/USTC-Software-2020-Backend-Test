from django.urls import path
from jw import views


urlpatterns = [
    path('getall/', views.GetAllView.as_view(), name='getall_view'),
    path('getprivke/', views.GetPrivkeView.as_view(), name='getprivke_view'),
    path('elecke/', views.ElecKeView.as_view(), name='elecke_view'),
    path('dropke/', views.DropKeView.as_view(), name='dropke_view'),
]

