from django.shortcuts import render
from django.http import JsonResponse
from .models import course, courseResult, coursePrefix
from django.contrib.auth import get_user_model
from account.wrapper import loginPermission, unLogPermission, methodFilter
from account.validate import requiredArgumentValidation, gradeValidation
from django.core.exceptions import ValidationError
from .filters import userGETFilter, normalGETFilter
from account.validate import requiredArgumentGET

userModel = get_user_model()

'''
    List course result
    列出当前用户选择的课程以及学习情况
    要求首先登陆
    method : GET
        GET parameter:
            gradeFilter<int> : 是否只展示合乎用户年级的课程（需要登陆，可以缺省）
            含义：
                1 : 只展示要求年级小于等于用户年级的课程
                其他值或缺省 : 展示所有已选中的课程
        
        JSON response:
            status<int> : 状态码
            含义:
                200 : 成功查询
                406 : 尚未登陆

            total<int> : 查询到的课程数目

            course<list> :查询课程结果
                |---- pk<str> : 课程唯一编码
                |---- course<str> : 课程名称
                |---- haveLearnt<boolean> : 是否已经学习
            
            msg<str> : 状态码相关解释
'''
@methodFilter(['GET'])
@loginPermission
@userGETFilter([('result__grade', 'gradeFilter', 'grade')])
def listUserResult(request, userFilter):
    if request.method == 'GET':
        result = [{"pk": i.result.courseID,
                   "course": i.result.name,
                   "haveLearnt": i.haveLearnt
                   } for i in request.user.resultSet.all().filter(**userFilter)]
        return JsonResponse({"status": 200, "total": len(result), "course": result})

'''
    Set learning status
    更新学习情况
    要求首先登陆
    method : GET
        GET parameter:
            pk<str> : 课程唯一编码
        
        JSON response:
            status<int> : 状态码
            含义:
                200 : 成功更新
                400 : 缺少某些参数 （具体参数会在msg中给出）
                406 : 尚未登陆
                410 : 尚未选择这门课
                413 : 已经学习过这门课
            
            msg<str> : 状态码相关解释
'''
@methodFilter(['GET'])
@loginPermission
@requiredArgumentGET(['pk'])
def setLearnStatus(request):
    if request.method == 'GET':
        pk = request.GET.get('pk')

        # Check if the course has been chosen.
        userSearchResult = request.user.resultSet.filter(result__courseID=pk)
        if not userSearchResult:
            return JsonResponse({"status": 410, "msg": "You havn\'t chosen the course."})

        # Check if the chosen course has been learnt.
        userSearchResult = userSearchResult[0]
        if userSearchResult.haveLearnt:
            return JsonResponse({"status": 413, "msg": "You have learnt the course."})

        # Update learning status.
        userSearchResult.haveLearnt = True
        userSearchResult.save()
        return JsonResponse({"status": 200, "msg": "Update the learning status successfully."})

'''
    Choose course
    用户选课
    要求首先登陆
    method : GET
        GET parameter:
            pk<str> : 课程唯一编码
        
        JSON response:
            status<int> : 状态码
            含义:
                200 : 成功选课
                400 : 缺少某些参数 （具体参数会在msg中给出）
                406 : 尚未登陆
                411 : 已经选择这门课
                414 : 课程不存在
                415 : 课程不符合年级
                416 : 前置课程未学习
            
            requiredPk<list> : 状态码为416时，返回还未学习的前置课程
                |---- pk<str> : 课程唯一编码
            
            msg<str> : 状态码相关解释
'''
@methodFilter(['GET'])
@loginPermission
@requiredArgumentGET(['pk'])
def chooseCourse(request):
    if request.method == 'GET':
        pk = request.GET.get('pk')

        # Check if the course has been chosen.
        userSearchResult = [(i.result.courseID, i.haveLearnt)
                            for i in request.user.resultSet.all()]
        if any(i[0] == pk for i in userSearchResult):
            return JsonResponse({"status": 411, "msg": "You\'ve chosen the course."})

        # Check if the course exists.
        searchResult = course.objects.filter(courseID=pk)
        if not searchResult:
            return JsonResponse({"status": 414, "msg": "The course doesn\'t exists."})
        searchResult = searchResult[0]

        # Check grade.
        if not searchResult.grade == request.user.grade:
            return JsonResponse({"status": 415, "msg": "Not for your grade."})

        # Check if all prefix have been achieved.
        prefixList = [i.prefix.courseID for i in searchResult.prefixSet.all()]
        requiredPrefix = []
        for i in prefixList:
            if not ((i, True) in userSearchResult):
                requiredPrefix.append({"pk": i})
        if requiredPrefix:
            return JsonResponse({"status": 416, "msg": "You haven\'t met all requirement.", "requiredPk": requiredPrefix})

        # Choose course, write it in result.
        resultInstance = courseResult(
            learner=request.user, result=searchResult, haveLearnt=False)
        resultInstance.save()
        return JsonResponse({"status": 200, "msg": "Choose course successfully."})

