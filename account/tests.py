from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.http import HttpResponse, JsonResponse
import json


class AccountModelTests(TestCase):
    def test_register(self):
        data1 = {"name": "1122","pwd": "abcd","re_pwd": "abcd"}
        # 注意名称要和veiws的request.POST.get()内容对应
        response = self.client.post('/account/register/', data1)
        # 注意首尾两个/不能丢
        self.assertEqual(json.loads(response.content)["key"], "402")
        # {"key": "402", "msg": "register successfully"}

        data2 = {"name": "1122", "pwd": "abcd", "re_pwd": "abcd"}
        response = self.client.post('/account/register/', data2)
        self.assertEqual(json.loads(response.content)["key"], "401")
        # {"key": "401", "msg": "the username exists"}

        data3 = {"name": "1133", "pwd": "abcd", "re_pwd": "abc"}
        response = self.client.post('/account/register/', data3)
        self.assertEqual(json.loads(response.content)["key"], "403")
        # {"key": "403", "msg": "please input the same password"}

        data4 = {"name": "1144", "pwd": "abcd", "re_pwd": ""}
        response = self.client.post('/account/register/', data4)
        self.assertEqual(json.loads(response.content)["key"], "404")
        # {"key": "404", "msg": "blank input is not allowed"}

    def test_login(self):
        register = self.client.post('/account/register/',
                {"name": "1234", "pwd": "abcd", "re_pwd": "abcd"})
        # 先建立一个账户

        data1 = {"name": "1234", "pwd": "abcd"}
        response = self.client.post('/account/login/', data1)
        self.assertEqual(json.loads(response.content)["key"], "501")
        # {"key": "501", "msg": "login successfully"}

        data2 = {"name": "12345", "pwd": "abcd"}
        response = self.client.post('/account/login/', data2)
        self.assertEqual(json.loads(response.content)["key"], "503")
        # {"key": "503", "msg": "username doesn't exist"}

        data3 = {"name": "1234", "pwd": "abc"}
        response = self.client.post('/account/login/', data3)
        self.assertEqual(json.loads(response.content)["key"], "502")
        # {"key": "502", "msg": "pwd error"}

    def test_logout(self):
        register = self.client.post('/account/register/',
                                    {"name": "1234", "pwd": "abcd", "re_pwd": "abcd"})
        login = self.client.post('/account/login/', {"name": "1234", "pwd": "abcd"})
        # 先注册并且登录

        response = self.client.post('/account/logout/')
        self.assertEqual(json.loads(response.content)["key"], "602")
        # {"key": "602", "msg": "logout successfully"}

        response = self.client.post('/account/logout/')
        self.assertEqual(json.loads(response.content)["key"], "601")
        # {"key": "601", "msg": "please login first"}


    def test_allcourse(self):
        register = self.client.post('/account/register/',
                                    {"name": "1234", "pwd": "abcd", "re_pwd": "abcd"})
        login = self.client.post('/account/login/', {"name": "1234", "pwd": "abcd"})
        # 先注册并且登录
        response = self.client.get('/account/allcourse/')
        # 注意是GET提交方式
        self.assertEqual(json.loads(response.content)["key"], "603")
        # {"key": "603", "msg": "Get all courses successfully"}


    def test_choose(self):
        register = self.client.post('/account/register/',
                                    {"name": "1234", "pwd": "abcd", "re_pwd": "abcd"})
        login = self.client.post('/account/login/', {"name": "1234", "pwd": "abcd"})
        # 先注册并且登录
        data1 = {"choice": "1234"}
        response = self.client.post('/account/choose/', data1)
        self.assertEqual(json.loads(response.content)["key"], "605")
        # {"key": "605", "msg": "choose course successfully"}

        data2 = {"choice": ""}
        response = self.client.post('/account/choose/', data2)
        self.assertEqual(json.loads(response.content)["key"], "604")
        # {"key": "604", "msg": "you didn't make a choice"}

    def test_mycourse(self):
        register = self.client.post('/account/register/',
                                    {"name": "1234", "pwd": "abcd", "re_pwd": "abcd"})
        login = self.client.post('/account/login/', {"name": "1234", "pwd": "abcd"})
        # 先注册并且登录
        response = self.client.get('/account/mycourse/')
        # 注意是GET提交方式
        self.assertEqual(json.loads(response.content)["key"], "606")
        # {"key": "606", "msg": "Get you courses successfully"}

    def test_delete(self):
        register = self.client.post('/account/register/',
                                    {"name": "1234", "pwd": "abcd", "re_pwd": "abcd"})
        login = self.client.post('/account/login/', {"name": "1234", "pwd": "abcd"})
        # 先注册并且登录
        data1 = {"delete": "1234"}
        response = self.client.post('/account/delete/', data1)
        self.assertEqual(json.loads(response.content)["key"], "607")
        # {"key": "607", "msg": "delete course successfully"}

        data2 = {"delete": ""}
        response = self.client.post('/account/choose/', data2)
        self.assertEqual(json.loads(response.content)["key"], "604")
        # {"key": "604", "msg": "you didn't make a choice"}


# Create your tests here.
