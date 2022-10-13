# coding=utf-8

from engine import *
from main import *
import os


# 检验数据总量
def ckeck_total(dir):
    files = os.listdir(dir)
    file_total = 0
    for dir0 in files:
        dir_y = dir + dir0 + '/'
        # 计算数据量
        file_total += len(os.listdir(dir_y))
        print("数据总量: %d" % file_total)


# 校验数据丢失情况
def check_lose(hits=None, save_dir='/', lose_file='lose/lose.txt'):
    if not hits:
        return
    tiles = hits['tiles']
    count = 0
    # 生成需要下载的全量数据列表
    with open(lose_file, 'a+', encoding='utf8') as s:
        for til in tiles:
            x_start = til['X']
            y_start = til['Y']
            for x in range(x_start, x_start + 50):
                for y in range(y_start, y_start + 50):
                    img_file = save_dir + str(x) + '/' + str(y) + '.png'
                    # 校验数据是否存在
                    if not os.path.exists(img_file):
                        print(">>>>>>>>>>>>>>>>>丢失的数据", img_file)
                        s.write(str(x) + ',' + str(y) + '\n')
                        count += 1
    print("数据校验完成")
    print("丢失数据总量: %d" % count)
    return


def check_total(task):
    mission = []
    x_start = int(task['xStart'])
    y_start = int(task['yStart'])
    city_id = task["cityId"]
    root_dir = SAVE_DIR.format(city_id) + task['pushDir'] + "/piece/" + '18/'
    for x in range(x_start, x_start + 50):
        for y in range(y_start, y_start + 50):
            img_file = root_dir + str(x) + '/' + str(y) + '.png'
            if not os.path.exists(img_file):
                position = [x, y,]
                mission.append(position)
    if mission:
        logging.error('丢失数据总量: {}'.format(len(mission)))
        logging.error('丢失数据已加入redis队列并重试')
        while True:
            if not mission:
                return 1
            else:
                mis = mission.pop()
                single_task(mis, city_id, task)
    else:
        logging.warning('数据校验完成,未发现丢失数据...')
        return 1
