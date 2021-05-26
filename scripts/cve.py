#!/usr/bin/python
# coding=utf-8
'''
Date: 2021-05-24 16:37:17
LastEditors: recar
LastEditTime: 2021-05-26 15:52:03
'''
from scripts.base import Base
from lxml import etree
import traceback


class Spider(Base):
    def __init__(self, resv):
        super(Spider, self).__init__(resv)
        self.script_name = "cve"
        self.source = "CVE"
        self.source_url = "https://cassandra.cerias.purdue.edu/CVE_changes/today.html"
        self.url = "https://cassandra.cerias.purdue.edu/CVE_changes/today.html"
        self.base_url = "https://cve.mitre.org/"
        self.title_xpath = '/html/body/a[{0}]/text()'
        self.href_xpath = '/html/body/a[{0}]/@href'
        self.synopsis_xpath = '//*[@id="GeneratedTable"]/table/tbody/tr[4]/td/text()'
        self.new_type = 1

    def parse(self, response, test=False):
        result = list()
        if not response:
            return result
        max_size = 50
        frist_size = 2
        init_size = 1
        r=etree.HTML(response)
        if not test:
            range_size = max_size
        else:
            range_size = frist_size
        for i in range(init_size, range_size):
            title=r.xpath(self.title_xpath.format(i))[0] if r.xpath(self.title_xpath.format(i)) else None
            href=r.xpath(self.href_xpath.format(i))[0] if r.xpath(self.href_xpath.format(i)) else None
            hash_code = self.get_hash_code(title)
            if self.is_repeat(hash_code):
                continue
            synopsis = ""
            if href:
                info_html = self.get_response_text(url=href)
                if info_html:
                    r_info=etree.HTML(info_html)
                    synopsis=r_info.xpath('//*[@id="GeneratedTable"]/table//text()')[22]
                    title=r_info.xpath('//*[@id="GeneratedTable"]/table//text()')[7]
            if title:
                title = title.replace("\n", "").replace("\t", "").strip()
                if "CVE" not in title:
                    title = "CVE-"+title
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

    def run(self):
        self.logger.info("update CVE")
        self.update()