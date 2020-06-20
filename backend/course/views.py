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


@methodFilter(['GET'])
@loginPermission
@userGETFilter([('result__grade__lte', 'gradeFilter', 'grade')])
def listUserResult(request, userFilter):
    if request.method == 'GET':
        result = [{"pk": i.result.courseID,
                   "course": i.result.name,
                   "haveLearnt": i.haveLearnt
                   } for i in request.user.resultSet.all().filter(**userFilter)]
        return JsonResponse({"status": 200, "total": len(result), "course": result})


@methodFilter(['GET'])
@loginPermission
@requiredArgumentGET(['pk'])
def setLearnStatus(request):
    if request.method == 'GET':
        pk = request.GET.get('pk')

        # Check if the course has been chosen.
        userSearchResult = request.user.resultSet.filter(result__courseID=pk)
        if not userSearchResult:
            return JsonResponse({"status": 416, "msg": "You havn\'t chosen the course."})

        # Check if the chosen course has been learnt.
        userSearchResult = userSearchResult[0]
        if userSearchResult.haveLearnt:
            return JsonResponse({"status": 416, "msg": "You have learnt the course."})

        # Update learning status.
        userSearchResult.haveLearnt = True
        userSearchResult.save()
        return JsonResponse({"status": 200, "msg": "Update the learning status successfully."})


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
            return JsonResponse({"status": 413, "msg": "You\'ve chosen the course."})

        # Check if the course exists.
        searchResult = course.objects.filter(courseID=pk)
        if not searchResult:
            return JsonResponse({"status": 414, "msg": "The course doesn\'t exists."})
        searchResult = searchResult[0]

        # Check grade.
        if searchResult.grade > request.user.grade:
            return JsonResponse({"status": 414, "msg": "Not for your grade."})

        # Check if all prefix have been achieved.
        prefixList = [i.prefix.courseID for i in searchResult.prefixSet.all()]
        requiredPrefix = []
        for i in prefixList:
            if not ((i, True) in userSearchResult):
                requiredPrefix.append({"pk": i})
        if requiredPrefix:
            return JsonResponse({"status": 415, "msg": "You haven\'t met all requirement.", "requiredPk": requiredPrefix})

        # Choose course, write it in result.
        resultInstance = courseResult(
            learner=request.user, result=searchResult, haveLearnt=False)
        resultInstance.save()
        return JsonResponse({"status": 200, "msg": "Choose course successfully."})


@methodFilter(['GET'])
@loginPermission
@requiredArgumentGET(['pk'])
def exitCourse(request):
    if request.method == 'GET':
        pk = request.GET.get('pk')

        # Check if the course has been chosen.
        userSearchResult = request.user.resultSet.filter(result__courseID=pk)
        if not userSearchResult:
            return JsonResponse({"status": 416, "msg": "You havn\'t chosen the course."})

        # Check if the chosen course has been learnt.
        userSearchResult = userSearchResult[0]
        if userSearchResult.haveLearnt:
            return JsonResponse({"status": 416, "msg": "You have learnt the course."})

        # Exit the course.
        userSearchResult.delete()
        return JsonResponse({"status": 200, "msg": "Exit the course successfully."})


@methodFilter(['GET'])
@userGETFilter([('grade__lte', 'gradeFilter', 'grade')])
@normalGETFilter([('grade', 'grade', 'grade')])
def listAllCourse(request, userFilter, normalFilter):
    if request.method == 'GET':
        grade = request.GET.get('grade')
        if grade:
            try:
                gradeValidation(grade)
            except ValidationError as e:
                return JsonResponse({"status": 417, "msg": e.messages})
        print(userFilter)
        print(normalFilter)
        result = course.objects.all().filter(**userFilter).filter(**normalFilter)
        result = [{"pk": i.courseID, "course": i.name} for i in result]

        return JsonResponse({"status": 200, "total": len(result), "course": result})


@methodFilter(['GET'])
@requiredArgumentGET(['pk'])
def listPrefix(request):
    if request.method == 'GET':
        pk = request.GET.get('pk')
        searchResult = course.objects.filter(courseID=pk)
        if not searchResult:
            return JsonResponse({"status": 414, "msg": "The course doesn\'t exists."})
        result = [{
            "pk": i.prefix.courseID,
            "course": i.prefix.name} for i in searchResult[0].prefixSet.all()]
        return JsonResponse({"status": 200, "total": len(result), "course": result})

@methodFilter(['GET'])
@loginPermission
@requiredArgumentGET(['pk'])
def haveLearntCourse(request):
    if request.method=='GET':
        pk = request.GET.get('pk')
        userSearchResult = request.user.resultSet.filter(result__courseID=pk)
        if not userSearchResult:
            return JsonResponse({"status": 416, "msg": "You havn\'t chosen the course."})
        userSearchResult = userSearchResult[0]
        return JsonResponse({"status":200,"haveLearnt":userSearchResult.haveLearnt})
