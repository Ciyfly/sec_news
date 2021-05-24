#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-10 23:04:42
LastEditors: recar
LastEditTime: 2021-05-24 11:38:58
'''
from . import app
from flask import render_template
from app.models import News, Company, Domain
import datetime

@app.route("/")
@app.route("/list/<int:page>")
def index(page=1):
    pagination = News.query.filter(News.new_type==0).order_by(News.update_time.desc()).paginate(page=page, per_page=20)
    datas = pagination.items
    current_time = datetime.datetime.now()
    return render_template("index.html", datas=datas, pagination=pagination, current_time=current_time)

@app.route("/loophole")
@app.route("/loophole/<int:page>")
def loophole(page=1):
    pagination = News.query.filter(News.new_type==1).order_by(News.update_time.desc()).paginate(page=page, per_page=20)
    datas = pagination.items
    current_time = datetime.datetime.now()
    return render_template("loophole.html", datas=datas, pagination=pagination, current_time=current_time)

@app.route("/subdomain")
@app.route("/subdomain/<int:page>")
def subdomain(page=1):
    companys = Company.query.all()
    current_time = datetime.datetime.now()
    return render_template("subdomain.html", companys=companys, current_time=current_time)


@app.route("/company/")
def company(id=1):
    domains = Domain.query.filter(Domain.company_id==id).order_by(Domain.update_time.desc()).all()
    return render_template("subdomain_info.html", domains=domains)


