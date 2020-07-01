from django.test import TestCase,Client
from Course.models import Course,ACRelationship,CCRelationship
from django.urls import reverse
from account.models import Account
from Course import views
import json
# Create your tests here.

class CoureTest(TestCase):
    def setUp(self):
        Account.objects.create_user(username = 'PB18000001',password = '123456',grade = 2)
        views.AddCourse('Math A1',1)
        views.AddCourse('Math A2',1)
        views.AddCourse('Math A3',2)
        views.AddCourse('Program C',1)
        views.AddCourse('Data Structure',2)
        views.AddCourse('Algebraic Structure',1)
        views.AddCourse('Graph Theory',2)
        views.AddCourse('Mathematical Logic',2)
        views.AddCourse('Artificial Intelligence',3)
        views.AddCourse('Computer System',2)
        views.AddCourse('Computer Network',3)
        views.UpdateACRelationship('PB18000001',primarykey = 1)#student have already learn the course
        views.UpdateACRelationship('PB18000001',primarykey = 2)
        views.UpdateACRelationship('PB18000001',primarykey = 4)
        views.UpdateACRelationship('PB18000001',primarykey = 6)
        views.AddCCRelationship('Math A2','Math A1')
        views.AddCCRelationship('Math A3','Math A1')
        views.AddCCRelationship('Math A3','Math A2')
        views.AddCCRelationship('Data Structure','Program C')
        views.AddCCRelationship('Graph Theory','Algebraic Structure')
        views.AddCCRelationship('Mathematical Logic','Algebraic Structure')
        views.AddCCRelationship('Mathematical Logic','Graph Theory')
        views.AddCCRelationship('Artificial Intelligence','Math A1')
        views.AddCCRelationship('Artificial Intelligence','Math A2')
        views.AddCCRelationship('Computer System','Program C')
        views.AddCCRelationship('Computer System','Data Structure')
        views.AddCCRelationship('Computer Network','Graph Theory')
        views.AddCCRelationship('Computer Network','Data Structure')

    def test_ListAllCourse(self):
        self.client = Client()
        print('Test of list all courses')
        response = self.client.get(reverse('Course:listAllCourse'))
        self.assertEqual(json.loads(response.content)['status'],'400')
        print(json.loads(response.content)['error_msg'])#print all courses

    def test_ChooseCourse_and_QuitCourse(self):
        self.client = Client()
        print('Test of choose course')
        account = self.client.post(reverse('account:login'),{'username':'PB18000001','password':'123456'})
        response = self.client.post(reverse('Course:chooseCourse'),{'pk':1})
        self.assertEqual(json.loads(response.content)['status'],'501')#have already finished this course
        response = self.client.post(reverse('Course:chooseCourse'),{'pk':3})
        self.assertEqual(json.loads(response.content)['status'],'500')#Choose course successful
        response = self.client.post(reverse('Course:chooseCourse'),{'pk':3})
        self.assertEqual(json.loads(response.content)['status'],'502')#have already selected this course
        print('Test of quit course')
        response = self.client.post(reverse('Course:quitCourse'),{'pk':1})
        self.assertEqual(json.loads(response.content)['status'],'701')#have already finished this course
        response = self.client.post(reverse('Course:quitCourse'),{'pk':5})
        self.assertEqual(json.loads(response.content)['status'],'702')#have not choosen this course
        response = self.client.post(reverse('Course:quitCourse'),{'pk':3})
        self.assertEqual(json.loads(response.content)['status'],'700')#Quit course successful
        self.client.get(reverse('account:logout'))

    def test_ListGradeCourse(self):
        self.client = Client()
        print('Test of list courses in the grade of account')
        account = self.client.post(reverse('account:login'),{'username':'PB18000001','password':'123456'})
        response = self.client.get(reverse('Course:listGradeCourse'))
        self.assertEqual(json.loads(response.content)['status'],'800')
        print(json.loads(response.content)['error_msg'])#print all courses in account's grade
        self.client.get(reverse('account:logout'))

    def test_ListChosenCourse(self):
        self.client = Client()
        print('Test of list courses choosen by the account')
        account = self.client.post(reverse('account:login'),{'username':'PB18000001','password':'123456'})
        self.client.post(reverse('Course:chooseCourse'),{'pk':3})
        self.client.post(reverse('Course:chooseCourse'),{'pk':5})
        self.client.post(reverse('Course:chooseCourse'),{'pk':7})
        response = self.client.get(reverse('Course:listChosenCourse'))
        self.assertEqual(json.loads(response.content)['status'],'900')
        print(json.loads(response.content)['error_msg'])#print all choosen courses
        self.client.get(reverse('account:logout'))

    def test_ListPreparatoryCourse(self):
        self.client = Client()
        print('Test of list all preparatory courses of one course')
        response = self.client.post(reverse('Course:listPreparatoryCourse'),{'pk':3})
        self.assertEqual(json.loads(response.content)['status'],'1100')
        print(json.loads(response.content)['error_msg'])#print all preparatory courses

