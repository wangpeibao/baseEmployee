# 单元测试脚本
'''
数据库从空开始
'''
import json
import requests


# api测试工具
class TestTool:

    @staticmethod
    def get(url, params=(), headers=None):
        try:
            res = requests.get(url, params=params, headers=headers)
            res = json.loads(res.content)
            return res
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def post(url, data=(), headers=None):
        try:
            res = requests.post("http://127.0.0.1:5000" + url, data=data, headers=headers)
            res = json.loads(res.content)
            return res
        except Exception as e:
            print(e)
            return None

