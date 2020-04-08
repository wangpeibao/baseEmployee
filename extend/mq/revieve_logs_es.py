# 从消息队列中接受数据并存储到ES中
import json

import pika
from elasticsearch import Elasticsearch

mq_status = True  # 消息队列连接状态
es_status = True  # es服务连接状态

connect = None
try:
    connect = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
except Exception as e:
    print(e)
    mq_status = False

# es配置
client = Elasticsearch(hosts=[{"host": "172.17.0.1", "port": 9200}])
if not client.ping():
    es_status = False
else:
    settings = {
        "mappings": {
            "members": {
                "dynamic": "strict",
                "properties": {
                    "platform": {"type": "integer"},
                    "version": {"type": "text"},
                    "manager_id": {"type": "integer"},  # 根据人员主键数据类型
                    "enterprise_id": {"type": "integer"},  # 根据人员主键数据类型
                    "module": {"type": "integer"},
                    "title": {"type": "text"},
                    "content": {"type": "text"},
                    "op_time": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"}
                }
            }
        }
    }
    if not client.indices.exists(index="op_logs"):
        client.indices.create(index="op_logs", body=settings, ignore=400)


def callback(ch, method, properties, body):
    try:
        body = str(body, encoding="utf8")
        body = json.loads(body)
    except Exception as e:
        print(e)
    # 存储日志
    try:
        client.index(index="op_logs", body=body)
    except Exception as e:
        print(e)
    ch.basic_ack(delivery_tag=method.delivery_tag)


if mq_status and es_status:
    channel = connect.channel()
    channel.basic_qos(prefetch_count=1)  # 公平调度
    channel.basic_consume("queue_op_logs", on_message_callback=callback)
    print("start OK!")
    channel.start_consuming()

