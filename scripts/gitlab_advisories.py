#!/usr/bin/python
# coding=utf-8
'''
Date: 2021-01-07 11:36:26
LastEditors: Recar
LastEditTime: 2021-01-10 15:43:21
'''
from .models import News
from scripts.base import Base
import traceback


class Spider(Base):
    def __init__(self, resv):
        super(Spider, self).__init__(resv)
        self.script_name = "gitlab_advisories"
        self.source = "https://github.com/advisories"
        self.url = "https://github.com/advisories"
        self.get_last_info()
        self.get_url_frist_title('//*[@id="js-pjax-container"]/div/div[2]/div[2]/div/div[2]/div/a/text()')

    def update_new(self):
        add_news = list()
        try:
            html = requests.get(self.url).content
            r=etree.HTML(html)
            title_base = '//*[@id="js-pjax-container"]/div/div[2]/div[{0}]/div/div[2]/div/a/text()'
            href_base = '//*[@id="js-pjax-container"]/div/div[2]/div[{0}]/div/div[2]/div/a/@href'
            synopsis_base = '//*[@id="js-pjax-container"]/div/div[2]/div[{0}]/div/div[2]/div/div/span[1]/text()'
            for i in range(2, 27):
                title=r.xpath(title_base.format(i))[0] if r.xpath(title_base.format(i)) else None
                href=r.xpath(href_base.format(i))[0] if r.xpath(href_base.format(i)) else None
                synopsis=r.xpath(synopsis_base.format(i))[0] if r.xpath(synopsis_base.format(i)) else None
                if title:
                    title = title.replace("\n", "").replace("\t", "").strip()
                if href:
                    href = href.replace("\n", "").replace("\t", "").strip()
                    href = "https://github.com{0}".format(href)
                if synopsis:
                    synopsis = synopsis.replace("\n", "").replace("\t", "").strip()
                self.logger.debug("{0} find: {1}".format(self.script_name, title))
                if title == self.last_news.title:
                    self.logger.info("{0} add {1}".format(self.script_name, len(add_news)))
                    break
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
