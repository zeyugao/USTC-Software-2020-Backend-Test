from django.http import JsonResponse
#Here some decorators.
#loginPermission: view function with this decorator need user to login first.
def loginPermission(func):
    def inner(request,**kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"status": 405,"msg": "Please login first."})
        else:
            return func(request,**kwargs)
    return inner

#unLogPermission: with this, user shouldn't login before.
def unLogPermission(func):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return JsonResponse({"status": 404,"msg": "You\'ve login. Please logout first."})
        else:
            return func(request,*args,**kwargs)
    return inner

#methodFilter(['methods allowed', ...]): to only response to specify method.
def methodFilter(allowedMethod):
    def outer(func):
        def inner(request,*args,**kwargs):
            if not (request.method in allowedMethod):
                return JsonResponse({"status": 400,"msg": "Request method mismatch."})
            else:
                return func(request,*args,**kwargs)
        return inner
    return outer

