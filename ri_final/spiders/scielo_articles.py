# -*- coding: utf-8 -*-
import scrapy


class ScieloArticlesSpider(scrapy.Spider):
    name = 'scielo-articles'
    allowed_domains = ['http://www.scielo.br']
    start_urls = ['http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0011-52582024000100206&lang=pt']

    def parse(self, response):
        pass
