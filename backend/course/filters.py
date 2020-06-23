from django.http import JsonResponse

'''
    To add extra filter rule to the function according to the parameters.
    Ignore the rule when the correspond url parameter mismatches.
    This filter is linked with the attribute of users, so it need user to login first.

    The filterArgs accepts a list of rule in tuples, which should be in such format:
        [(filter condition:<str>, url parameter:<str>, user attribute:<str>) , ... ]
    And only when the url parameter exists, the filter will work.

    For example, if you want to filter the recode, where:
        course.grade <= user.grade
    Then you can use it like this:
        @userGETFilter([
            ('grade__lte','gradeFilter','grade')
        ])
        def function(request,userFilter):
            ......
            course.objects.filter(**userFilter)
            ......
        
    Only when the parameter 'gradeFilter' in url equal to 1,the decorater will add a filter 
    in userFilter.
    if the url parameter 'gradeFilte' doesn't exist or not equal to 1, then this rule will 
    be ignored.
'''
def userGETFilter(filterArgs):
    def outer(func):
        def inner(request,*args,**kwargs):
            filterResult={}
            for i in filterArgs:
                filterFlag=request.GET.get(i[1])
                if filterFlag=="1":
                    if not request.user.is_authenticated:
                        return JsonResponse({"status": 405,"msg": "Please login first."})
                    filterResult[i[0]]=getattr(request.user,i[2])
            return func(request,userFilter=filterResult,*args,**kwargs)
        return inner
    return outer

'''
    Too add normal filter rule to function according to the parameters.
    Ignore the rule when the correspond url parameter mismatches.

    The filterArgs accepts a list of rule in tuples, which should be in such format:
        [(filter condition:<str>, url parameter:<str>) , ... ]
    And only when the url parameter exists, the filter will work.

    For example, if user want to list the course in specific grade, or get the record where:
        course.record == given grade,
    
    Then you can use it like this:

        @normalGETFilter([
            ('grade__lte','grade')
        ])
        def function(request,normalFilter):
            ......
            course.objects.filter(**normalFilter)
            ......
        
    Only when the parameter 'grade' in url exists,the decorater will add a filter in 
    normalFilter.
    if the url parameter 'gradeFilte' doesn't exist, then this rule will be ignored.

    Notice:
    This decorator can work together with userGETFilter.
'''
def normalGETFilter(filterArgs):
    def outer(func):
        def inner(request,*args,**kwargs):
            filterResult={}
            for i in filterArgs:
                filterValue=request.GET.get(i[1])
                if filterValue:
                    filterResult[i[0]]=filterValue
            return func(request,normalFilter=filterResult,*args,**kwargs)
        return inner
    return outer




