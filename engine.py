# coding=utf-8

# redis队列
# REDIS_HOST = '127.0.0.1' # 本地
REDIS_HOST = '192.168.10.230' # 内网
# REDIS_HOST = '192.168.200.131' # 虚拟机
REDIS_PORT = 6379
REDIS_DB = 9 # 选择数据库单个机器自主分配数据库
REDIS_QUEUE = 'GoogleMap_Zoom' # 后续采用单机器一个数据库，多个队列

# 爬取的链接
# 旧链接
# uri = 'https://mts0.google.com/vt/lyrs=r@189000000&hl=en&src=app&x={}&y={}&z={}&s=Gal&apistyle=s.t:1%7Cs.e:l.t%7Cp.v:off,s.t:2%7Cs.e:l%7Cp.v:off,s.t:2%7Cs.e:g%7Cp.v:off,s.t:3%7Cs.e:l.t%7Cp.v:off,s.t:5%7Cs.e:g%7Cp.v:off,s.t:5%7Cs.e:l.t%7Cp.v:off,s.t:6%7Cs.e:l.t%7Cp.v:off,s.t:6%7Cs.e:g%7Cp.v:off,s.t:33%7Cs.e:l%7Cp.v:off,s.t:35%7Cs.e:l%7Cp.v:off,s.t:49%7Cs.e:l.i%7Cp.v:off,s.t:66%7Cs.e:l.i%7Cp.v:off,s.t:66%7Cs.e:l.t%7Cp.v:off'
# 新链接
uri = 'https://mts0.google.com/vt/lyrs=r@189000000&hl=en&src=app&x={}&y={}&z={}&s=Gal&apistyle=s.t:1%7Cs.e:l.t%7Cp.v:off,s.t:1%7Cs.e:g.s%7Cp.v:off,s.t:2%7Cs.e:l%7Cp.v:off,s.t:2%7Cs.e:g%7Cp.v:off,s.t:3%7Cs.e:l.t%7Cp.v:off,s.t:5%7Cs.e:g%7Cp.v:off,s.t:5%7Cs.e:l.t%7Cp.v:off,s.t:6%7Cs.e:l.t%7Cp.v:off,s.t:6%7Cs.e:g%7Cp.v:off,s.t:33%7Cs.e:l%7Cp.v:off,s.t:35%7Cs.e:l%7Cp.v:off,s.t:49%7Cs.e:l.i%7Cp.v:off,s.t:65%7Cs.e:l.t%7Cp.v:off,s.t:65%7Cs.e:g%7Cp.v:off,s.t:66%7Cs.e:l.i%7Cp.v:off,s.t:66%7Cs.e:l.t%7Cp.v:off'



# 文件持久化
SAVE_DIR = '/home/map/{}/' # 服务器本地请使用这个按照国家名称存储
# SAVE_DIR = r'\\192.168.10.230\tile\{}/' # 其他机器请使用这个
# 新ssd
# SAVE_DIR = r'\\192.168.10.230\ssd\map\{}/' # 其他机器请使用这个


# 日志输出文件
LOG_SUCCESS = 'log.txt'
LOG_ERROR = 'error_log.txt'

# 最大并发数
MAX_CONCURRENT = 50

# 代理路径
PROXIES = {'http': 'http://127.0.0.1:4780', 'https': 'http://127.0.0.1:4780'}

# 超时时间
TIMEOUT = 3

#  配置起始位置与结束位置 ===>暂时不配

# 配置地图数据层级
MAP_LEVEL = 18

# 最大重试次数
MAX_RETRY_NUM = 10

# 消息队列
KAFKA_QUEUE = 'BIG_TILE'
RABBITMQ_QUEUE = 'BIG_TILE'