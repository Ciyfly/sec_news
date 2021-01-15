#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-10 23:04:42
LastEditors: Recar
LastEditTime: 2021-01-14 23:48:18
'''
from . import app
from flask import render_template
from app.models import News

@app.route("/")
@app.route("/list/<int:page>")
def index(page=1):
    pagination = News.query.order_by(News.update_time.desc()).paginate(page=page, per_page=20)
    datas = pagination.items
    return render_template("index.html", datas=datas, pagination=pagination)