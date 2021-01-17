#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-10 16:40:29
LastEditors: Recar
LastEditTime: 2021-01-16 10:58:20
'''
# https://www.freebuf.com/
from scripts.models import News
from scripts.base import Base
from lxml import etree
import traceback
import requests
import json

class Spider(Base):
    def __init__(self, resv):
        super(Spider, self).__init__(resv)
        self.script_name = "freebuf"
        self.source = "freebuf"
        self.source_url = "https://www.freebuf.com"
        self.url = "https://www.freebuf.com/fapi/frontend/home/article?page=1&limit=20&type=1&day=&category=%E7%B2%BE%E9%80%89"
        self.base_url = "https://www.freebuf.com"
        self.get_url_frist_title()
        self.get_last_info()
        self.new_type = 0

    def get_url_frist_title(self):
        response = requests.get(self.url).content
        if response:
            datas = json.loads(response).get("data").get("list")
            for data in datas:
                title = data.get("post_title")
                self.url_frist_title = title
                break
            
    def update_new(self, test=False):
        self.update_json(test=test)

    def run(self):
        if self.need_update():
            self.logger.info("update freebuf")
            self.update_new()
        else:
            self.logger.info("== freebuf")
