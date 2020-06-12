from django.views.generic.base import View
from django.http import JsonResponse
from django.forms.models import model_to_dict

from accounts.models import Stu
from accounts.models import Ke


class GetAllView(View):
    http_method_names = ['get']

    def get(self, request):
        allcourse = Ke.objects.all().order_by('kid')
        allcoursedict = [model_to_dict(course, fields=['id', 'name', 'grade']) for course in allcourse]
        return JsonResponse({
            'code': 200,
            'msg': allcoursedict
        })

class GetPrivkeView(View):
    http_method_names = ['get']

    def get(self, request):
        # privke = request.