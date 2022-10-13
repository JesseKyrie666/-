# coding=utf-8

import pickle
import time
import pika
import json

class RBMQ_Consumer:
    def __init__(self,host,queue_name,new_func):
        queue_host = host
        self.QUEEUE_NAME = queue_name
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=queue_host, port=5672))
        self.channel = connection.channel()
        self.channel.queue_declare(queue=self.QUEEUE_NAME, durable=True)
        # 设置只接受一条消息
        self.channel.basic_qos(prefetch_count=1)
        self.new_func = new_func
    def callback(self, ch, method, properties, body):
        if body:
            # msg = pickle.loads(body)
            msg = json.loads(body)
            self.new_func(msg)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            pass
    def start(self):
        self.channel.basic_consume(queue=self.QUEEUE_NAME,
                              auto_ack=False,
                              on_message_callback=self.callback)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close(self):
        self.channel.close()
