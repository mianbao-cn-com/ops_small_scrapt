# -*- coding:utf-8 -*-
'''
@Created on 2018年06月27日

@author: mianbao

@author_web: Mianbao.cn.com

@主要用于zabbix的接口登录
'''
import sys
from zabbix_api import ZabbixAPI


server = ''
path = ''
username = ''
password = ''

def login():
    zapi = ZabbixAPI(server=server, path=path, log_level=0)

    try:
        zapi.login(username, password)
    except Exception:
        print 'Login Faild!'
        sys.exit()
    return zapi


if __name__ == "__main__":
    login()