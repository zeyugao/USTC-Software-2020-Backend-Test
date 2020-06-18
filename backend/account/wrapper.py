from django.http import JsonResponse
def loginPermission(func):
    def inner(request,**kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"status": 405,"msg": "Please login first."})
        else:
            return func(request,**kwargs)
    return inner

def unLogPermission(func):
    def inner(request,**kwargs):
        if request.user.is_authenticated:
            return JsonResponse({"status": 404,"msg": "You\'ve login. Please logout first."})
        else:
            return func(request,**kwargs)
    return inner