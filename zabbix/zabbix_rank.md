zabbix_rank 的介绍
====

初始需求：
---
> 为了解决zabbix不能排序的问题。<br>
> 比如我需要获取zabbix所监控的主机的流量最高的前20台机器的IP地址。

需要用到的组件：
---
>python 2.7 <br>
>influxdb<br>
>grafana<br>

效果图如下：
---
![image](https://github.com/mianbao-cn-com/ops_small_scrapt/blob/master/zabbix/image/zabbix/1551150277970.jpg)

待优化：
---
- [ ] 支持针对于组的查询