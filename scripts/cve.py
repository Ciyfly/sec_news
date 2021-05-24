#!/usr/bin/python
# coding=utf-8
'''
Date: 2021-05-24 16:37:17
LastEditors: recar
LastEditTime: 2021-05-24 18:08:36
'''
from scripts.models import News
from scripts.base import Base
from lxml import etree
import traceback
import requests


class Spider(Base):
    def __init__(self, resv):
        super(Spider, self).__init__(resv)
        self.script_name = "cve"
        self.source = "CVE"
        self.source_url = "https://cassandra.cerias.purdue.edu/CVE_changes/today.html"
        self.url = "https://cassandra.cerias.purdue.edu/CVE_changes/today.html"
        self.base_url = "https://cve.mitre.org/"
        self.get_last_info()
        self.get_url_frist_title('/html/body/a[1]/text()')
        self.title_xpath = '/html/body/a[{0}]/text()'
        self.href_xpath = '/html/body/a[{0}]/@href'
        self.synopsis_xpath = '//*[@id="GeneratedTable"]/table/tbody/tr[4]/td/text()'
        self.new_type = 1

    def update_new(self, test=False):
        
        max_size = 50
        frist_size = 2
        init_size = 1
        self.update_cve(
            self.title_xpath, self.href_xpath, self.synopsis_xpath,
            max_size, frist_size, init_size, test=test)
      
    def run(self):
        if self.need_update():
            self.logger.info("update CVE")
            self.update_new()
        else:
            self.logger.info("== CVE")
