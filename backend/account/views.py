import re
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout,get_user_model

Account = get_user_model()


# Create your views here.
def AccountExist(username):
    if len(Account.objects.filter(username = username)) == 0:
        return '1'#This username not exist
    else:
        return '0'#This username exist

def AccountValid(username,password):
    if len(username) == 0 or len(password) == 0 or username == None or password == None:
        return '2'
    if len(re.search('PB[0-9]+|SA[0-9]+|BA[0-9]+|',username).group()) != 10:#username is not the studnet ID
        return '3'
    if not re.search(u'^[_0-9a-zA-Z]+$',password) or len(password) < 6 or len(password) > 20:#password have invalid character or length
        return '4'
    return '0'

def Login(request):
    loginmsg = {
    '0':'Login successful',
    '1':'Login failed!This account is not exist',
    '2':'Login failed!Your username or password is blank,please input something',
    '3':'Login failed!Password is wrong'
    }
    loginstatus = {
        '0':200,
        '1':201,
        '2':202,
        '3':203
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if len(username) == 0 or len(password) == 0 or username == None or password == None:
            return JsonResponse({'status':loginstatus['2'],'error_msg':loginmsg['2']})
        else:
            if AccountExist(username) != '0':
                return JsonResponse({'status':loginstatus['1'],'error_msg':loginmsg['1']})
            else:
                account = authenticate(request,username = username,password = password)
                if account:
                    login(request,account)
                    return JsonResponse({'status':loginstatus['0'],'error_msg':loginmsg['0']})
                else:
                    return JsonResponse({'status':loginstatus['3'],'error_msg':loginmsg['3']})

def Logout(request):
    if request.method == 'GET':
        logout(request)
        return JsonResponse({'status':100,'error_msg':'Logout successful'})

def Register(request):
    registermsg = {
    '0':'Register successful',
    '1':'Register failed!This account has already existed',
    '2':'Register failed!Your username or password is blank,please input something',
    '3':'Register failed!Your username is invalid,please use your student ID to register',
    '4':'Register failed!Your passward is invalid,only letters,numbers and underline can be used.Make sure the length of it between 6 and 20',
    '5':'Register failed!Your grade is invalid,only 1 to 4 is accepted'
    }
    registerstatus = {
        '0':300,
        '1':301,
        '2':302,
        '3':303,
        '4':304,
        '5':305
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        grade = request.POST['grade']
        error_code = AccountValid(username,password)
        if error_code != '0':
            return JsonResponse({'status':registerstatus[error_code],'error_msg':registermsg[error_code]})
        else:
            if AccountExist(username) != '1':
                return JsonResponse({'status':registerstatus['1'],'error_msg':registermsg['1']})
            elif grade <= '0' or grade > '4':
                return JsonResponse({'status':registerstatus['5'],'error_msg':registermsg['5']})
            else:
                Account.objects.create_user(username=username,password=password,grade=grade)
                return JsonResponse({'status':registerstatus['0'],'error_msg':registermsg['0']})
