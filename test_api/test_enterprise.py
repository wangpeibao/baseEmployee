# 测试企业相关接口

import unittest

from app import create_app


class TestEnterprise(unittest.TestCase):
    login_url = "/app_api/auth/login"
    create_url = "/app_api/enterprise/create_enterprise"
    update_url = "/app_api/enterprise/update_enterprise_info"
    phone = "15620011759"
    passwd = "123456"

    headers = {
        "Token": None,
        "AccountID": None,
        "EnterpriseID": None
    }

    def setUp(self):
        self.app = create_app("test")
        self.client = self.app.test_client()
        res = self.client.post(
            self.login_url,
            data={
                "phone": self.phone,
                "passwd": self.passwd
            }
        ).json
        self.headers["Token"] = res["data"]["app_token"]
        self.headers["AccountID"] = res["data"]["object_id"]

    def test_01_create_enterprise_success(self):
        res = self.client.post(
            self.create_url,
            data={
                "name": "王沛宝的公司"
            },
            headers=self.headers
        ).json
        self.headers["EnterpriseID"] = res["data"]["enterprise_id"]
        self.assertEqual(res["code"], 200)

    def test_02_create_enterprise_name_has(self):
        res = self.client.post(
            self.create_url,
            data={
                "name": "王沛宝的公司"
            },
            headers=self.headers
        ).json
        self.assertEqual(res["code"], -1)

    def test_03_update_enterprise_info_fail(self):
        self.client.post(
            self.create_url,
            data={
                "name": "王沛宝的公司1"
            },
            headers=self.headers
        )
        res = self.client.post(
            self.update_url,
            data={
                "name": "王沛宝的公司1"
            },
            headers=self.headers
        ).json
        self.assertEqual(res["code"], -1)

    def test_04_update_enterprise_info_success(self):
        res = self.client.post(
            self.update_url,
            data={
                "name": "王沛宝的公司2"
            },
            headers=self.headers
        ).json
        self.assertEqual(res["code"], 200)



