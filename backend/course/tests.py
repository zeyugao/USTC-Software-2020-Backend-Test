from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.http import HttpResponse, JsonResponse
import json
from django.contrib.auth import authenticate, get_user_model
from course.models import course, coursePrefix, courseResult


class CourseModelTests(TestCase):

    def setUp(self):
        userModel = get_user_model()
        userModel.objects.create_user(
            username="aaaaaaaa", password="pAs5W02D11", grade=1)
        userModel.objects.create_user(
            username="bbbbbbbb", password="pAs5W02D22", grade=2)
        userModel.objects.create_user(
            username="cccccccc", password="pAs5W02D33", grade=3)
        userModel.objects.create_user(
            username="dddddddd", password="pAs5W02D44", grade=4)

        course.objects.create(pk="BX0001", name="废理兴工纲要A1", grade="1")
        course.objects.create(pk="BX0002", name="废理兴工纲要A2", grade="2")
        course.objects.create(pk="BX0003", name="废理兴工纲要A3", grade="3")
        course.objects.create(pk="BX0004", name="废理兴工纲要A4", grade="4")
        course.objects.create(pk="BX0005", name="现代一教爆破技术A1", grade="2")
        course.objects.create(pk="BX0006", name="现代一教爆破技术A2", grade="3")
        course.objects.create(pk="BX0007", name="现代一教爆破技术B1", grade="2")
        course.objects.create(pk="BX0008", name="现代一教爆破技术B2", grade="3")
        course.objects.create(pk="GX0001", name="CWK思想概论", grade="3")
        course.objects.create(pk="GX0002", name="GZY主义辩证原理", grade="4")

        coursePrefix.objects.create(prefix=course.objects.filter(pk="BX0001")[0],
                                    suffix=course.objects.filter(pk="BX0002")[0])
        coursePrefix.objects.create(prefix=course.objects.filter(pk="BX0002")[0],
                                    suffix=course.objects.filter(pk="BX0003")[0])
        coursePrefix.objects.create(prefix=course.objects.filter(pk="BX0003")[0],
                                    suffix=course.objects.filter(pk="BX0004")[0])
        coursePrefix.objects.create(prefix=course.objects.filter(pk="BX0001")[0],
                                    suffix=course.objects.filter(pk="BX0005")[0])
        coursePrefix.objects.create(prefix=course.objects.filter(pk="BX0002")[0],
                                    suffix=course.objects.filter(pk="BX0006")[0])
        coursePrefix.objects.create(prefix=course.objects.filter(pk="BX0005")[0],
                                    suffix=course.objects.filter(pk="BX0006")[0])
        coursePrefix.objects.create(prefix=course.objects.filter(pk="BX0001")[0],
                                    suffix=course.objects.filter(pk="BX0007")[0])
        coursePrefix.objects.create(prefix=course.objects.filter(pk="BX0002")[0],
                                    suffix=course.objects.filter(pk="BX0008")[0])
        coursePrefix.objects.create(prefix=course.objects.filter(pk="BX0007")[0],
                                    suffix=course.objects.filter(pk="BX0008")[0])
        coursePrefix.objects.create(prefix=course.objects.filter(pk="GX0001")[0],
                                    suffix=course.objects.filter(pk="GX0002")[0])
        coursePrefix.objects.create(prefix=course.objects.filter(pk="BX0001")[0],
                                    suffix=course.objects.filter(pk="GX0001")[0])
        
    def teststream(self):
        r=json.loads(self.client.get('/course/result').content)["status"]
        self.assertEqual(r,406)
        #haven't login

        pl={"username":"aaaaaaaa","password":"pAs5W02D11"}
        r=self.client.post('/account/login',pl)
        self.assertEqual(json.loads(r.content)["status"],200)

        r=json.loads(self.client.get('/course/result').content)["total"]
        self.assertEqual(r,0)
        #normal


        r=json.loads(self.client.get('/course/choose?pk=BX0001').content)["status"]
        self.assertEqual(r,200)
        #choose

        r=json.loads(self.client.get('/course/result?gradeFilter=1').content)["total"]
        self.assertEqual(r,1)
        #gradeFilter

        r=json.loads(self.client.get('/course/choose?pk=BX0002').content)["status"]
        self.assertEqual(r,415)
        #choose grade too high

        
        pl={"grade":"2"}
        r=self.client.post('/account/setGrade',pl)
        self.assertEqual(json.loads(r.content)["status"],200)
        #upgrade

        r=json.loads(self.client.get('/course/result?gradeFilter=1').content)["total"]
        self.assertEqual(r,0)
        #gradeFilter

        r=json.loads(self.client.get('/course/result').content)["total"]
        self.assertEqual(r,1)
        #gradeFilter


        r=json.loads(self.client.get('/course/choose?pk=BX0002').content)["status"]
        self.assertEqual(r,416)
        #prefix lost


        r=json.loads(self.client.get('/course/choose?pk=BX0002').content)["requiredPk"][0]["pk"]
        self.assertEqual(r,"BX0001")
        #prefix lost

        r=json.loads(self.client.get('/course/setLearnStatus?pk=BX0001').content)["status"]
        self.assertEqual(r,200)
        #normal


        r=json.loads(self.client.get('/course/choose?pk=BX0002').content)["status"]
        self.assertEqual(r,200)
        #prefix lost


        pl={"grade":"3"}
        r=self.client.post('/account/setGrade',pl)
        self.assertEqual(json.loads(r.content)["status"],200)
        #upgrade


        r=json.loads(self.client.get('/course/choose?pk=BX0006').content)["requiredPk"][0]["pk"]
        self.assertEqual(r,"BX0002")
        #prefix lost


        r=len(json.loads(self.client.get('/course/choose?pk=BX0006').content)["requiredPk"])
        self.assertEqual(r,2)
        #normal

        r=json.loads(self.client.get('/course/choose?pk=BX2333').content)["status"]
        self.assertEqual(r,414)

        pl={"grade":"2"}
        r=self.client.post('/account/setGrade',pl)
        self.assertEqual(json.loads(r.content)["status"],200)
        #upgrade

        r=json.loads(self.client.get('/course/list').content)["total"]
        self.assertEqual(r,10)
        #list all
        r=json.loads(self.client.get('/course/list?grade=4').content)["total"]
        self.assertEqual(r,2)
        #grade

        r=json.loads(self.client.get('/course/list?gradeFilter=1').content)["total"]
        self.assertEqual(r,3)
        #gradeFilter
        
        r=json.loads(self.client.get('/course/exitCourse?pk=BX0001').content)["status"]
        self.assertEqual(r,413)
        #have learnt

        r=json.loads(self.client.get('/course/exitCourse?pk=BX0002').content)["status"]
        self.assertEqual(r,200)
        #normal

        r=json.loads(self.client.get('/course/exitCourse?pk=BX0003').content)["status"]
        self.assertEqual(r,410)
        #havn't choose

