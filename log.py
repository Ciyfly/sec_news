#!/usr/bin/python
# coding=utf-8
'''
Date: 2021-01-07 11:34:05
LastEditors: Recar
LastEditTime: 2021-01-10 14:25:11
'''
#!/usr/bin/python
# coding=UTF-8

import logging.handlers
import configparser
import logging
import os
import sys


def get_logger(console=True, log_file=None, level=logging.INFO, maxBytes=200*1024, backupCount=5, log_name='root'): # noqa E501
    # log_name 是用于区分 不然对于同一个log会不断 addHandler
    logger = logging.getLogger(log_name)
    logger.setLevel(level)
    formatter = logging.Formatter(
         '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S') # noqa #E501
    if log_file:
        # 使用FileHandler输出到文件
        fh = logging.handlers.RotatingFileHandler(log_file, maxBytes=maxBytes, backupCount=backupCount, encoding="utf-8") # noqa E501
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    if console:
        # 使用StreamHandler输出到屏幕
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        # 添加两个Handler
        logger.addHandler(ch)
    return logger


base_path = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(base_path, "log")
if not os.path.exists(log_dir):
    os.mkdir(log_dir)
log_file_path = os.path.join(log_dir, "spider_sec.log")
logger = get_logger(log_file=log_file_path, log_name="spider_sec")