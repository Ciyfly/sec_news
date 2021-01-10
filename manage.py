#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-10 14:07:38
LastEditors: Recar
LastEditTime: 2021-01-10 16:33:17
'''
from main import Resvars
from scripts.models import Base_model
from scripts.models import News
from log import logger
from lxml import etree
import traceback
import requests
import click

class Manager(Resvars):
    def __init__(self):
        super(Manager,self).__init__()   

    def init_db(self):
        Base_model.metadata.create_all(self.engine)

    def dropdb(self):
        Base_model.metadata.drop_all(self.engine)

    def test_gitlab_advisories(self):
        try:
            # 直接插入最新的一条
            html = requests.get("https://github.com/advisories").content
            r=etree.HTML(html)
            title_base = '//*[@id="js-pjax-container"]/div/div[2]/div[5]/div/div[2]/div/a/text()'
            href_base = '//*[@id="js-pjax-container"]/div/div[2]/div[5]/div/div[2]/div/a/@href'
            synopsis_base = '//*[@id="js-pjax-container"]/div/div[5]/div[2]/div/div[2]/div/div/span[1]/text()'
            title=r.xpath(title_base)[0] if r.xpath(title_base) else None
            href=r.xpath(href_base)[0] if r.xpath(href_base) else None
            synopsis=r.xpath(synopsis_base)[0] if r.xpath(synopsis_base) else None
            if title:
                title = title.replace("\n", "").replace("\t", "").strip()
            if href:
                href = href.replace("\n", "").replace("\t", "").strip()
                href = "https://github.com{0}".format(href)
            if synopsis:
                synopsis = synopsis.replace("\n", "").replace("\t", "").strip()
            logger.info("test_gitlab_advisories find: {0}".format(title))
            logger.info("test_gitlab_advisories find: {0}".format(href))
            logger.info("test_gitlab_advisories find: {0}".format(synopsis))
            new = News(
                title=title,synopsis=synopsis,
                script_name="gitlab_advisories",
                source="https://github.com/advisories", href=href)
            self.DBSession.add(new)
            self.DBSession.commit()
        except Exception:
            self.logger.error(traceback.format_exc())

    def test_aliyun_xz(self):
        try:
            # 直接插入最新的一条
            html = requests.get("https://xz.aliyun.com/").content.decode("utf-8").strip()
            r=etree.HTML(html)
            title_base = '//*[@id="includeList"]/table/tr[8]/td/p[1]/a/text()'
            href_base = '//*[@id="includeList"]/table/tr[8]/td/p[1]/a/@href'
            synopsis_base = '//*[@id="includeList"]/table/tr[8]/td/p[2]/a[2]/text()'
            title=r.xpath(title_base)[0] if r.xpath(title_base) else None
            href=r.xpath(href_base)[0] if r.xpath(href_base) else None
            synopsis=r.xpath(synopsis_base)[0] if r.xpath(synopsis_base) else None
            if title:
                title = title.replace("\n", "").replace("\t", "").strip()
            if href:
                href = href.replace("\n", "").replace("\t", "").strip()
                href = "https://xz.aliyun.com/{0}".format(href)
            if synopsis:
                synopsis = synopsis.replace("\n", "").replace("\t", "").strip()
            logger.info("test_aliyun_xz find: {0}".format(title))
            logger.info("test_aliyun_xz find: {0}".format(href))
            logger.info("test_aliyun_xz find: {0}".format(synopsis))
            new = News(
                title=title,synopsis=synopsis,
                script_name="aliyun_xz",
                source="https://xz.aliyun.com", href=href)
            self.DBSession.add(new)
            self.DBSession.commit()
        except Exception:
            self.logger.error(traceback.format_exc())

manager = Manager()

@click.group()
def cli():
    pass

@click.command()
def initdb():
    manager.init_db()
    click.echo('init db')

@click.command()
def dropdb():
    manager.dropdb()
    click.echo('drop db')

@click.command()
def test():
    click.echo('test')

@click.command()
def test_gitlab_advisories():
    manager.test_gitlab_advisories()
    click.echo('test_gitlab_advisories')

@click.command()
def test_aliyun_xz():
    manager.test_aliyun_xz()
    click.echo('test_aliyun_xz')

cli.add_command(initdb)
cli.add_command(dropdb)
cli.add_command(test)
cli.add_command(test_gitlab_advisories)
cli.add_command(test_aliyun_xz)

if __name__ == "__main__":
    cli()