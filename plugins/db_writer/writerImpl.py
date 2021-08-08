#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# @Time    : 2021/8/8 19:29
# @Author  : StLeoX
# @Email   : 1228354389@qq.com
import queue
from multiprocessing import Process
from db_writer_utils import Singleton, wlog
from bufferImpl import Buffer
from settings.const import DatabaseType


class Writer(Process):
    def __init__(self, buffer_, client_, dbtype_):
        super(Writer, self).__init__(name='db_writer', daemon=False)
        self.buffer: Buffer = buffer_
        self.client = client_
        self.dbtype = dbtype_

    def run(self) -> None:
        # 把switch放在外面有助于性能
        if self.dbtype == DatabaseType.INFLUXDB.value:
            while True:
                try:
                    item_ = self.buffer.get(timeout=5)  # 最多等待秒数，之后抛出Empty异常
                    self.client.write_points(item_)
                except KeyboardInterrupt:
                    exit(15)
                except queue.Empty:
                    wlog.p_info('timeout')
                    exit(14)
        elif self.dbtype == DatabaseType.ES.value:
            pass
        elif self.dbtype == DatabaseType.MYSQL.value:
            pass
        elif self.dbtype == DatabaseType.PROMETHEUS.value:
            pass
        else:
            raise NotImplementedError


@Singleton
class SingleWriter(Writer):
    def __init__(self, buffer_, client_, dbtype_):
        super(SingleWriter, self).__init__(buffer_, client_, dbtype_)
        self.daemon = True  # 覆盖，设置成守护进程

    def run(self) -> None:
        super(SingleWriter, self).run()
