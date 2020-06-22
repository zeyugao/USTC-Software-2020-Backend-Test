from django.shortcuts import redirect
from django.http import JsonResponse
def unauthenticated_user(view_func):#used in login and register.
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return JsonResponse({
                'status': 405,
                'msg': 'Already Logged in'
            })
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func