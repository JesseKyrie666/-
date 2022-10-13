# coding=utf-8

import logging
from PIL import Image
import os
from engine import SAVE_DIR


def join_imgs_y(imgs_path, saver_img):
    all_length = 0
    imgs = []
    for img_path in imgs_path:
        img = Image.open(img_path)
        img_size = img.size
        # all_length+=img_size[0]
        loc = (0, all_length)
        # print("起始纵坐标位置", all_length)
        # print("起始位置", loc)
        all_length += img_size[0]
        img_one_join = [img, loc]
        imgs.append(img_one_join)
    # # 开始拼接
    # joint = Image.new('RGB', (256, len(imgs_path) * 256))
    joint = Image.new('RGBA', (256, len(imgs_path) * 256))
    for img in imgs:
        joint.paste(img[0], img[1])

    joint.save(saver_img)
    # print("拼接结束..")


def join_imgs_x(imgs_path, saver_img):
    all_length = 0
    imgs = []
    for img_path in imgs_path:
        img = Image.open(img_path)
        img_size = img.size
        # all_length+=img_size[0]
        loc = (all_length, 0)
        # print("起始横坐标位置", all_length)
        # print("起始位置", loc)
        all_length += img_size[0]
        img_one_join = [img, loc]
        imgs.append(img_one_join)
    # joint = Image.new('RGB', (len(imgs_path) * 256, len(imgs_path) * 256))
    joint = Image.new('RGBA', (len(imgs_path) * 256, len(imgs_path) * 256))
    for img in imgs:
        joint.paste(img[0], img[1])
    joint.save(saver_img)
    # print("拼接结束..")

    # 删除部分数据
    for img_path in imgs_path:
        os.remove(img_path)


def depart_groups(x_min, x_max, y_min, y_max):
    # 根据x ,y 增长50个对数据分组
    groups = []
    for i in range(x_min, x_max, 50):
        for j in range(y_min, y_max, 50):
            group = []
            # # print("起始位置===>",i, j)
            for x in range(i, i + 50):
                for y in range(j, j + 50):
                    group.append([x, y])
            # # print("分组数据===>", group)
            groups.append(group)
    return groups


def add_v2(group, saver_end, bulk):
    all_imgs = []
    for i in range(0, len(group), 50):
        index_start = i
        index_end = i + 50
        hit = group[i:i + 50]
        # add_y.append(hit)
        # # print("分组数据===>", hit)
        x = hit[0][0]
        next_img = 'imgs/' + str(x) + '.png'
        # print("生成的第一组数据", next_img)
        add_y = []
        for one in hit:
            x = one[0]
            y = one[1]
            img = bulk.replace('bulk/', 'piece/') + "18/" + str(x) + '/' + str(y) + '.png'
            add_y.append(img)
            # # print(img)
            # 先拼接y方向
        join_imgs_y(add_y, next_img)
        all_imgs.append(next_img)
    join_imgs_x(all_imgs, saver_end)
    # print("ok!!")


def check(mjson):
    cityId = mjson['city_id']
    # print("城市id==>", cityId)
    # print(mjson)
    # 创建一个bulk目录
    bulk = SAVE_DIR.format(cityId) + mjson['pushDir'] + '/bulk/'
    # print('bulk', bulk)
    if not os.path.exists(bulk):
        os.mkdir(bulk)
    end_file = bulk + '18_{}_{}_50.png'
    x = mjson["x_start"]
    y = mjson["y_start"]
    save_file = end_file.format(x, y)
    group = depart_groups(x, x + 50, y, y + 50)
    hit = group[0]
    # print("开始拼接数据====================================>{}<====================================".format(end_file))
    # 更改数据的存储位置
    # 确定大图是否存在,存在即不拼图
    if not os.path.exists(save_file):
        add_v2(hit, save_file, bulk)
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>拼接完成18_{}_{}.png<<<<<<<<<<<<<<<<<<<<<<<<<<<<".format(x, y))
    else:
        logging.warning("======>已存在<=====" + save_file)
    return 1


def add_img_big(mjson):
    try:
        code = check(mjson)
        if code:
            return 1
    except:
        return 0
