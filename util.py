#!/usr/bin/python
# coding=utf-8
'''
Date: 2021-01-07 12:00:26
LastEditors: recar
LastEditTime: 2021-01-07 12:06:48
'''
from difflib import SequenceMatcher


class Util():
    # 计算页面相似度
    @ staticmethod
    def get_ischange(one_html, two_html):
        def _remove_redundant_strings(html):
            # 把html标签去除掉
            if html:
                return html.replace('<.*?>', '').replace('\n', '').replace('\t', '') # noqa E501
            else:
                return html
        one_html = _remove_redundant_strings(one_html)
        two_html = _remove_redundant_strings(two_html)
        seq = SequenceMatcher(None, one_html, two_html)
        ratio = seq.ratio()
        if ratio < 0.95:
            return True
        else:
            return False

