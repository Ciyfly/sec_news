#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-09 23:09:34
LastEditors: recar
LastEditTime: 2021-05-26 15:46:41
'''

from re import I
from .models import News
from lxml import etree
import requests
import traceback
import hashlib
import json
import socket
import urllib3

class Base():
    def __init__(self, resv):
        self.resv = resv
        self.DBSession = self.resv.DBSession
        self.logger = self.resv.logger
        self.timeout = 3
        self.headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    }
        

    def get_response_text(self, url=None, headers=None, timeout=None):
        if url is None:
            url = self.url
        if headers is None:
            headers = self.headers
        if timeout is None:
            timeout = self.timeout
        try:
            html = requests.get(url, headers=self.headers, timeout=self.timeout).content
            return html
        except requests.exceptions.Timeout:
            self.logger.error("{0} requets error timeout".format(self.script_name))
        except socket.timeout:
            self.logger.error("{0} requets error timeout".format(self.script_name))
        except urllib3.exceptions.ReadTimeoutError:
            self.logger.error("{0} requets error timeout".format(self.script_name))
        except requests.exceptions.ConnectionError:
            self.logger.error("{0} requets error timeout".format(self.script_name))
        except Exception:
            self.logger.error(traceback.format_exc())

    def get_hash_code(self, title):
        signaturemd5 = hashlib.md5()
        signaturemd5.update(title.encode('utf-8'))
        return signaturemd5.hexdigest()        

    def is_repeat(self, hash_code):
        if self.DBSession.query(News).filter_by(hash_code=hash_code).first():
            return True
        return False

    def base_parse(self, response, init_size, frist_size, max_size, test=False):
        result = list()
        if not response:
            return result
        r=etree.HTML(response)
        if not test:
            range_size = max_size
        else:
            range_size = frist_size
        for i in range(init_size, range_size):
            title=r.xpath(self.title_xpath.format(i))[0] if r.xpath(self.title_xpath.format(i)) else None
            href=r.xpath(self.href_xpath.format(i))[0] if r.xpath(self.href_xpath.format(i)) else None
            synopsis=r.xpath(self.synopsis_xpath.format(i))[0] if r.xpath(self.synopsis_xpath.format(i)) else None
            if title:
                title = title.replace("\n", "").replace("\t", "").strip()
            if href:
                href = href.replace("\n", "").replace("\t", "").strip()
                href = "{0}/{1}".format(self.base_url, href)
            if synopsis:
                synopsis = synopsis.replace("\n", "").replace("\t", "").strip()
            result.append(
                {
                    "title": title,
                    "href": href,
                    "synopsis": synopsis,
                }
            )
        return result

    def update(self, test=False):
        try:
            add_news = list()
            result = list()
            try:
               response = self.get_response_text()
               if not response:
                   self.logger.error("{0} requets error response is None".format(self.script_name))
                   return
            except:
                self.logger.error("{0} requets error :{1}".format(self.script_name, traceback.format_exc()))
                return
            try:
                add_news = self.parse(response, test=test)
            except:
                self.logger.error("{0} find: {1}".format(self.script_name, traceback.format_exc()))
            for new in add_news:
                title = new.get("title")
                href =new.get("href", "")
                synopsis = new.get("synopsis", "")
                cover_url = new.get("cover_url", "")
                hash_code = self.get_hash_code(title)
                if self.is_repeat(hash_code):
                    self.logger.debug("repeat: {0}".format(title))
                    continue
                self.logger.info("{0} find: {1}".format(self.script_name, title))
                self.logger.info("{0} find: {1}".format(self.script_name, href))
                self.logger.info("{0} find: {1}".format(self.script_name, synopsis))
                self.logger.info("{0} find: {1}".format(self.script_name, cover_url))
                result.append(News(
                    title=title,synopsis=synopsis,
                    script_name=self.script_name,
                    source=self.source, href=href, 
                    source_url=self.source_url,
                    new_type=self.new_type,
                    cover_url=cover_url,
                    hash_code=hash_code))
                if test:
                    break
        except Exception:
            self.logger.error(traceback.format_exc())
        try:
            self.logger.info("{0} add {1}".format(self.script_name, len(result)))
            for new in result:
                self.DBSession.add(new)
                
            self.DBSession.commit()
        except Exception:
            self.logger.error(traceback.format_exc())

