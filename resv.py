#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-18 23:58:47
LastEditors: recar
LastEditTime: 2021-05-27 18:11:00
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scripts.models import Base_model
from log import logger
import configparser
import os

class Resvars():

    def __init__(self):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        # config
        config_path = os.path.join(self.base_path, "config", "config.ini") # noqa E501
        self.conf = configparser.ConfigParser()
        self.conf.read(config_path, encoding="utf-8-sig")
        self.logger = logger
        self.model = self.conf.get('others', "model")
        self.spider_time = int(self.conf.get('others', 'spider_time'))
        self.subdomain_time = int(self.conf.get('others', 'subdomain_time'))
        self.tag_list = eval(self.conf.get('filter', "tag_list"))
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
        # db连接
        # self.engine = create_engine("mysql://{0}:{1}@{2}/{3}?charset=uft8".format(
        #     db_username, db_password,
        #     db_host, db_port, "news"
        #     ))
        self.engine = create_engine('sqlite:///news.db')
        self.DBSession = sessionmaker(bind=self.engine)()
