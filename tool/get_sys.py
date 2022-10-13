# coding=utf-8


# 获取系统信息
import platform
import sys

def get_sys():
    sysstr = platform.system()
    if(sysstr =="Windows"):
        return "Windows"
    elif(sysstr == "Linux"):
        return "Linux"
    else:
        return "Other System"

if __name__ == '__main__':
    print(get_sys())