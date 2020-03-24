# 单元测试脚本
'''
数据库从空开始
'''
import json
import requests


# api测试工具
class TestTool:

    @staticmethod
    def get(url, params, headers):
        try:
            res = requests.get("127.0.0.1:5000" + url, params=params, headers=headers)
            res = json.loads(res.content)
            assert True
            return res["data"]
        except Exception as e:
            print(e)
            assert False
