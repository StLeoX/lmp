#! /usr/bin/python3
# -*- coding:utf-8 -*-
from settings.const import DatabaseType
from settings.init_db import influx_client
from bufferImpl import Buffer, SingleBuffer
from writerImpl import Writer, SingleWriter


def write2db(datatype, data, client=influx_client, dbtype=DatabaseType.INFLUXDB.value):
    """
    :param datatype: 数据类型
    :param data: 数据
    :param client: 数据库client
    :param dbtype: 数据库类型
    """
    if dbtype == DatabaseType.INFLUXDB.value:
        tmp = [{"measurement": None, "tags": {}, "fields": {}, }]
        tmp[0]["measurement"] = datatype["measurement"]
        for x in datatype['tags']:
            tmp[0]["tags"][x] = getattr(data, x)
        for y in datatype['fields']:
            tmp[0]["fields"][y] = getattr(data, y)
        client.write_points(tmp)
    elif dbtype == DatabaseType.ES.value:
        pass
    elif dbtype == DatabaseType.MYSQL.value:
        pass
    elif dbtype == DatabaseType.PROMETHEUS.value:
        pass


# 方案实现
def item_adepter(datatype_, data_):
    item = [{"measurement": None, "tags": {}, "fields": {}, }]
    item[0]["measurement"] = datatype_["measurement"]
    for x in datatype_['tags']:
        item[0]["tags"][x] = getattr(data_, x)
    for y in datatype_['fields']:
        item[0]["fields"][y] = getattr(data_, y)
    return item


# 方案一实现
def write_to_db01(datatype, data, client=influx_client, dbtype=DatabaseType.INFLUXDB.value):
    """
    :param datatype: 数据类型
    :param data: 数据
    :param client: 数据库client
    :param dbtype: 数据库类型
    """
    buffer = Buffer()  # 每次调用都存在一个buffer
    writer = Writer(buffer_=buffer, client_=client, dbtype_=dbtype)  # bind
    writer.start()  # spawn
    while True:
        try:
            buffer.put(item_adepter(datatype, data))
        except KeyboardInterrupt:
            exit(15)


# 方案二实现：单例守护写进程
def write_to_db02(datatype, data, client=influx_client, dbtype=DatabaseType.INFLUXDB.value):
    """
    :param datatype: 数据类型
    :param data: 数据
    :param client: 数据库client
    :param dbtype: 数据库类型
    """
    buffer = SingleBuffer()  # 每次调用都存在一个buffer
    writer = SingleWriter(buffer_=buffer, client_=client, dbtype_=dbtype)  # bind
    writer.start()  # spawn
    while True:
        try:
            buffer.put(item_adepter(datatype, data))
        except KeyboardInterrupt:
            exit(15)
