#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-10 16:40:29
LastEditors: Recar
LastEditTime: 2021-05-24 21:30:26
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
        self.get_url_frist_title()
        self.get_last_info()
        self.new_type = 0

    def get_url_frist_title(self):
        response = requests.get(self.url).content
        if response:
            datas = json.loads(response).get("data")
            for data in datas:
                title = data.get("title")
                self.url_frist_title = title
                break

    def parse(self, response, test=False):
        add_news = list()
        try:
            datas = json.loads(response).get("data")
            for data in datas:
                title = data.get("title")
                synopsis = data.get("desc")
                href = data.get("url")
                cover = data.get("cover")
                if self.last_news:
                    if title == self.last_news.title and not test:
                        self.logger.info("{0} add {1}".format(self.script_name, len(add_news)))
                        break
                add_news.append({
                    "title": title,
                    "synopsis": synopsis,
                    "href": href,
                    "cover": cover
                })
                if test:
                    # test模式只添加第一个数据
                    break
            return add_news
        except:
            self.logger.error(traceback.format_exc())
            return add_news


    def update_new(self, test=False):
        self.update_json(test=test)

    def run(self):
        if self.need_update():
            self.logger.info("update anquanke")
            self.update_new()
        else:
            self.logger.info("== anquanke")
