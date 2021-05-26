#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-10 16:40:29
LastEditors: recar
LastEditTime: 2021-05-26 14:43:15
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
        self.new_type = 0

    def parse(self, response, test=False):
        try:
            add_news = list()
            datas = json.loads(response).get("data").get("list")
            for data in datas:
                title = data.get("post_title")
                synopsis = data.get("content")
                href = "".join([self.base_url, data.get("url")])
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

    def run(self):
        self.logger.info("update freebuf")
        self.update()
