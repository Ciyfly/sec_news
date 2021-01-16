#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-12 23:38:09
LastEditors: Recar
LastEditTime: 2021-01-16 11:17:45
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(base_dir, "../", 'news.db')
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True

db = SQLAlchemy(app)

from app import router