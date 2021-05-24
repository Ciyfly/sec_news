#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2021-01-10 14:07:38
LastEditors: recar
LastEditTime: 2021-05-24 18:02:39
'''
from resv import Resvars
from spider import SpiderSec
from scripts.models import Base_model
from scripts.models import News, Company, Domain
from scripts.gitlab_advisories import Spider as gitlab_advisorie_spider
from scripts.cve import Spider as cve_spider
from scripts.aliyun_xz import Spider as aliyun_xz_spider
from scripts.freebuf import Spider as freebuf_spider
from log import logger
from lxml import etree
import traceback
import requests
import click

class Manager(Resvars):
    def __init__(self):
        super(Manager,self).__init__()   

    def init_db(self):
        Base_model.metadata.create_all(self.engine)

    def dropdb(self):
        Base_model.metadata.drop_all(self.engine)

    def get_first_gitlab_advisories(self):
        gitlab_advisorie_spider(self).update_new(test=True)

    def get_first_cve_spider(self):
        cve_spider(self).update_new(test=True)


    def get_first_aliyun_xz(self):
        aliyun_xz_spider(self).update_new(test=True)

    def get_first_freebuf(self):
        freebuf_spider(self).update_new(test=True)

    def insert_compamy(self, name, domain, icon_url):
        Company.add(name, domain, icon_url, self.DBSession)

    def get_compamy_all(self):
        company_list = Company.get_all(self.DBSession)
        return company_list

    def test_insert_domain(self,domain, ips, company_id):
        Domain.add(domain, ips, company_id, self.DBSession)

    def get_domain_all(self):
        return Domain.get_all(self.DBSession)

    def get_domain_byname(self, name):
        return Company.get_domains_byname(self.DBSession, name)

manager = Manager()

@click.group()
def cli():
    pass

@click.command()
def initdb():
    manager.init_db()
    click.echo('init db')

@click.command()
def dropdb():
    manager.dropdb()
    click.echo('drop db')

@click.command()
def test():
    click.echo('test')

@click.command()
def test_gitlab_advisories():
    manager.get_first_gitlab_advisories()
    click.echo('test_gitlab_advisories')

@click.command()
def test_cve_spider():
    manager.get_first_cve_spider()
    click.echo('get_first_cve_spider')

@click.command()
def test_aliyun_xz():
    manager.get_first_aliyun_xz()
    click.echo('test_aliyun_xz')

@click.command()
def test_freebuf():
    manager.get_first_freebuf()
    click.echo('test_freebuf')

@click.command()
def test_run():
    SpiderSec(manager).run()
    click.echo('test_run')

@click.command()
@click.option("--name", required=True)
@click.option("--domain", required=True)
@click.option("--icon_url", required=True)
def insert_compamy(name, domain, icon_url):
    manager.insert_compamy(name, domain, icon_url)
    click.echo('insert Company')

@click.command()
def get_compamy_all():
    company_list = manager.get_compamy_all()
    click.echo(str(company_list))

@click.command()
@click.option("--domain", required=True)
@click.option("--ips", required=True)
@click.option("--company_id", required=True)
def test_insert_domain(domain, ips, company_id):
    manager.test_insert_domain(domain, ips, company_id)
    click.echo('insert domain')

@click.command()
def get_domain_all():
    domain_list = manager.get_domain_all()
    click.echo(str(domain_list))


@click.command()
@click.option("--name", required=True)
def get_domain_byname(name):
    domains = manager.get_domain_byname(name)
    domains = [str(domain) for domain in domains]
    click.echo(str(domains))

cli.add_command(initdb)
cli.add_command(dropdb)
cli.add_command(test)
cli.add_command(test_gitlab_advisories)
cli.add_command(test_cve_spider)
cli.add_command(test_aliyun_xz)
cli.add_command(test_freebuf)
cli.add_command(test_run)
cli.add_command(insert_compamy)
cli.add_command(get_compamy_all)
cli.add_command(test_insert_domain)
cli.add_command(get_domain_all)
cli.add_command(get_domain_byname)

if __name__ == "__main__":
    cli()