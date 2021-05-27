#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-10 23:05:09
LastEditors: recar
LastEditTime: 2021-05-27 17:44:54
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
     cover_url = db.Column(db.String(255))
     source_url = db.Column(db.String(255))
     href = db.Column(db.String(255))
     script_name = db.Column(db.String(255))
     synopsis = db.Column(db.String(255))
     tag = db.Column(db.String(255))
     type_tags = db.Column(db.String(255))
     new_type =  db.Column(db.Integer, default=0)
     hash_code = db.Column(db.String(255))

class Company(db.Model):
     __tablename__ = 'company'
     id = db.Column(db.Integer, primary_key=True)
     domain_name = db.Column(db.String(255))
     domain = db.Column(db.String(255))
     icon_url = db.Column(db.String(255))
     create_time = db.Column(db.DateTime, default=datetime.now)
     update_time = db.Column(db.DateTime, default=datetime.now)
     subdomain_domains = db.relationship("Domain", backref='company')

     def __str__(self):
          return str({
               "id": self.id,
               "domain_name": self.domain_name,
               "domain": self.domain,
               "icon_url": self.icon_url,
               "create_time": datetime.strftime(self.create_time, "%Y-%m-%d %H:%M"),
               "update_time": datetime.strftime(self.update_time, "%Y-%m-%d %H:%M"),
          })


class Domain(db.Model):
     __tablename__ = 'domain'
     id = db.Column(db.Integer, primary_key=True)
     domain_base = db.Column(db.String(255))
     domain = db.Column(db.String(255))
     ips = db.Column(db.Text())
     company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
     create_time = db.Column(db.DateTime, default=datetime.now)
     update_time = db.Column(db.DateTime, default=datetime.now)
     company = db.ForeignKey('company', nullable=False, unique=True)

     def __str__(self):
          return str({
               "id": self.id,
               "domain_base": self.domain_base,
               "domain": self.domain,
               "ips": self.ips,
               "company_id": self.company_id,
               "create_time": datetime.strftime(self.create_time, "%Y-%m-%d %H:%M"),
               "update_time": datetime.strftime(self.update_time, "%Y-%m-%d %H:%M"),
          })