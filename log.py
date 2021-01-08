#!/usr/bin/python
# coding=utf-8
'''
Date: 2021-01-07 11:34:05
LastEditors: recar
LastEditTime: 2021-01-07 11:39:43
'''
#!/usr/bin/python
# coding=UTF-8

import logging.handlers
import configparser
import logging
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


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
log_file_path = os.path.join(base_path, "log", "spider_sec.log")
logger = get_logger(level=level, log_file=log_file_path, log_name="spider_sec")
