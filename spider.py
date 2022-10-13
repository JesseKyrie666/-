# coding=utf-8

import requests
import logging
from engine import *
import os


# 日志输出样式
log_format = '%(levelname)s <=== (%(asctime)s) ====> %(message)s'
logging.basicConfig(
    filename=LOG_SUCCESS,
    format=log_format,
    level=logging.INFO
)


class Spider:
    def __init__(self):
        pass
    
    def request_url(self, url, img_name, proxies,timeout):
        if os.path.exists(img_name):
            logging.info('图片已经存在: %s' % img_name)
            return 0
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
        # logging.debug("正在请求url:{}".format(url))
        try:
            # resp = requests.get(url, headers=headers, proxies=proxies,timeout=timeout)
            resp = requests.get(url, headers=headers, timeout=timeout) # 无代理
            # 接口响应时间
            # logging.info("接口响应时长:{}".format(resp.elapsed.total_seconds()))
            # logging.info("响应状态码:{}".format(resp.status_code))
            if resp.status_code == 200:
                with open(img_name, 'wb+') as s:
                    s.write(resp.content)
                # if not check_size(img_name):
                #     return 0
                return 1
            else:
                logging.info("状态码错误url:=======>{}".format(url))
                return -1
        except Exception as e:
            print(e)
            logging.error("请求失败url:=======>{}".format(url))
            return -1

    # 重试
    def request_with_retry(self, url, img_name, proxies,timeout):
        for i in range(MAX_RETRY_NUM):
            code = self.request_url(url, img_name, proxies,timeout)
            if code == 1 or code == 0:
                return 1
        return -1


def check_size(img_name):
    file_size = int(os.path.getsize(img_name))
    if file_size>=1000:
        return True
    return False


