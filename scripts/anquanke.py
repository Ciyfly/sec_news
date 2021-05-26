#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-10 16:40:29
LastEditors: recar
LastEditTime: 2021-05-26 15:23:29
'''
# https://www.anquanke.com/
from scripts.models import News
from scripts.base import Base
from lxml import etree
import traceback
import requests
import json

class Spider(Base):
    def __init__(self, resv):
        super(Spider, self).__init__(resv)
        self.script_name = "anquanke"
        self.source = "安全客"
        self.source_url = "https://www.anquanke.com/"
        self.url = "https://api.anquanke.com/data/v1/posts?page=1&size=20"
        self.base_url = "https://www.anquanke.com/"
        self.new_type = 0

    def parse(self, response, test=False):
        add_news = list()
        try:
            datas = json.loads(response).get("data")
            for data in datas:
                title = data.get("title")
                synopsis = data.get("desc")
                href = data.get("url")
                cover = data.get("cover")
                add_news.append({
                    "title": title,
                    "synopsis": synopsis,
                    "href": href,
                    "cover": cover
                })
            return add_news
        except:
            self.logger.error(traceback.format_exc())
            return add_news

    def run(self):
        self.logger.info("update anquanke")
        self.update()
