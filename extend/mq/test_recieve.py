import pika

connect = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connect.channel()


def callback(ch, method, properties, body):
    print(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)  # 公平调度
channel.basic_consume("queue_op_logs", on_message_callback=callback)
print("Waiting for message")
channel.start_consuming()