#!/usr/bin/python
# coding=utf-8
'''
Date: 2021-01-07 11:36:26
LastEditors: recar
LastEditTime: 2021-05-26 14:40:32
'''
from scripts.base import Base


class Spider(Base):
    def __init__(self, resv):
        super(Spider, self).__init__(resv)
        self.script_name = "gitlab_advisories"
        self.source = "gitlab advisories"
        self.source_url = "https://github.com/advisories"
        self.url = "https://github.com/advisories"
        self.base_url = "https://github.com/"
        self.title_xpath = '//*[@id="js-pjax-container"]/div/div[2]/div[{0}]/div/div[2]/div/a/text()'
        self.href_xpath = '//*[@id="js-pjax-container"]/div/div[2]/div[{0}]/div/div[2]/div/a/@href'
        self.synopsis_xpath = '//*[@id="js-pjax-container"]/div/div[2]/div[{0}]/div/div[2]/div/div/span[1]/text()'
        self.new_type = 1

    def parse(self, response, test=False):
        max_size = 27
        frist_size = 3
        init_size = 2
        return self.base_parse(response, init_size, frist_size, max_size, test=test)

    def run(self):
        self.logger.info("update gitlab_advisories")
        self.update()
