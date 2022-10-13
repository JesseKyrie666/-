# coding=utf-8


# 获取内网ip

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('192.168.10.230', 80))
print(s.getsockname()[0])
names = s.getsockname()
print(names)
s.close()




