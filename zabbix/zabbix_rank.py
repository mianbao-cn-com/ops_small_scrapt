# -*- coding:utf-8 -*-
'''
@Created on 2019年02月25日

@author: mianbao

@author_web: Mianbao.cn.com

@用于获取所需的key
'''
from influxdb import InfluxDBClient

from login import login


class ITEMTOP(object):

    def __init__(self, key):
        self.__z = login()
        self.__key = key
        self.__want_top_num = 20

    def SearchFilter(self):
        '''所需key的查询条件'''
        out_filter = {
            "output": "extend",
            "search": {
                "key_": self.__key  # example: "net.if.out"
            }
        }
        return out_filter

    def GetZabbixWant(self):
        '''从zabbix上面获取所需要的信息'''
        rs = dict()
        items = self.__z.item.get(self.SearchFilter())
        for item in items:
            rs = self.ItemRsScheduler(item, rs)
        host_infos = self.ItemSortAndSlice(rs)
        return host_infos

    def ItemRsScheduler(self, item, rs):
        hostid = item.get('hostid')
        key = item.get('key_')
        value = item.get('lastvalue')

        item_dict = {'hostid': hostid, 'key': key}
        if rs.get(value):
            rs[value].append(item_dict)
        else:
            rs[value] = [item_dict, ]

        return rs

    def ItemSortAndSlice(self, rs):
        key_list = rs.keys()
        key_list_int = list()
        [key_list_int.append(int(x)) for x in key_list]
        key_list = key_list_int
        key_list.sort(reverse=True)
        want_top = key_list[:self.__want_top_num]

        host_rs = dict()
        for key in want_top:
            host_infos = rs.get(str(key))
            for host_info in host_infos:
                host_info['hostname'] = self.FromHostIdGetHostIp(host_info.get('hostid'))
            if host_rs.get(key):
                host_rs.get(key).append(host_infos)
            else:
                host_rs[key] = [host_infos]
        return host_rs

    def FromHostIdGetHostIp(self, id):
        host = 'No HostNameGet'
        rs = self.__z.host.get({"output": ["host"], "hostids": id})
        if len(rs) > 0:
            host = rs[0].get('host', 'No HostNameGet')
        return host


def FormtPrint(item_key, rs):
    for key, value in rs.get(item_key).items():
        for the_one in value:
            for one in the_one:
                SaveToInfluxdb(one.get('hostname'), one.get('key'), key, item_key)
                print '%s---%s----%s bps' % (one.get('hostname'), one.get('key'), unit_convert(key))


def unit_convert(v1, start=0):
    v1 = int(v1)
    li = ['bytes', 'Kb', 'M', 'G', 'T', 'P']
    a = start
    while v1 > 1024:
        v1 = v1 / 1024
        a += 1
    return str(round(v1, 1)) + str(li[a])


def SaveToInfluxdb(ip, mark, value, type=None):
    c = InfluxDBClient('localhost', 8086, 'root', 'root', 'zabbix_rank')
    json_body = [
        {
            "measurement": "network_rank",
            "tags": {
                "host": ip,
                "mark": mark,
                "type": type
            },
            "fields": {
                "value": value
            }
        }
    ]
    c.write_points(json_body)


if __name__ == '__main__':
    rs = dict()

    want = ITEMTOP('net.if.out')
    out_rs = want.GetZabbixWant()
    rs['out'] = out_rs

    want = ITEMTOP('net.if.in')
    out_rs = want.GetZabbixWant()
    rs['in'] = out_rs

    # 以下代码主要用于console打印
    print '=' * 30, 'OUT', '=' * 30
    FormtPrint('out', rs)

    print '*' * 30, 'IN', '*' * 30
    FormtPrint('in', rs)



















