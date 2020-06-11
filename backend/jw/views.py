from django.views.generic.base import View
from django.http import JsonResponse


from accounts.models import Stu
from accounts.models import Ke


class GetAllView(View):
    http_method_names = ['get']

    def get(self, request):
        Ke.objects.all() # ?