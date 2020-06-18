from django.urls import path
from . import views


urlpatterns = [
    path('register',views.userRegistration,name='revReg'),
    path('login',views.userLogin,name='revLogin'),
    path('logout',views.userLogout,name='revLogout'),
    path('changePassword',views.userChangePassword,name='revChangePassword'),
]