from django.views.generic.base import View
from django.http import JsonResponse
from django.utils.translation import gettext

class LoginView(View):
    http_method_names = ['get', 'post']

    def get(self, request):
        pass

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        return JsonResponse({
            'code': 200,
            'msg': [gettext('Login successfully')]
        })

class RegisterView(View):
    http_method_names = ['get', 'post']

    def get(self, request):
        pass

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        return JsonResponse({
            'code': 200,
            'msg': [gettext('Register successfully')]
        })


class LogoutView(View):
    http_method_names = ['post']

    def post(self, request):
        return JsonResponse({
            'code': 200,
        })
