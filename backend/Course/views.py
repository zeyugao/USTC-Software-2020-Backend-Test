from django.shortcuts import render
from Course.models import Course,ACRelationship,CCRelationship
from django.contrib.auth import get_user_model
from django.http import JsonResponse

Account = get_user_model()

# Create your views here.
def CourseExist(coursename):
    if len(Course.objects.filter(coursename = coursename)) == 0:
        return '1'#This course not exist
    else:
        return '0'#This course exist

#add course in system
def AddCourse(coursename,grade):
    if len(coursename) == 0 or coursename == None or grade <= 0 or grade > 4:
        return JsonResponse({'status':'001','error_msg':'Add course failed!Please input the corect coursename and grade'})
    elif CourseExist(coursename) == '0':
        return JsonResponse({'status':'002','error_msg':'Add course failed!This course has already existed'})
    course = Course.objects.create(coursename = coursename,grade = grade)
    return JsonResponse({'status':'000','error_msg':'Add course successful!The primary key of course is' + str(course.pk)})#return the primary key of the course

#delete course in system
def DeleteCourse(coursename):
    if len(coursename) == 0 or coursename == None:
        return JsonResponse({'status':'003','error_msg':'Delete course failed!Please input the corect coursename'})
    elif CourseExist(coursename) == '1':
        return JsonResponse({'status':'004','error_msg':'Delete course failed!This course does not exist'})
    course = Course.objects.get(coursename = coursename)
    course.delete()
    return JsonResponse({'status':'005','error_msg':'Delete course successful!'})

#list all course in the system
def ListAllCourse(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        backmsg = "Grade:      Course:\n"
        if len(courses) == 0:#There is no course information in system
            return JsonResponse({'status':'401','error_msg':'No course information in system'})
        for course in courses:
            backmsg = backmsg + str(course.grade) + "           " + course.coursename + "\n"
        return JsonResponse({'status':'400','error_msg':backmsg})

#account choose a course
def ChooseCourse(request):
    if request.method == 'POST':
        username = request.user
        primarykey = request.POST['pk']
        account = Account.objects.get(username = username)
        course = Course.objects.get(pk = primarykey)#choose course through its primary key
        ac = ACRelationship.objects.filter(course = course,account = account)
        if len(ac) != 0:
            if ac[0].finished == True:#This course has already been finished
                return JsonResponse({'status':'501','error_msg':'You have already finished this course'})
            elif ac[0].selection == True:#This course has already been chosen
                return JsonResponse({'status':'502','error_msg':'You have already selected this course'})
            else:
                ac[0].selection = True#choose the course
        else:
            ac = ACRelationship.objects.create(course = course,account = account,finished = False,selection = True)
        return JsonResponse({'status':'500','error_msg':'Choose course successful'})

#update if user has finished the course
def UpdateACRelationship(username,primarykey):
        account = Account.objects.get(username = username)
        course = Course.objects.get(pk = primarykey)#choose course through its primary key
        ac = ACRelationship.objects.get_or_create(course = course,account = account,finished = True,selection = False)
        return JsonResponse({'status':'600','error_msg':'Update successful'})

#quit course
def QuitCourse(request):
    if request.method == 'POST':
        username = request.user
        primarykey = request.POST['pk']
        account = Account.objects.get(username = username)
        course = Course.objects.get(pk = primarykey)#choose course through its primary key
        ac = ACRelationship.objects.filter(course = course,account = account)
        if len(ac) != 0:
            if ac[0].finished == True:#This course has already been finished
                return JsonResponse({'status':'701','error_msg':'You have already finished this course'})
            elif ac[0].selection == False:#This course has not been chosen
                return JsonResponse({'status':'702','error_msg':'You have not choosen this course'})
            else:
                ac[0].selection = False#choose the course
                return JsonResponse({'status':'700','error_msg':'Quit course successful'})
        else:
            ac = ACRelationship.objects.create(course = course,account = account,finished = False,selection = False)
        return JsonResponse({'status':'702','error_msg':'You have not choosen this course'})

#return the course that in user's grade
def ListGradeCourse(request):
    if request.method == 'GET':
        username = request.user
        account = Account.objects.get(username = username)
        grade = account.grade
        courses = Course.objects.all()
        backmsg = "Course in your grade:\n"
        for course in courses:
            if course.grade == grade:
                backmsg = backmsg + course.coursename + "\n"
        if backmsg == "Course in your grade:\n":
            return JsonResponse({'status':'801','error_msg':'No course in your grade'})
        else:
            return JsonResponse({'status':'800','error_msg':backmsg})

#List the course that user choose
def ListChosenCourse(request):
    if request.method == 'GET':
        username = request.user
        account = Account.objects.get(username = username)
        courses = Course.objects.all()
        backmsg = "Your chosen course:\n"
        for course in courses:
            acrelationship = ACRelationship.objects.filter(course = course,account = account)
            if len(acrelationship) != 0:
                if acrelationship[0].selection == True:
                    backmsg = backmsg + course.coursename + "\n"
        if backmsg == "Your chosen course:\n":
            return JsonResponse({'status':'901','error_msg':'You have not chosen any course'})
        else:
            return JsonResponse({'status':'900','error_msg':backmsg})

#add preparatory course
def AddCCRelationship(coursename,preparatorycoursename):
    if CourseExist(coursename) == '1' or CourseExist(preparatorycoursename) == '1':
        return JsonResponse({'status':'1001','error_msg':'Some courses not in system'})
    course = Course.objects.get(coursename = coursename)
    preparatorycourse = Course.objects.get(coursename = preparatorycoursename)
    CC = CCRelationship.objects.get_or_create(course = course,preparatorycourse = preparatorycourse)
    return JsonResponse({'status':'1000','error_msg':'Build relationship between two courses'})

#list a course's preparatory courses
def ListPreparatoryCourse(request):
    if request.method == 'POST':
        primarykey = request.POST['pk']
        course = Course.objects.get(pk = primarykey)
        preparatorycourses = CCRelationship.objects.filter(course = course)
        backmsg = "preparatory courses of this course:\n"
        if len(preparatorycourses) == 0:#no preparatory courses
            return JsonResponse({'status':'1101','error_msg':'This course have no preparatory courses'})
        for preparatorycourse in preparatorycourses:
            backmsg = backmsg + preparatorycourse.preparatorycourse.coursename + "\n"
        return JsonResponse({'status': '1100', 'error_msg': backmsg})
        