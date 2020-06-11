from django.views.generic.base import View
from django.http import JsonResponse
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class LoginView(View):
    http_method_names = ['get', 'post']

    def get(self, request):
        pass

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
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

        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'code': 401,
                'msg': 'Invalid username'
            })
        User.objects.create_user(username=username, password=password)
        return JsonResponse({
            'code': 200,
            'msg': 'Register successfully'
        })


class LogoutView(View):
    http_method_names = ['post']

    def post(self, request):
        logout(request)
        return JsonResponse({
            'code': 200,
        })
