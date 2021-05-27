#!/usr/bin/python
# coding=utf-8
'''
Date: 2021-05-27 16:41:46
LastEditors: recar
LastEditTime: 2021-05-27 17:01:49
'''

# https://paper.seebug.org/?page=1

from scripts.base import Base


class Spider(Base):
    def __init__(self, resv):
        super(Spider, self).__init__(resv)
        self.script_name = "paper"
        self.source = "paper"
        self.source_url = "https://paper.seebug.org"
        self.url = "https://paper.seebug.org/?page=1"
        self.base_url = "https://paper.seebug.org/"
        self.title_xpath = '//*[@id="wrapper"]/main/div/article[{0}]/header/h5/a/text()'
        self.href_xpath = '//*[@id="wrapper"]/main/div/article[{0}]/header/h5/a/@href'
        self.synopsis_xpath = '//*[@id="wrapper"]/main/div/article[{0}]/section/text()'
        self.tag_xpath = '//*[@id="wrapper"]/main/div/article[{0}]/header/section/a/text()'
        # 0是文章 1 是cve
        self.new_type = 0

    def parse(self, response, test=False):
        max_size = 10
        frist_size = 2
        init_size = 0
        return self.base_parse(response, init_size, frist_size, max_size, test=test)

    def run(self):
        self.logger.info("update gitlab_advisories")
        self.update()
