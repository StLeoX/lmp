#! /usr/bin/python3
# -*- coding:utf-8 -*-
from settings.const import DatabaseType
from settings.init_db import influx_client


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

# todo 封装write2db接口
