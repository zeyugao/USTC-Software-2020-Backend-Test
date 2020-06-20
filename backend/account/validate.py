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
