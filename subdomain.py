#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-18 23:27:13
LastEditors: Recar
LastEditTime: 2021-01-24 13:37:11
'''

# 拿出来所有的domain 然后交给子域名脚本获取json判断并入库
from scripts.models import Company, Domain
from y_subdomain.lib.core import EngineScan, ExhaustionScan
from resv import Resvars
import os

class Subdomain():
    def __init__(self, debug=False):
        self.resv = Resvars()
        self.DBSession = self.resv.DBSession
        self.debug = debug
        self.load_company()
        self.load_domain()
        
    def load_domain(self):
        self.db_domains = dict()
        domains = self.DBSession.query(Domain).all()
        for data in domains:
            subdomain = data.domain
            self.db_domains[subdomain] = subdomain

    def load_company(self):
        companys = self.DBSession.query(Company).all()
        self.companys = companys

    def run_subdomain(self, company):
        domain_ips_dict = dict()
        engine_domain_ips_dict = dict()
        exh_domain_ips_dict = dict()
        # 接口
        if not self.debug:
            engine_scan = EngineScan([company])
            engine_domain_ips_dict = engine_scan.run()
        # 爆破
        if self.debug:
            base_path = os.path.dirname(os.path.abspath(__file__))
            sub_dict = os.path.join(base_path, "y_subdomain", "config", "test_sub.txt")
            exhaustion_scan =  ExhaustionScan(company, thread_count=100, sub_dict=sub_dict)
        else:
            exhaustion_scan =  ExhaustionScan(company, thread_count=100)
        exh_domain_ips_dict = exhaustion_scan.run()
        
        domain_ips_dict.update(engine_domain_ips_dict)
        domain_ips_dict.update(exh_domain_ips_dict)
        return domain_ips_dict

    def insert(self, subdomain, company, ips):
        Domain.add(subdomain, ips, company.id, self.resv.DBSession)

    def get_new_domain(self, domain_ips_dict, company):
        for domain in domain_ips_dict.keys():
            if domain not in self.db_domains:
                print("get new domain: {0}".format(domain))
                ips = ",".join(domain_ips_dict[domain])
                self.insert(domain, company, ips)

    def run(self):
        for company in self.companys:
            print("load {0}".format(company.domain_name))
            domain_ips_dict = self.run_subdomain(company.domain)
            self.get_new_domain(domain_ips_dict, company)

def run():
    logger.info('start')
    Subdomain(debug=True).run()
    logger.info('end')

if __name__ == '__main__':
    resv = Resvars()
    schedule.every(resv.subdomain_time).seconds.do(run)
    while True:
        schedule.run_pending()
        time.sleep(1)
