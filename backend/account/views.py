from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .form import LoginForm, RegistrationForm
from .models import Student, Course
from django import views
import hashlib

# Create your views here.

# learn from https://blog.csdn.net/qq_39138295/article/details/82762940

def setPassword(password):
    """
    加密密码，算法单次md5
    :param apssword: 传入的密码
    :return: 加密后的密码
    """
    md5 = hashlib.md5()
    md5.update(password.encode())
    password = md5.hexdigest()
    return str(password)

def  checklog(request):
    """
    检查用户是否登录
    :param request:
    :return:登录   用户姓名
            未登录  Flase

    """
    name=request.session.get('stu_name')
    if name:
        return  name
    else:
        return  False



class Login(views.View):
    '''
       登陆类
       返回错误码和错误信息
    '''
    # get请求方式
    def get(self, request):
        # 用自定义的Form类实例化一个对象，用于前端页面生成标签
        login_obj = LoginForm()
        return render(request, 'register.html', {'login_obj': login_obj})

    # post请求方式
    def post(self, request):
        res = {'code': 100}
        login_obj = LoginForm(request.POST)
        if login_obj.is_valid():
            e= Student.objects.filter(stu_name=login_obj.stu_name)
            if not e:   # 用户不存在
                res['code'] = 101
                res['msg'] = '用户名不存在，请重新输入'
            else:       # 用户存在
                if setPassword(login_obj.stu_password) == e.stu_passward:
                   # 返回前端页面要跳转的url
                   res['code']=100
                   res['msg'] = '/index/'

                else:
                   res['code']=102
                   res['msg']='密码错误，请重新输入'
                   request.session['stu_name']=e.stu_name
        else:  # 格式不正确
            res['code'] = 103
            # 错误信息
            res['msg'] = login_obj.errors
        return JsonResponse(res)



class  Logout(views.View):
    '''
       退出类
       要求用户已经登录
       return:错误码和错误信息
    '''
    # get请求方式
    def get(self, request):
        # 用自定义的Form类实例化一个对象，用于前端页面生成标签
        return HttpResponseRedirect('/logout/')

    # post请求方式
    def post(self, request):
        res = {'code': 300}
        name = checklog(request)
        if name:  # 修改 若用户已登录s
            request.session.delete("request.session.session_key")
            res['msg'] = '/login'
        else:
            res['code']=301
            res['msg']='用户未登录'

        return JsonResponse(res)


class Register(views.View):
    '''
       注册类
       return:错误码和错误信息
    '''
    # get请求方式
    def get(self, request):
        # 用自定义的Form类实例化一个对象，用于前端页面生成标签
        register_obj = RegistrationForm()
        return render(request, 'register.html', {'register_obj': register_obj})

    # post请求方式
    def post(self, request):
        res = {'code': 200}
        register_obj = RegistrationForm(request.POST)
        if register_obj.is_valid():
            name = Student.objects.filter(stu_name=request.POST.get('stu_name'))
            if name:    # 用户已存在
                res['code'] = 201
                res['msg'] = '用户名已存在，请重新输入'
            else:      # 用户不存在
                name = register_obj.stu_name
                grade = register_obj.stu_grade
                password = register_obj.stu_password
                Student.objects.create(
                    stu_name=name,
                    stu_grade=grade,
                    stu_password=setPassword(password),
                )
                # 返回前端页面要跳转的url
                res['msg'] = '/login/'
        else:
            res['code'] = 202
            # 错误信息
            res['msg'] = register_obj.errors
        return JsonResponse(res)



