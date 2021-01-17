#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-09 22:58:52
LastEditors: Recar
LastEditTime: 2021-01-17 23:40:02
'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer, String, Text, Date, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from datetime import datetime

Base_model = declarative_base()

class News(Base_model):
     __tablename__ = 'news'
     id = Column(Integer, primary_key=True)
     title = Column(String(255))
     create_time = Column(DateTime, default=datetime.now())
     update_time = Column(DateTime, default=datetime.now())
     source = Column(String(255))
     source_url = Column(String(255))
     href = Column(String(255))
     script_name = Column(String(255))
     synopsis = Column(String(255))
     new_type =  Column(Integer, default=0)
    # def __repr__(self):
    #     return str({
    #         "id":self.id,
    #         "title": self.title,
    #         "create_time": self.create_time,
    #         "update_time": self.update_time,
    #         "source": self.source,
    #         "href": self.href,
    #         "script_name": script_name
    #     })