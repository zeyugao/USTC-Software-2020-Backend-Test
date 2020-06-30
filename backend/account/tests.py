from django.test import TestCase,Client
from django.urls import reverse
from account.models import Account
import json

# Create your tests here.
class AccountTest(TestCase):
    def setUp(self):
        Account.objects.create_user(username = 'PB18000001',password = '123456',grade = 2)

    def test_Register(self):
        case1 = {'username':'PB18000002','password':'123456','grade':2}
        case2 = {'username':'PB180000','password':'123456','grade':2}
        case3 = {'username':'PB18000002','password':'','grade':2}
        case4 = {'username':'PB18000002','password':'<123456>','grade':4}
        case5 = {'username':'PB18000001','password':'123456','grade':2}
        case6 = {'username':'PB18000002','password':'123456','grade':6}
        self.client = Client()
        print('Test of register')
        response = self.client.post(reverse('account:register'),case5)
        self.assertEqual(json.loads(response.content)['status'],301)#account has already existed
        response = self.client.post(reverse('account:register'),case3)
        self.assertEqual(json.loads(response.content)['status'],302)#username or password is blank
        response = self.client.post(reverse('account:register'),case2)
        self.assertEqual(json.loads(response.content)['status'],303)#username is invalid,please use student ID
        response = self.client.post(reverse('account:register'),case4)
        self.assertEqual(json.loads(response.content)['status'],304)#passward is invalid,only letters,numbers and underline can be used.Make sure the length of it between 6 and 20
        response = self.client.post(reverse('account:register'),case6)
        self.assertEqual(json.loads(response.content)['status'],305)#grade is invalid,only 1 to 4 is accepted
        response = self.client.post(reverse('account:register'),case1)
        self.assertEqual(json.loads(response.content)['status'],300)#Register successful

    def test_Login_Logout(self):
        case1 = {'username':'PB18000001','password':'123456'}
        case2 = {'username':'PB18000003','password':'123456'}
        case3 = {'username':'PB18000001','password':''}
        case4 = {'username':'PB18000001','password':'123456789'}
        self.client = Client()
        print('Test of login')
        response = self.client.post(reverse('account:login'),case2)
        self.assertEqual(json.loads(response.content)['status'],201)#account is not exist
        response = self.client.post(reverse('account:login'),case3)
        self.assertEqual(json.loads(response.content)['status'],202)#username or password is blank
        response = self.client.post(reverse('account:login'),case4)
        self.assertEqual(json.loads(response.content)['status'],203)#Password is wrong
        response = self.client.post(reverse('account:login'),case1)
        self.assertEqual(json.loads(response.content)['status'],200)#Login successful
        print('Test of logout')
        response = self.client.get(reverse('account:logout'))
        self.assertEqual(json.loads(response.content)['status'],100)#Logout successful
        