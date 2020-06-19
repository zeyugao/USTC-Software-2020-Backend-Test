def gradeFilterGET(func):
    def inner(request,*args,**kwargs):
        gradeFilter=request.GET.get('gradeFilter')
        if gradeFilter:
            filterArgs={"grade":request.user.grade}
        else:
            filterArgs={}
        return func(request,filterArgs,*args,**kwargs)
    return inner