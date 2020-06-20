from django.http import JsonResponse,HttpResponse
#Here some decorators.
#loginPermission: view function with this decorator need user to login first.

'''
    To only response to request with user's authentication.
    For example, choosing course and changing password need user to logged in before.
        
        @loginPermission
        def changePassword(request):
            ...
        
    Then if the user hasn't logged in before, the function will return a status code 405.
'''
def loginPermission(func):
    def inner(request,**kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"status": 405,"msg": "Please login first."})
        else:
            return func(request,**kwargs)
    return inner


'''
    To only response to request without user's authentication.
    For example, if you want to register or login, it's necessary that he hasn't logged in.

        @unLogPermission
        def login(request):
            ......
        
    If the user has logged in before, the function will return a status code 404.
'''
def unLogPermission(func):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return JsonResponse({"status": 404,"msg": "You\'ve login. Please logout first."})
        else:
            return func(request,*args,**kwargs)
    return inner


'''
    To only response to specify method.
    The argument allowMethod will accept a list of chosen method.
    For example:

        @methodFilter(['GET','POST'])
        def viewFunction(request):
            ......
        
    Then the viewFunction will only response to GET and POST method.
    Other methods will be responsed with http status 405 (Method Not Allowed).
'''
def methodFilter(allowedMethod):
    def outer(func):
        def inner(request,*args,**kwargs):
            if not (request.method in allowedMethod):
                return HttpResponse("Method mismatch.",status=405)
            else:
                return func(request,*args,**kwargs)
        return inner
    return outer

