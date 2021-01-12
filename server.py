#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-10 23:03:57
LastEditors: Recar
LastEditTime: 2021-01-12 23:45:46
'''

from app import app

if __name__ == "__main__":
    app.run("0.0.0.0", 5050, debug=True)

