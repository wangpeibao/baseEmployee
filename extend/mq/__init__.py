import json

import pika


class Rmq:
    def __init__(self, app=None):
        self.app = app
        self.connect = None
        self.channel = None

    def init_app(self, app):  # 建立连接
        self.app = app
        self.connect = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.app.config["MQ_LINK"],
            heartbeat=0  # 不主动断开连接
        ))
        self.channel = self.connect.channel()
        # 声明持续化队列名称
        self.init_send_log()

    def init_send_log(self):  # 自定义的操作日志生产者(业务简单，直连交换机即可，持续化存储)
        try:
            self.channel.exchange_declare(
                exchange="exchange_op_logs",
                durable=True,
                exchange_type="direct"
            )
        except Exception as e:
            print("操作日志交换机已存在", e)
        try:
            self.channel.queue_declare(
                queue="queue_op_logs",
                durable=True
            )
            self.channel.queue_bind(
                exchange="exchange_op_logs",
                queue="queue_op_logs",
                routing_key="op_logs"
            )
        except Exception as e:
            print("操作日志队列已存在", e)

    def send_log(self, body):
        self.channel.basic_publish(
            exchange="exchange_op_logs",
            routing_key="op_logs",
            body=json.dumps(body),
            properties=pika.BasicProperties(delivery_mode=2)
        )

