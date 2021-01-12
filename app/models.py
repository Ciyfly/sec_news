#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-10 23:05:09
LastEditors: Recar
LastEditTime: 2021-01-12 23:50:13
'''
from app import db
from datetime import datetime
class News(db.Model):
     __tablename__ = 'news'
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(255))
     create_time = db.Column(db.DateTime, default=datetime.now)
     update_time = db.Column(db.DateTime, default=datetime.now)
     source = db.Column(db.String(255))
     href = db.Column(db.String(255))
     script_name = db.Column(db.String(255))
     synopsis = db.Column(db.String(255))
