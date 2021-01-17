#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-10 23:04:42
LastEditors: Recar
LastEditTime: 2021-01-18 00:06:07
'''
from . import app
from flask import render_template
from app.models import News

@app.route("/")
@app.route("/list/<int:page>")
def index(page=1):
    pagination = News.query.filter(News.new_type==0).order_by(News.update_time.desc()).paginate(page=page, per_page=20)
    datas = pagination.items
    return render_template("index.html", datas=datas, pagination=pagination)

@app.route("/loophole")
@app.route("/loophole/<int:page>")
def loophole(page=1):
    pagination = News.query.filter(News.new_type==1).order_by(News.update_time.desc()).paginate(page=page, per_page=20)
    datas = pagination.items
    return render_template("loophole.html", datas=datas, pagination=pagination)

@app.route("/subdomain")
@app.route("/subdomain/<int:page>")
def subdomain(page=1):
    pagination = News.query.order_by(News.update_time.desc()).paginate(page=page, per_page=20)
    datas = pagination.items
    return render_template("subdomain.html", datas=datas, pagination=pagination)


