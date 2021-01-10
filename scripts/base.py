#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-09 23:09:34
LastEditors: Recar
LastEditTime: 2021-01-10 16:36:04
'''

from .models import News
from lxml import etree
import requests

class Base():
    def __init__(self, resv):
        self.resv = resv
        self.DBSession = self.resv.DBSession
        self.logger = self.resv.logger
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
        }
        

    def get_last_info(self):
        self.last_news = self.resv.DBSession.query(News).filter_by(script_name=self.script_name).order_by(News.update_time.desc()).first()

    def get_url_frist_title(self, xpath):
        html = requests.get(self.url).content
        r=etree.HTML(html)
        url_frist_title=r.xpath(xpath)
        if not url_frist_title:
            self.logger.error("{0} get url_frist_title is None please check".format(self.script_name))
            self.url_frist_title =  None
        else:
            self.url_frist_title =  url_frist_title[0].replace("\n", "").replace("\t", "").strip()

    def need_update(self):
        last_title = self.last_news.title
        self.logger.debug("last_title: {0}".format(last_title))
        self.logger.debug("url_frist_title: {0}".format(self.url_frist_title))
        if not self.url_frist_title:
            return False
        elif last_title != self.url_frist_title:
            return True
        else:
            return False
