#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-09 23:32:49
LastEditors: Recar
LastEditTime: 2021-01-10 16:28:22
'''
from scripts.gitlab_advisories import Spider as gitlab_advisorie_spider
from scripts.aliyun_xz import Spider as aliyun_xz_spider
from scripts.models import News
from main import Resvars

resv = Resvars()

def test_gitlab_advisorie_spider():
    gitlab_advisorie_spider(resv).run()

def test_aliyun_xz_spider():
    aliyun_xz_spider(resv).run()
# test_gitlab_advisorie_spider()
test_aliyun_xz_spider()
