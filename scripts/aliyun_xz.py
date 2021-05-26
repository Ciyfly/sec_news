#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-10 15:34:13
LastEditors: recar
LastEditTime: 2021-05-26 14:40:15
'''

from scripts.base import Base

class Spider(Base):
    def __init__(self, resv):
        super(Spider, self).__init__(resv)
        self.script_name = "aliyun_xz"
        self.source = "阿里先知"
        self.source_url = "https://xz.aliyun.com/"
        self.url = "https://xz.aliyun.com/"
        self.base_url = "https://xz.aliyun.com/"
        self.title_xpath = '//*[@id="includeList"]/table/tr[{0}]/td/p[1]/a/text()'
        self.href_xpath = '//*[@id="includeList"]/table/tr[{0}]/td/p[1]/a/@href'
        self.synopsis_xpath = '//*[@id="includeList"]/table/tr[{0}]/td/p[2]/a[2]/text()'
        self.new_type = 0

    def parse(self, response, test=False):
        max_size = 31
        frist_size = 2
        init_size = 1
        return self.base_parse(response, init_size, frist_size, max_size, test=test)

    def run(self):
        self.logger.info("update aliyun_xz")
        self.update()
