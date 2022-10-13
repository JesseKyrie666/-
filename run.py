# coding=utf-8


import logging
from engine import *
import json
from main import run_task
from check_retry import check_total
from add_imgs import add_img_big
from kafka import KafkaConsumer
import time
from baoyou import baoyou_001
import redis
import requests
from consumer import RBMQ_Consumer
import socket
import os

log_format = '%(levelname)s <=== (%(asctime)s) ====> %(message)s'
logging.basicConfig(
    filename=LOG_SUCCESS,
    format=log_format,
    level=logging.WARNING
)


def send_time(task, margs):
    if margs == "start":
        msg = {
            "id": task['id'],
            "startTime": int(time.time()) * 1000,
        }
        resp = requests.post(url='http://192.168.10.230:9300/api/bigTile/updateStatus', json=msg)
    else:
        msg = {
            "id": task['id'],
            "endTime": int(time.time()) * 1000,
        }
        resp = requests.post(url='http://192.168.10.230:9300/api/bigTile/updateStatus', json=msg)


def heart_beat(speed=0):
    # 获取当前内网ip
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('192.168.10.230', 80))
    names = s.getsockname()
    mip = names[0]
    pid = os.getpid()
    data_send = '{}_{}'.format(mip, pid)
    heart_beat = {
        'key': 'google_map_server:' + data_send,
        'ip': mip,
        'rate': int(speed),
        # 格式化输出时间
        'time': int(time.time())
    }
    rnn = redis.Redis(host='192.168.10.230', port=6379, db=0, decode_responses=True)
    rnn.hset(heart_beat['key'], "ip", heart_beat['ip'])
    rnn.hset(heart_beat['key'], "rate", heart_beat['rate'])
    rnn.hset(heart_beat['key'], "time", heart_beat['time'])
    # 设置心跳时间
    rnn.expire(heart_beat['key'], 600)
    print("心跳成功啦")


def check_data(task):
    while True:
        code = check_total(task)
        if code:
            break
        # 开始重试爬虫数据


def change_status(_id, status):
    try:
        import requests
        url = 'http://192.168.10.230:9300/api/bigTile/updateStatus'
        msg = {
            "id": _id,
            "status": status
        }
        requests.post(url=url, json=msg)
    except:
        pass


def start_consumer():
    # 获取到一个消息
    consumer = KafkaConsumer(KAFKA_QUEUE, bootstrap_servers='192.168.10.230:9092', group_id='cleaner')
    msg = next(consumer)
    hit = msg.value.decode('utf-8')
    return (hit, consumer)

def run(task_msg):
    start_time = int(time.time())
    hit = task_msg
    logging.warning('<===============kafka 消费者已连接================>')
    print("接受到的消息", hit)
    # ================================>启动任务爬虫<===================================
    task = hit
    task_id = task['id']
    # 修改mysql任务状态todo
    change_status(task_id, 2)
    logging.warning('<===============已经接受到任务{}================>'.format(task_id))
    print('-----------------')
    print("=========爬虫已启动=========")
    logging.warning('<===============爬虫已启动================>')
    print("=========启动爬虫成功=========")
    task_num = 2500
    send_time(task, margs="start")
    city_code = task["cityId"]
    pushDir_part = city_code + "/" + str(task["pushDir"]) + '/'
    print("保存的提交文件夹为", pushDir_part)
    print("任务id为", task_id)
    # input("请确认提交文件夹是否正确，按回车键继续")
    task['pushDir_use'] = pushDir_part
    baoyou_001()
    run_task(task_num, city_code, task)
    logging.warning('<===============爬虫已结束================>')
    print("=========爬虫已结束=========")
    # # 开始校验数据
    logging.warning('<===============开始校验任务数据总量================>')
    check_data(task)  # 单线程处理数据超时异常
    logging.warning('<===============校验任务数据总量结束================>')
    logging.warning('<===============下载任务完成================>')
    print("=========下载任务完成=========")
    img_mission_async(task)
    end_time = int(time.time())
    speed = int(2500 / (end_time - start_time))
    heart_beat(speed)
    return


def img_mission_async(task):
    logging.warning('<===============开始拼接瓦片================>')
    # # 拼接瓦片开始
    add_json = {'x_start': task['xStart'], 'y_start': task['yStart'], 'city_id': task['cityId'], 'task_id': task['id'],
                'pushDir': task['pushDir']}
    add_status = add_img_big(add_json)
    if not add_status:
        # 发送拼接失败消息todo
        logging.warning('<===============图片拼接异常================>')
        print('<===============图片拼接异常================>')
        change_status(task['id'], -1)
    else:
        # 发送拼接成功消息todo
        logging.warning('<===============拼接瓦片成功================>')
        print('<===============拼接瓦片成功================>')
        change_status(task['id'], 3)
    # 确认提交任务完成
    send_time(task, margs="end")


def main():
    start_time = int(time.time())
    # 从rabbitmq获取消息
    rbmq_host = '192.168.10.230'
    rbmq = RBMQ_Consumer(rbmq_host, RABBITMQ_QUEUE, run)
    rbmq.start()


if __name__ == '__main__':
    main()
