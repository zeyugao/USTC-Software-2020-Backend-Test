from django.views.generic.base import View
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from accounts.models import Stu

class LoginView(View):
    http_method_names = ['get', 'post']

    def get(self, request):
        pass

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_login = authenticate(request, username=username, password=password)
        if user_login:
            login(request, user_login)
            return JsonResponse({
                'code': 200,
                'msg': 'Login successfully'
            })
        else:
            return JsonResponse({
                'code': 401,
                'msg': 'Invalid username or password'
            })


class RegisterView(View):
    http_method_names = ['get', 'post']

    def get(self, request):
        pass

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if Stu.user.objects.filter(username=username).exists():
            return JsonResponse({
                'code': 401,
                'msg': 'Invalid username'
            })
        Stu.user.objects.create_user(username=username, password=password)
        return JsonResponse({
            'code': 200,
            'msg': 'Register successfully'
        })


class LogoutView(View):
    http_method_names = ['get', 'post']

    def get(self, request):
        pass

    def post(self, request):
        logout(request)
        return JsonResponse({
            'code': 200,
        })
