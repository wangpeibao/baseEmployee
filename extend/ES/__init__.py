# 与elasticsearch交互

from elasticsearch import Elasticsearch


class ESClient(object):
    def __init__(self, app=None):
        self.client = None
        self.app = app

    def init_app(self, app):
        self.app = app
        self.client = Elasticsearch(hosts=[self.app.config["ES_URI"]])
        if not self.client.ping():
            raise ConnectionError

    def query_op_logs(self, enterprise_id, page=1, manager_id=None, platform=None, module=None, version=None,
                      start=None, end=None):
        must_body = [{"term": {"enterprise_id": enterprise_id}}]
        if manager_id is not None:
            must_body.append({"term": {"manager_id": manager_id}})
        if platform is not None:
            must_body.append({"term": {"platform": platform}})
        if module is not None:
            must_body.append({"term": {"module": module}})
        if version is not None:
            must_body.append({"term": {"version": version}})
        if start and end:
            must_body.append({"range": {"op_time": {"gte": start, "lte": end}}})
        query_body = {
            "query": {"bool": {"must": must_body}}
        }
        result = self.client.search(index="op_logs", body=query_body, from_=(page - 1) * 10, size=10)
        print(result)

