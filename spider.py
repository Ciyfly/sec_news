#!/usr/bin/python
# coding=utf-8
'''
Date: 2021-01-07 11:33:40
LastEditors: Recar
LastEditTime: 2021-01-23 23:09:41
'''
from resv import Resvars
from log import logger
import importlib
import traceback
import schedule
import json
import time
import sys
import os

class SpiderSec():
    def __init__(self, resv):
        self.resv = resv
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.script_path = os.path.join(self.base_path, "scripts")
        sys.path.append(self.script_path)
        self.logger = resv.logger
        self._get_scripts()
        self.logger.debug('use script list: %s', self.script_list)    

    def _get_scripts(self):
        self.script_list = list()
        for root, dirs, files in os.walk(self.script_path):  
            for filename in files:
                name = os.path.splitext(filename)[0]
                suffix = os.path.splitext(filename)[1]
                if suffix == '.py' and name!="base" and name!="models":
                    self.script_list.append(name)

    def run(self):
        """
        加载脚本
        """
        try:
            for script_name in self.script_list:
                self.logger.info("run {0}".format(script_name))
                metaclass = importlib.import_module(script_name)
                metaclass.Spider(self.resv).run() # noqa E501
        except Exception:
            self.logger.error(traceback.format_exc())


def run():
    logger.info('start')
    hp = SpiderSec(resv)
    hp.run()
    logger.info('end')

if __name__ == '__main__':
    resv = Resvars()
    schedule.every(resv.spider_time).seconds.do(run)
    while True:
        schedule.run_pending()
        time.sleep(1)
