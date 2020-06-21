from django.views.generic.base import View
from django.http import JsonResponse
from django.forms.models import model_to_dict

from accounts.models import Stu
from accounts.models import Ke


class GetAllView(View):
    http_method_names = ['get']

    def get(self, request):
        allcourse = Ke.objects.all().order_by('pk')
        allcoursedict = [model_to_dict(course, fields=['pk', 'name', 'grade']) for course in allcourse]
        return JsonResponse({
            'code': 200,
            'msg': allcoursedict
        })

class GetPrivkeView(View):
    http_method_names = ['get']

    def get(self, request):
        if not request.user.is_authenticated():
            return JsonResponse({
                'code': 401,
                'msg': 'Login first'
            })
        privke = request.user.stu.ke_set.all().order_by('pk')
        privkedict = [model_to_dict(course, fields=['pk', 'name', 'grade']) for course in privke]
        return JsonResponse({
            'code': 200,
            'msg': privkedict
        })

class ElecKeView(View):
    http_method_names = ['get', 'post']

    def get(self, request):
        pass

    def post(self, request):
        if not request.user.is_authenticated():
            return JsonResponse({
                'code': 401,
                'msg': 'Login first'
            })
        kid = request.POST.get('kid')
        if Ke.objects.filter(pk = kid).exists():
            selectd_ke = Ke.objects.get(pk = kid)
            selectd_ke.stus.add(request.user.stu)
            selectd_ke.save()
            return JsonResponse({
                'code': 200,
                'msg': 'Elec Ke successfully'
            })
        return JsonResponse({
            'code': 404,
            'msg': 'Invalid kid'
        })
    
class DropKeView(View):
    http_method_names = ['get', 'post']

    def get(self, request):
        pass

    def post(self, request):
        if not request.user.is_authenticated():
            return JsonResponse({
                'code': 401,
                'msg': 'Login first'
            })
        kid = request.POST.get('kid')
        if Ke.objects.filter(pk = kid).exists():
            selectd_ke = Ke.objects.get(pk = kid)
            try:
                selectd_ke.stus.remove(request.user.stu)
            except ValueError:
                return JsonResponse({
                    'code': 404,
                    'msg': 'Invalid course status for user'
                })
            selectd_ke.save()
            return JsonResponse({
                'code': 200,
                'msg': 'Drop Ke successfully'
            })
        return JsonResponse({
            'code': 403,
            'msg': 'Invalid course id'
        })