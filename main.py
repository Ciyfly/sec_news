#!/usr/bin/python
# coding=utf-8
'''
Date: 2021-01-07 11:33:40
LastEditors: recar
LastEditTime: 2021-01-07 12:11:45
'''
from sqlalchemy import create_engine
from log import logger
import configparser
import importlib
import traceback
import schedule
import pymongo
import json
import time
import sys
import os

class SpiderSec():
    def __init__(self, resv):
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
                if suffix == '.py' and name!="base":
                    self.script_list.append(name)
                    
    def run(self):
        """
        加载脚本
        """
        try:
            for script_name in self.script_list:
                metaclass = importlib.import_module(script_name)
                metaclass.Spider(resv).run() # noqa E501
        except Exception:
            self.logger.error(traceback.format_exc())


class Resvars():

    def __init__(self):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        # config
        config_path = os.path.join(self.base_path, "config", "config.ini") # noqa E501
        self.conf = configparser.ConfigParser()
        self.conf.read(config_path)
        self.logger = logger
        self.model = self.conf.get('others', "model")
        self.sleep_time = int(self.conf.get('others', 'time'))
        if self.model == "debug":
            self.model = False
        else:
            self.model = True
        env_db_host = os.environ.get('DB_HOST')
        env_db_port = os.environ.get('DB_PORT')
        env_db_username = os.environ.get('DB_USER')
        env_db_password = os.environ.get('DB_PASS')
        # db
        db_host = env_db_host if env_db_host else self.conf.get('db', "host") # noqa E501
        db_port = env_db_port if env_db_port else self.conf.get('db', "port") # noqa E501
        db_username = env_db_username if env_db_username else self.conf.get('db', "username") # noqa E501
        db_password = env_db_password if env_db_password else self.conf.get('db', "password") # noqa E501
        # mongo连接
        engine = create_engine("mysql://user:password@hostname/dbname?charset=utf8")
        myclient = pymongo.MongoClient(
            "mongodb://{0}:{1}@{2}:{3}/".format(
                mongo_username, mongo_password, mongo_host, mongo_port
                )
            )
        self.news_info = myclient["sec_news"]["news_info"]


def run():
    logger.info('start')
    hp = SpiderSec(resv)
    hp.run()
    logger.info('end')

if __name__ == '__main__':
    resv = Resvars()
    schedule.every(resv.sleep_time).seconds.do(run)
    while True:
        schedule.run_pending()
        time.sleep(1)
