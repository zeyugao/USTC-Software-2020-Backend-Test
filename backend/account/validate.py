from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re
from django.http import JsonResponse
userModel=get_user_model()

def usernameValidation(username,regFlag=False):
    errList=[]
    #Check conflict.
    if regFlag:
        if userModel.objects.filter(username=username).exists():
            errList.append('Username has been used.')
    #Check length and content.
    if len(username)>=30:
        errList.append('Username shouldn\'t be longer than 30.')
    if not re.search(u'^[_a-zA-Z0-9]+$',username):
        errList.append('Illegal symbol in username.')
    if errList:
        raise ValidationError(errList)

def gradeValidation(grade):
    if not grade.isdigit():
        raise ValidationError('Grade should be a positive number.')
    grade=int(grade)
    if grade<1:
        raise ValidationError('Grade should not be greater than 1.')
    if grade>4:
        raise ValidationError('Grade should not be greater than 4.')





def requiredArgumentValidation(args):
    msg="Argment lost: "
    lost=0
    for i in args:
        if not i[0]:
            msg+=i[1]+" "
            lost+=1
    if lost: raise ValidationError(msg+".")

'''
    To validate the wholeness of request Parameters, and list the lost Parameter. 
    The requiredArgs accepts a list of Parameters the function needs.
    For example:

        @requiredArgumentGET(['username','password'])
        def login(request):
            ......
        
    Then when the function deal with a GET request, it'll work only if username and password were
    both given.
    If not, it will return a status code 401, and message telling you the list of lost parameters.

    Same use as requiredArgumentPost.

    Notice:
    You can use both of them, to deal with different methods.
    For example:

        @requiredArgumentGET(['username','password'])
        @requiredArgumentPOST(['grade'])
        def login(request):
            ......
    
    The first decorator will work when the request method is GET, the second decorator will work 
    when the method is POST. They won't conflict.


'''
def requiredArgumentGET(requiredArgs):
    def outer(func):
        def inner(request,*args,**kwargs):
            if request.method == 'GET':
                lost=0
                msg="Argment lost: "
                for i in requiredArgs:
                    tempArg=request.GET.get(i)
                    if not tempArg:
                        msg+=i+" "
                        lost+=1
                if lost: return JsonResponse({"status":401,"msg":msg+"."})
            return func(request,*args,**kwargs)
        return inner
    return outer


def requiredArgumentPOST(requiredArgs):
    def outer(func):
        def inner(request,*args,**kwargs):
            if request.method == 'POST':
                lost=0
                msg="Argment lost: "
                for i in requiredArgs:
                    tempArg=request.POST.get(i)
                    if not tempArg:
                        msg+=i+" "
                        lost+=1
                if lost: return JsonResponse({"status":401,"msg":msg+"."})
            return func(request,*args,**kwargs)
        return inner
    return outer
