#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-10 14:07:38
LastEditors: Recar
LastEditTime: 2021-01-10 22:35:50
'''
from main import Resvars
from scripts.models import Base_model
from scripts.models import News
from scripts.gitlab_advisories import Spider as gitlab_advisorie_spider
from scripts.aliyun_xz import Spider as aliyun_xz_spider
from scripts.freebuf import Spider as freebuf_spider
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

    def get_first_gitlab_advisories(self):
        gitlab_advisorie_spider(self).update_new(test=True)

    def get_first_aliyun_xz(self):
        aliyun_xz_spider(self).update_new(test=True)

    def get_first_freebuf(self):
        freebuf_spider(self).update_new(test=True)


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
    manager.get_first_gitlab_advisories()
    click.echo('test_gitlab_advisories')

@click.command()
def test_aliyun_xz():
    manager.get_first_aliyun_xz()
    click.echo('test_aliyun_xz')

@click.command()
def test_freebuf():
    manager.get_first_freebuf()
    click.echo('test_freebuf')


cli.add_command(initdb)
cli.add_command(dropdb)
cli.add_command(test)
cli.add_command(test_gitlab_advisories)
cli.add_command(test_aliyun_xz)
cli.add_command(test_freebuf)

if __name__ == "__main__":
    cli()