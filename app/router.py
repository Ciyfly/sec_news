#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-10 23:04:42
LastEditors: Recar
LastEditTime: 2021-01-12 23:53:42
'''
from . import app
from flask import render_template
from app.models import News

@app.route("/")
def index():
    datas = News.query.all()
    return render_template("index.html", datas=datas)