class Index(views.View):
    """
        选课系统主页
    """
    http_method_names = ['get','post']

    def  get(self,request):
        """
         在登录情况下，显示选课系统主页所有课程
        :param request:
        :return:400  成功并显示全部课程
                401  用户未登录
        """
        res={'code' : 400, }
        if checklog(request):  # 检查用户是否登录，用户登录
           courses = Course.objects.all()
           res['msg']='successfully'
           return render(request, 'index.html', {'courses': courses})
        else:
            res['code']=401
            res['msg']='用户未登录'
            return  JsonResponse(res)

    def post(self,request):
        """
        在登录情况下，根据“”选择课程
        :param request: 包含‘course-id’
        :return:
        """
        res = {'code': 400, }
        if checklog(request):  # 检查用户是否登录，用户登录
            stu_name=request.POST('stu_name')  # checklog
            course_id=request.POST('course_id')
            student=Student.objects.filter(stu_name=stu_name)
            course=Course.objects.filter(id=course_id)
            chosen_courses=Student.objects.get(stu_name=stu_name).courses.all()

            if course in chosen_courses:    # 已选课程
                res['code']=402
                res['msg']='退课成功'
            else:
                student.courses.add(course)
                res['code'] = 403
                res['msg'] = '选课成功'
        else:
            res['code'] = 401
            res['msg'] = '用户未登录'
        return JsonResponse(res)



class Grade_Index(views.View):
    '''
    年级主页
    显示符合用户年级的课程，并完成退/选操作
    '''
    http_method_names = ['get', 'post']

    def get(self, request):
        """
         在登录情况下，显示年级主页所有课程
        :param request:
        :return:500  成功并显示符合用户年级的全部课程
                501  用户未登录
        """
        res = {'code': 500, }
        name=checklog(request)
        if name:  # 检查用户是否登录，用户登录
            student=Student.objects.filter(stu_name=name)
            courses = Course.objects.filter(course_grade=student.stu_grade)
            res['msg'] = 'successfully'
            return render(request, 'index.html', {'courses': courses})
        else:
            res['code'] = 501
            res['msg'] = '用户未登录'
            return JsonResponse(res)

    def post(self, request):
        """
         在登录情况下，选/退 课程
        :param request: 获取‘course-id’和登录用户的信息
        :return: 502 退课成功
                 503 选课成功
        """
        res = {'code': 500, }
        name=checklog(request)
        if name:  # 检查用户是否登录，用户登录
            course_id = request.POST('course_id')   #  从request中获取用户选择的课程id
            student = Student.objects.filter(stu_name=name)
            course = Course.objects.filter(id=course_id)
            chosen_courses = Student.objects.get(stu_name=name).courses.all()

            if course in chosen_courses:  # 已选课程
                res['code'] = 502
                res['msg'] = '退课成功'
            else:
                student.courses.add(course)
                res['code'] = 503
                res['msg'] = '选课成功'
        else:
            res['code'] = 504
            res['msg'] = '用户未登录'
        return JsonResponse(res)

class Personal_Index(views.View):
    """
     显示用户个人信息和已选课程,并可对已选课程进行退课操作
    """
    http_method_names = ['get', 'post']

    def get(self, request):
        """
         在登录情况下，显示个人主页
        :param request:
        :return:600  成功
                601  用户未登录
        """
        res = {'code': 600, }
        name = checklog(request)
        if name:  # 检查用户是否登录，用户登录
            student = Student.objects.filter(stu_name=name)
            chosen_courses=student.courses.all()
            res['msg'] = 'successfully'
            return render(request, 'personal_index.html', {'courses': chosen_courses},{'student':student})
        else:
            res['code'] = 601
            res['msg'] = '用户未登录'
            return JsonResponse(res)

    def post(self, request):
        """
         在登录情况下，选/退 课程
        :param request: 获取‘course-id’和登录用户的信息
        :return: 602退课成功

        """
        res = {'code': 600, }
        name = checklog(request)
        if name:  # 检查用户是否登录，用户登录
            course_id = request.POST('course_id')  # 从request中获取用户选择的课程id
            student = Student.objects.filter(stu_name=name)
            course = Course.objects.filter(id=course_id)
            chosen_courses = Student.objects.get(stu_name=name).courses.all()

            if course in chosen_courses:  # 已选课程
                student.courses.remove(course)
                res['code'] = 602
                res['msg'] = '退课成功'

            else:
                res['code'] = 603
                res['msg'] = '未选该课程'
        else:
            res['code'] = 601
            res['msg'] = '用户未登录'
        return JsonResponse(res)
