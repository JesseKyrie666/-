# coding=utf-8


import os
from concurrent.futures import ThreadPoolExecutor
from engine import *
from spider import Spider
import logging


log_format = '%(levelname)s <=== (%(asctime)s) ====> %(message)s'
logging.basicConfig(
    filename=LOG_SUCCESS,
    format=log_format,
    level=logging.INFO
)
# uri = 'https://mts0.google.com/vt/lyrs=r@189000000&hl=en&src=app&x={}&y={}&z={}&s=Gal&apistyle=s.t:1%7Cs.e:l.t%7Cp.v:off,s.t:2%7Cs.e:l%7Cp.v:off,s.t:2%7Cs.e:g%7Cp.v:off,s.t:3%7Cs.e:l.t%7Cp.v:off,s.t:5%7Cs.e:g%7Cp.v:off,s.t:5%7Cs.e:l.t%7Cp.v:off,s.t:6%7Cs.e:l.t%7Cp.v:off,s.t:6%7Cs.e:g%7Cp.v:off,s.t:33%7Cs.e:l%7Cp.v:off,s.t:35%7Cs.e:l%7Cp.v:off,s.t:49%7Cs.e:l.i%7Cp.v:off,s.t:66%7Cs.e:l.i%7Cp.v:off,s.t:66%7Cs.e:l.t%7Cp.v:off'

def single(i):
    url = uri.format(i, 0)
    img_name = SAVE_DIR + str(i) + '_' + str(0) + '.png'
    Spider().request_url(url, img_name, PROXIES, TIMEOUT)

def save_error_log(url):
    with open(LOG_ERROR,'a+',encoding='utf8') as s:
        s.write("请求错误"+url+'\n')

def single_task(position,city_code,task):
    # x y
    if position:
        x = position[0]
        y = position[1]
        z = 18
        url = uri.format(x, y, 18)
        img_name_part = str(y)+'.png'
        # 生成瓦片piece目录
        piece_dir = SAVE_DIR.format(city_code)+task['pushDir']+"/piece/"
        if not os.path.exists(piece_dir):
            os.mkdir(piece_dir)
        # 生成层级
        level_dir = piece_dir+'18/'
        if not os.path.exists(level_dir):
            os.mkdir(level_dir)
        saver_dir = level_dir + '{}/'.format(x)
        # print("生成的x目录为：",saver_dir)
        if not os.path.exists(saver_dir):
            os.mkdir(saver_dir)
        img_name = saver_dir+img_name_part
        # 更改任务瓦片的存储路径
        code = Spider().request_with_retry(url, img_name, PROXIES, TIMEOUT)
        if code == -1:
            save_error_log(url)
            return
        elif code == 1:
            logging.info("{}已保存".format(img_name))
        else:
            return
    else:
        return


def run_task(task_num,city_code,task_info):
    # 确定城市主目录存在,确定分组提交目录存在
    city_dir = SAVE_DIR.format(city_code)
    if not os.path.exists(city_dir):
        os.mkdir(city_dir)
    save_root_dir = city_dir+task_info['pushDir']
    if not os.path.exists(save_root_dir):
        os.mkdir(save_root_dir)

    # 任务数，redis配置，城市代码
    logging.info("程序开始运行!")
    # 数据开始入队列
    x_start = task_info['xStart']
    y_start = task_info['yStart']
    tasks = []
    for x in range(int(x_start),int(x_start)+50):
        for y in range(int(y_start),int(y_start)+50):
            tasks.append((x,y,))
    logging.warning('开始执行任务')
    pool = ThreadPoolExecutor(max_workers=MAX_CONCURRENT)
    for i in range(task_num):# 2500
        pool.submit(single_task,tasks.pop(),city_code,task_info)
    pool.shutdown()
    logging.info("爬虫任务结束!")
    return True




