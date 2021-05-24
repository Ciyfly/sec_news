#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-09 23:09:34
LastEditors: Recar
LastEditTime: 2021-05-24 20:49:51
'''

from .models import News
from lxml import etree
import requests
import traceback
import json

class Base():
    def __init__(self, resv):
        self.resv = resv
        self.DBSession = self.resv.DBSession
        self.logger = self.resv.logger
        self.headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding':'gzip, deflate',
        'Upgrade-Insecure-Requests':'1',
    }
        

    def get_last_info(self):
        self.last_news = self.resv.DBSession.query(News).filter_by(script_name=self.script_name).order_by(News.update_time.desc()).first()

    def get_url_frist_title(self, xpath):
        html = ""
        try:
            html = requests.get(self.url).content
        except:
            self.logger.error("{0} requets error ".format(self.script_name))
            return 
        r=etree.HTML(html)
        url_frist_title=r.xpath(xpath)
        if not url_frist_title:
            self.logger.error("{0} get url_frist_title is None please check".format(self.script_name))
            self.url_frist_title =  None
        else:
            self.url_frist_title =  url_frist_title[0].replace("\n", "").replace("\t", "").strip()

    def need_update(self):
        if not self.last_news:
            return True
        last_title = self.last_news.title
        self.logger.debug("last_title: {0}".format(last_title))
        self.logger.debug("url_frist_title: {0}".format(self.url_frist_title))
        if not self.url_frist_title:
            return False
        elif last_title != self.url_frist_title:
            return True
        else:
            return False

    def update(
        self, title_xpath, href_xpath, synopsis_xpath,
        max_size=20, frist_size=1, init_size=1, test=False ):
        add_news = list()
        html = ""
        try:
            try:
                html = requests.get(self.url, headers=self.headers).content
            except:
                self.logger.error("{0} requets error ".format(self.script_name))
                return 
            r=etree.HTML(html)
            if not test:
                range_size = max_size
            else:
                range_size = frist_size
            for i in range(init_size, range_size):
                title=r.xpath(title_xpath.format(i))[0] if r.xpath(title_xpath.format(i)) else None
                href=r.xpath(href_xpath.format(i))[0] if r.xpath(href_xpath.format(i)) else None
                synopsis=r.xpath(synopsis_xpath.format(i))[0] if r.xpath(synopsis_xpath.format(i)) else None
                if title:
                    title = title.replace("\n", "").replace("\t", "").strip()
                if href:
                    href = href.replace("\n", "").replace("\t", "").strip()
                    href = "{0}/{1}".format(self.base_url, href)
                if synopsis:
                    synopsis = synopsis.replace("\n", "").replace("\t", "").strip()
                self.logger.debug("{0} find: {1}".format(self.script_name, title))
                if self.last_news:
                    if title == self.last_news.title and not test:
                        self.logger.info("{0} add {1}".format(self.script_name, len(add_news)))
                        break
                self.logger.info("{0} find: {1}".format(self.script_name, title))
                self.logger.info("{0} find: {1}".format(self.script_name, href))
                self.logger.info("{0} find: {1}".format(self.script_name, synopsis))
                add_news.append(News(
                    title=title,synopsis=synopsis,
                    script_name=self.script_name,
                    source=self.source, href=href,
                    source_url=self.source_url,
                    new_type=self.new_type))
        except Exception:
            self.logger.error(traceback.format_exc())
        try:
            self.logger.info("{0} add {1}".format(self.script_name, len(add_news)))
            for new in add_news:
                self.DBSession.add(new)
                
            self.DBSession.commit()
        except Exception:
            self.logger.error(traceback.format_exc())

    def update_cve(
        self, title_xpath, href_xpath, synopsis_xpath,
        max_size=20, frist_size=1, init_size=1, test=False ):
        add_news = list()
        try:
            try:
                html = requests.get(self.url, headers=self.headers).content
            except:
                self.logger.error("{0} requets error ".format(self.script_name))
                return 
            r=etree.HTML(html)
            if not test:
                range_size = max_size
            else:
                range_size = frist_size
            for i in range(init_size, range_size):
                title=r.xpath(title_xpath.format(i))[0] if r.xpath(title_xpath.format(i)) else None
                href=r.xpath(href_xpath.format(i))[0] if r.xpath(href_xpath.format(i)) else None
                synopsis = ""
                if href:
                    info_html = requests.get(href, headers=self.headers).content
                    r_info=etree.HTML(info_html)
                    synopsis=r_info.xpath(synopsis_xpath) if r_info.xpath(synopsis_xpath) else None
                    with open("1.txt", "w") as f:
                        f.write(str(info_html))
                if title:
                    title = title.replace("\n", "").replace("\t", "").strip()
                if href:
                    href = href.replace("\n", "").replace("\t", "").strip()
                    href = "{0}/{1}".format(self.base_url, href)
                if synopsis:
                    synopsis = synopsis.replace("\n", "").replace("\t", "").strip()
                self.logger.debug("{0} find: {1}".format(self.script_name, title))
                if self.last_news:
                    if title == self.last_news.title and not test:
                        self.logger.info("{0} add {1}".format(self.script_name, len(add_news)))
                        break
                self.logger.info("{0} find: {1}".format(self.script_name, title))
                self.logger.info("{0} find: {1}".format(self.script_name, href))
                self.logger.info("{0} find: {1}".format(self.script_name, synopsis))
                add_news.append(News(
                    title=title,synopsis=synopsis,
                    script_name=self.script_name,
                    source=self.source, href=href,
                    source_url=self.source_url,
                    new_type=self.new_type))
        except Exception:
            self.logger.error(traceback.format_exc())
        try:
            self.logger.info("{0} add {1}".format(self.script_name, len(add_news)))
            for new in add_news:
                self.DBSession.add(new)
                
            self.DBSession.commit()
        except Exception:
            self.logger.error(traceback.format_exc())

    def update_json(self, test=False):
        try:
            add_news = list()
            response = requests.get(self.url).content
            if response:
                datas = json.loads(response).get("data").get("list")
                for data in datas:
                    title = data.get("post_title")
                    synopsis = data.get("content")
                    href = "".join([self.base_url, data.get("url")])
                    if self.last_news:
                        if title == self.last_news.title and not test:
                            self.logger.info("{0} add {1}".format(self.script_name, len(add_news)))
                            break
                    self.logger.info("{0} find: {1}".format(self.script_name, title))
                    self.logger.info("{0} find: {1}".format(self.script_name, href))
                    self.logger.info("{0} find: {1}".format(self.script_name, synopsis))
                    add_news.append(News(
                        title=title,synopsis=synopsis,
                        script_name=self.script_name,
                        source=self.source, href=href, 
                        source_url=self.source_url,
                        new_type=self.new_type))
                    if test:
                        # test模式只添加第一个数据
                        break
        except Exception:
            self.logger.error(traceback.format_exc())
        try:
            self.logger.info("{0} add {1}".format(self.script_name, len(add_news)))
            for new in add_news:
                self.DBSession.add(new)
                
            self.DBSession.commit()
        except Exception:
            self.logger.error(traceback.format_exc())
