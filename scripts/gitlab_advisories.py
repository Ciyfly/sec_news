#!/usr/bin/python
# coding=utf-8
'''
Date: 2021-01-07 11:36:26
LastEditors: Recar
LastEditTime: 2021-01-13 00:04:39
'''
from scripts.models import News
from scripts.base import Base
from lxml import etree
import traceback
import requests


class Spider(Base):
    def __init__(self, resv):
        super(Spider, self).__init__(resv)
        self.script_name = "gitlab_advisories"
        self.source = "gitlab advisories"
        self.url = "https://github.com/advisories"
        self.base_url = "https://github.com/"
        self.get_last_info()
        self.get_url_frist_title('//*[@id="js-pjax-container"]/div/div[2]/div[2]/div/div[2]/div/a/text()')
        self.title_xpath = '//*[@id="js-pjax-container"]/div/div[2]/div[{0}]/div/div[2]/div/a/text()'
        self.href_xpath = '//*[@id="js-pjax-container"]/div/div[2]/div[{0}]/div/div[2]/div/a/@href'
        self.synopsis_xpath = '//*[@id="js-pjax-container"]/div/div[2]/div[{0}]/div/div[2]/div/div/span[1]/text()'

    def update_new(self, test=False):
        max_size = 27
        frist_size = 3
        init_size = 2
        self.update(
            self.title_xpath, self.href_xpath, self.synopsis_xpath,
            max_size, frist_size, init_size, test=test)
      
    def run(self):

        if self.need_update():
            self.logger.info("update gitlab_advisories")
            self.update_new()
        else:
            self.logger.info("== gitlab_advisories")
