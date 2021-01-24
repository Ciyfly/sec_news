#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-09 22:58:52
LastEditors: Recar
LastEditTime: 2021-01-24 09:54:49
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

class Company(Base_model):
     __tablename__ = 'company'
     id = Column(Integer, primary_key=True)
     domain_name = Column(String(255))
     domain = Column(String(255))
     icon_url = Column(String(255))
     create_time = Column(DateTime, default=datetime.now)
     update_time = Column(DateTime, default=datetime.now)
     subdomain_domains = relationship("Domain", backref='company')
     
     def add(domain_name, domain, icon_url, session):
          company = Company(domain_name=domain_name, domain=domain, icon_url=icon_url)
          session.add(company)
          session.commit()
          return company

     def get_all(session):
          result_list = [str(company) for company in session.query(Company).all()]
          return result_list

     def get_domains_byname(session, name):
          company = session.query(Company).filter(Company.domain_name==name).first()
          if company:
               return company.subdomain_domains

     def __str__(self):
          return str({
               "id": self.id,
               "domain_name": self.domain_name,
               "domain": self.domain,
               "icon_url": self.icon_url,
               "create_time": datetime.strftime(self.create_time, "%Y-%m-%d %H:%M"),
               "update_time": datetime.strftime(self.update_time, "%Y-%m-%d %H:%M"),
          })



class Domain(Base_model):
     __tablename__ = 'domain'
     id = Column(Integer, primary_key=True)
     domain_base = Column(String(255))
     domain = Column(String(255))
     ips = Column(Text())
     company_id = Column(Integer, ForeignKey('company.id'))
     create_time = Column(DateTime, default=datetime.now)
     update_time = Column(DateTime, default=datetime.now)
     company = ForeignKey('company', nullable=False, unique=True)

     def add(domain, ips, company_id, session):
          domain_base = ".".join(domain.split(".")[-2:])
          domain = Domain(
               domain_base=domain_base,
               domain=domain, ips=ips,
               company_id=company_id)
          session.add(domain)
          session.commit()
          return domain

     def get_all(session):
          result_list = [str(domain) for domain in session.query(Domain).all()]
          return result_list

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
