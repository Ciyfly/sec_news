#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-10 15:34:13
LastEditors: Recar
LastEditTime: 2021-01-10 17:03:31
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
        self.get_last_info()
        self.get_url_frist_title('//*[@id="includeList"]/table/tr[1]/td/p[1]/a/text()')

    def update_new(self, test=False):
        add_news = list()
        try:
            html = requests.get(self.url, headers=self.headers).content
            r=etree.HTML(html)
            title_base = '//*[@id="includeList"]/table/tr[{0}]/td/p[1]/a/text()'
            href_base = '//*[@id="includeList"]/table/tr[{0}]/td/p[1]/a/@href'
            synopsis_base = '//*[@id="includeList"]/table/tr[{0}]/td/p[2]/a[2]/text()'
            if not test:
                max_size = 31
            else:
                max_size = 2
            for i in range(1, max_size):
                title=r.xpath(title_base.format(i))[0] if r.xpath(title_base.format(i)) else None
                href=r.xpath(href_base.format(i))[0] if r.xpath(href_base.format(i)) else None
                synopsis=r.xpath(synopsis_base.format(i))[0] if r.xpath(synopsis_base.format(i)) else None
                if title:
                    title = title.replace("\n", "").replace("\t", "").strip()
                if href:
                    href = href.replace("\n", "").replace("\t", "").strip()
                    href = "https://xz.aliyun.com/{0}".format(href)
                if synopsis:
                    synopsis = synopsis.replace("\n", "").replace("\t", "").strip()
                self.logger.debug("{0} find: {1}".format(self.script_name, title))
                if self.last_news:
                    if title == self.last_news.title and not test:
                        self.logger.info("{0} add {1}".format(self.script_name, len(add_news)))
                        break
                self.logger.info("aliyun_xz find: {0}".format(title))
                self.logger.info("aliyun_xz find: {0}".format(href))
                self.logger.info("aliyun_xz find: {0}".format(synopsis))
                add_news.append(News(
                    title=title,synopsis=synopsis,
                    script_name=self.script_name,
                    source=self.source, href=href))
        except Exception:
            self.logger.error(traceback.format_exc())
        try:
            for new in add_news:
                self.DBSession.add(new)
            self.DBSession.commit()
        except Exception:
            self.logger.error(traceback.format_exc())


    def run(self):
        if self.need_update():
            self.logger.info("update gitlab_advisories")
            self.update_new()
        else:
            self.logger.info("== gitlab_advisories")
