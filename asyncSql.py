# coding=utf-8

# 异步链接mysql
# import asyncio
# import aiomysql
#
#
# async def create_pool(loop, **kw):
#     print('create database connection pool...')
#     global __pool
#     __pool = await aiomysql.create_pool(
#         host=kw.get('host', 'localhost'),
#         port=kw.get('port', 3306),
#         user=kw['user'],
#         password=kw['password'],
#         db=kw['db'],
#         charset=kw.get('charset', 'utf8'),
#         autocommit=kw.get('autocommit', True),
#         maxsize=kw.get('maxsize', 10),
#         minsize=kw.get('minsize', 1),
#         loop=loop
#     )
import pymysql
table = 'big_tile'
# 同步链接mysql
db = 'google_map'
host = '192.168.10.230'
user = 'root'
password = '123456'
charset = 'utf8'
port = 3306
conn = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset, port=port)


# 链接mysql并设置爬虫参数


