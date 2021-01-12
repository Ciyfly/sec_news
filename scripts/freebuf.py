#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-10 16:40:29
LastEditors: Recar
LastEditTime: 2021-01-12 23:59:04
'''
# https://www.freebuf.com/
from .models import News
from scripts.base import Base
from lxml import etree
import traceback
import requests


class Spider(Base):
    def __init__(self, resv):
        super(Spider, self).__init__(resv)
        self.script_name = "freebuf"
        self.source = "freebuf"
        self.url = "https://www.freebuf.com/fapi/frontend/home/article?page=1&limit=20&type=1&day=&category=%E7%B2%BE%E9%80%89"
        self.base_url = "https://www.freebuf.com"
        self.get_last_info()

    def update_new(self, test=False):
        self.update_json(test=test)

    def run(self):
        if self.need_update():
            self.logger.info("update freebuf")
            self.update_new()
        else:
            self.logger.info("== freebuf")
