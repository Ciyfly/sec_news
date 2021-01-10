#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-10 15:34:13
LastEditors: Recar
LastEditTime: 2021-01-10 19:50:50
'''

from .models import News
from scripts.base import Base
from lxml import etree
import traceback
import requests


class Spider(Base):
    def __init__(self, resv):
        super(Spider, self).__init__(resv)
        self.script_name = "aliyun_xz"
        self.source = "https://xz.aliyun.com/"
        self.url = "https://xz.aliyun.com/"
        self.base_url = "https://xz.aliyun.com/"
        self.get_last_info()
        self.get_url_frist_title('//*[@id="includeList"]/table/tr[1]/td/p[1]/a/text()')
        self.title_xpath = '//*[@id="includeList"]/table/tr[{0}]/td/p[1]/a/text()'
        self.href_xpath = '//*[@id="includeList"]/table/tr[{0}]/td/p[1]/a/@href'
        self.synopsis_xpath = '//*[@id="includeList"]/table/tr[{0}]/td/p[2]/a[2]/text()'

    def update_new(self, test=False):
        max_size = 31
        frist_size = 2
        init_size = 1
        self.update(
            self.title_xpath, self.href_xpath, self.synopsis_xpath,
            max_size, frist_size, init_size, test=test)

    def run(self):
        if self.need_update():
            self.logger.info("update aliyun_xz")
            self.update_new()
        else:
            self.logger.info("== aliyun_xz")