'''
    Exit course
    用户退课
    要求首先登陆
    method : GET
        GET parameter:
            pk<str> : 课程唯一编码
        
        JSON response:
            status<int> : 状态码
            含义:
                200 : 成功退课
                400 : 缺少某些参数 （具体参数会在msg中给出）
                406 : 尚未登陆
                410 : 未选择这门课
                413 : 已经学习过这门课
            
            msg<str> : 状态码相关解释
'''
@methodFilter(['GET'])
@loginPermission
@requiredArgumentGET(['pk'])
def exitCourse(request):
    if request.method == 'GET':
        pk = request.GET.get('pk')

        # Check if the course has been chosen.
        userSearchResult = request.user.resultSet.filter(result__courseID=pk)
        if not userSearchResult:
            return JsonResponse({"status": 410, "msg": "You havn\'t chosen the course."})

        # Check if the chosen course has been learnt.
        userSearchResult = userSearchResult[0]
        if userSearchResult.haveLearnt:
            return JsonResponse({"status": 413, "msg": "You have learnt the course."})

        # Exit the course.
        userSearchResult.delete()
        return JsonResponse({"status": 200, "msg": "Exit the course successfully."})

'''
    List all course
    课程列表
    不要求登陆
    method : GET
        GET parameter:
            gradeFilter<int> : 是否只展示合乎用户年级的课程（需要登陆，可以缺省）
            含义：
                1 : 只展示要求年级小于等于用户年级的课程
                其他值或缺省 : 展示所有已选中的课程
            grade<int> : 只展示指定年级的课程（可以缺省）
        
        JSON response:
            status<int> : 状态码
            含义:
                200 : 成功查询
                406 : 尚未登陆
                403 : 年级不符合要求

            total<int> : 查询到的课程数目

            course<list> : 查询课程结果
                |---- pk<str> : 课程唯一编码
                |---- course<str> : 课程名称
            
            msg<str> : 状态码相关解释
'''
@methodFilter(['GET'])
@userGETFilter([('grade', 'gradeFilter', 'grade')])
@normalGETFilter([('grade', 'grade')])
def listAllCourse(request, userFilter, normalFilter):
    if request.method == 'GET':
        grade = request.GET.get('grade')
        if grade:
            try:
                gradeValidation(grade)
            except ValidationError as e:
                return JsonResponse({"status": 403, "msg": e.messages})
        result = course.objects.all().filter(**userFilter).filter(**normalFilter)
        result = [{"pk": i.courseID, "course": i.name} for i in result]

        return JsonResponse({"status": 200, "total": len(result), "course": result})

'''
    List prefix
    查询前置课程
    不要求登陆
    method : GET
        GET parameter:
            pk<int> : 课程唯一编码
        
        JSON response:
            status<int> : 状态码
            含义:
                200 : 成功查询
                400 : 缺少某些参数 （具体参数会在msg中给出）
                406 : 尚未登陆
                414 : 课程不存在

            total<int> : 查询到的课程数目

            course<list> : 查询课程结果
                |---- pk<str> : 课程唯一编码
                |---- course<str> : 课程名称
            
            msg<str> : 状态码相关解释
'''
@methodFilter(['GET'])
@requiredArgumentGET(['pk'])
@userGETFilter([('prefix__grade', 'gradeFilter', 'grade')])
def listPrefix(request,userFilter):
    if request.method == 'GET':
        pk = request.GET.get('pk')
        searchResult = course.objects.filter(courseID=pk)
        if not searchResult:
            return JsonResponse({"status": 414, "msg": "The course doesn\'t exists."})
        result = [{
            "pk": i.prefix.courseID,
            "course": i.prefix.name} for i in searchResult[0].prefixSet.all().filter(**userFilter)]
        return JsonResponse({"status": 200, "total": len(result), "course": result})

'''
    Learning status
    查询课程学习状况
    要求登陆
    method : GET
        GET parameter:
            pk<str> : 课程唯一编码
        
        JSON response:
            status<int> : 状态码
            含义:
                200 : 成功查询
                400 : 缺少某些参数 （具体参数会在msg中给出）
                406 : 尚未登陆
                410 : 尚未选择这门课
            
            haveLearnt<boolean> : 当状态码为200时，查询结果，是否已学
            
            msg<str> : 状态码相关解释
'''
@methodFilter(['GET'])
@loginPermission
@requiredArgumentGET(['pk'])
def haveLearntCourse(request):
    if request.method=='GET':
        pk = request.GET.get('pk')
        userSearchResult = request.user.resultSet.filter(result__courseID=pk)
        if not userSearchResult:
            return JsonResponse({"status": 410, "msg": "You havn\'t chosen the course."})
        userSearchResult = userSearchResult[0]
        return JsonResponse({"status":200,"msg":"Success.","haveLearnt":userSearchResult.haveLearnt})
