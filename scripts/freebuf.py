#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-10 16:40:29
LastEditors: Recar
LastEditTime: 2021-05-24 21:12:59
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

    def parse(self, response, test=False):
        try:
            add_news = list()
            datas = json.loads(response).get("data").get("list")
            for data in datas:
                title = data.get("post_title")
                synopsis = data.get("content")
                href = "".join([self.base_url, data.get("url")])
                if self.last_news:
                    if title == self.last_news.title and not test:
                        self.logger.info("{0} add {1}".format(self.script_name, len(add_news)))
                        break
                add_news.append({
                    "title": title,
                    "synopsis": synopsis,
                    "href": href
                })
                if test:
                    break
            return add_news
        except:
            self.logger.error(traceback.format_exc())
            return add_news

    def update_new(self, test=False):
        self.update_json(test=test)

    def run(self):
        if self.need_update():
            self.logger.info("update freebuf")
            self.update_new()
        else:
            self.logger.info("== freebuf")
