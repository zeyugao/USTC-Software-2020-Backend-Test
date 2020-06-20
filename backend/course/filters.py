from django.http import JsonResponse

def userGETFilter(filterArgs):
    def outer(func):
        def inner(request,*args,**kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({"status": 405,"msg": "Please login first."})
            filterResult={}
            for i in filterArgs:
                filterFlag=request.GET.get(i[1])
                if filterFlag=="1":
                    filterResult[i[0]]=getattr(request.user,i[2])
            return func(request,userFilter=filterResult,*args,**kwargs)
        return inner
    return outer

def commonGETFilter(filterArgs):
    def outer(func):
        def inner(request,*args,**kwargs):
            filterResult={}
            for i in filterArgs:
                filterValue=request.GET.get(i[1])
                if filterValue:
                    filterResult[i[0]]=filterValue
            return func(request,commonFilter=filterResult,*args,**kwargs)
        return inner
    return outer




