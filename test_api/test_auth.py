'''
注册登录接口
'''
import json

from app import create_app, db

import unittest


class TestRegisterLogin(unittest.TestCase):
    register_url = "/app_api/auth/register"
    login_url = "/app_api/auth/login"
    phone1 = "15620011759"
    passwd1 = "123456"

    def setUp(self):
        self.app = create_app("test")
        db.create_all()
        self.client = self.app.test_client()

    def test_01_register_success(self):
        res = self.client.post(
            self.register_url,
            data={
                "phone": self.phone1,
                "name": "测试",
                "passwd": self.passwd1
            }
        ).json
        self.assertEqual(res["code"], 200)

    def test_02_register_repeat(self):
        res = self.client.post(
            self.register_url,
            data={
                "phone": self.phone1,
                "name": "测试",
                "passwd": self.passwd1
            }
        ).json
        self.assertEqual(res["code"], -1)

    def test_03_login_success(self):
        res = self.client.post(
            self.login_url,
            data={
                "phone": self.phone1,
                "passwd": self.passwd1
            }
        ).json
        print(res["data"])
        self.assertEqual(res["code"], 200)

    def test_04_login_fail(self):
        res = self.client.post(
            self.login_url,
            data={
                "phone": self.phone1,
                "passwd": self.passwd1 + "123"
            }
        ).json
        print(res["data"])
        self.assertEqual(res["code"], -1)
