from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.http import HttpResponse, JsonResponse
import json
from django.contrib.auth import authenticate,get_user_model

class AccountModelTests(TestCase):

    def setUp(self):
        userModel=get_user_model()
        userModel.objects.create_user(username="aaaaaaaa",password="pAs5W02D11",grade=1)
        userModel.objects.create_user(username="bbbbbbbb",password="pAs5W02D22",grade=2)
        userModel.objects.create_user(username="cccccccc",password="pAs5W02D33",grade=3)
        userModel.objects.create_user(username="dddddddd",password="pAs5W02D44",grade=4)

    def testreg(self):
        pl={"username":"","password":"","grade":""}
        r=self.client.post('/account/register',pl)
        self.assertEqual(json.loads(r.content)["status"],400)
        #lost args.

        pl={"username":"aaaaaaaa","password":"nmsl123456","grade":"1"}
        r=self.client.post('/account/register',pl)
        self.assertEqual(json.loads(r.content)["status"],401)
        #username conflict

        pl={"username":"a__++bbccdd","password":"nmsl123456","grade":"1"}
        r=self.client.post('/account/register',pl)
        self.assertEqual(json.loads(r.content)["status"],401)
        #special symbols

        pl={"username":"eeeeeeeeeeeeeeeeeee333eeeeeeeeeeeeeeeeee","password":"nmsl123456","grade":"1"}
        r=self.client.post('/account/register',pl)
        self.assertEqual(json.loads(r.content)["status"],401)
        #long username

        pl={"username":"gzytqlmoe","password":"88888888","grade":"1"}
        r=self.client.post('/account/register',pl)
        self.assertEqual(json.loads(r.content)["status"],402)
        #easy pwd

        
        pl={"username":"gzytqlmoe","password":"flxg123456","grade":"9"}
        r=self.client.post('/account/register',pl)
        self.assertEqual(json.loads(r.content)["status"],403)
        #illegal grade

        pl={"username":"gzytqlmoe","password":"flxg123456","grade":"hhh"}
        r=self.client.post('/account/register',pl)
        self.assertEqual(json.loads(r.content)["status"],403)
        #illegal grade

        pl={"username":"gzytqlmoe","password":"flxg123456","grade":"4"}
        r=self.client.post('/account/register',pl)
        self.assertEqual(json.loads(r.content)["status"],200)
        #gdltql!

    def testlog(self):
        r=self.client.get('/account/logout')
        self.assertEqual(json.loads(r.content)["status"],406)
        #havn't login

        pl={"username":"aaaaaaaa","password":"pAs5W02D11"}
        r=self.client.post('/account/login',pl)
        self.assertEqual(json.loads(r.content)["status"],200)
        #ok

        pl={"username":"aaaaaaaa","password":"pAs5W02D11"}
        r=self.client.post('/account/login',pl)
        self.assertEqual(json.loads(r.content)["status"],405)
        #repeat


        r=self.client.get('/account/logout')
        self.assertEqual(json.loads(r.content)["status"],200)

        pl={"username":"aaaaaaaa","password":"acccc"}
        r=self.client.post('/account/login',pl)
        self.assertEqual(json.loads(r.content)["status"],407)


        pl={"username":"c++isthebestlanguage","password":"pAs5W02D11"}
        r=self.client.post('/account/login',pl)
        self.assertEqual(json.loads(r.content)["status"],401)

        pl={"username":"aaasscccee","password":"pAs5W02D11"}
        r=self.client.post('/account/login',pl)
        self.assertEqual(json.loads(r.content)["status"],407)

    def testchangepassword(self):
        pl={"oldPassword":"pAs5W02D11","newPassword":"pAs5W02D112"}
        r=self.client.post('/account/changePassword',pl)
        self.assertEqual(json.loads(r.content)["status"],406)
        #havn't login

        pl={"username":"aaaaaaaa","password":"pAs5W02D11"}
        r=self.client.post('/account/login',pl)
        self.assertEqual(json.loads(r.content)["status"],200)

        pl={"oldPassword":"pAs5W02D11","newPassword":"pAs5W02D11"}
        r=self.client.post('/account/changePassword',pl)
        self.assertEqual(json.loads(r.content)["status"],404)
        #unchanged password

        pl={"oldPassword":"pAs5W02D","newPassword":"pAs5W02D11"}
        r=self.client.post('/account/changePassword',pl)
        self.assertEqual(json.loads(r.content)["status"],409)
        #wrong old password

        pl={"oldPassword":"pAs5W02D11","newPassword":"pAs5W02D112"}
        r=self.client.post('/account/changePassword',pl)
        self.assertEqual(json.loads(r.content)["status"],200)

        pl={"oldPassword":"pAs5W02D112","newPassword":"pAs5W02D11"}
        r=self.client.post('/account/changePassword',pl)
        self.assertEqual(json.loads(r.content)["status"],200)
        #success


        pl={"oldPassword":"pAs5W02D11","newPassword":"pAs"}
        r=self.client.post('/account/changePassword',pl)
        self.assertEqual(json.loads(r.content)["status"],408)
        #easy password

        r=self.client.get('/account/logout')
        self.assertEqual(json.loads(r.content)["status"],200)
    
    def testsetgrade(self):
        pl={"grade":"1"}
        r=self.client.post('/account/setGrade',pl)
        self.assertEqual(json.loads(r.content)["status"],406)
        #havn't login


        pl={"username":"aaaaaaaa","password":"pAs5W02D11"}
        r=self.client.post('/account/login',pl)
        self.assertEqual(json.loads(r.content)["status"],200)


        pl={"grade":"4"}
        r=self.client.post('/account/setGrade',pl)
        self.assertEqual(json.loads(r.content)["status"],200)
        #normal


        pl={"grade":"xy"}
        r=self.client.post('/account/setGrade',pl)
        self.assertEqual(json.loads(r.content)["status"],403)
        #illegal grade


        pl={"grade":"0"}
        r=self.client.post('/account/setGrade',pl)
        self.assertEqual(json.loads(r.content)["status"],403)
        #illegal grade


        pl={"grade":"3.7"}
        r=self.client.post('/account/setGrade',pl)
        self.assertEqual(json.loads(r.content)["status"],403)
        #illegal grade