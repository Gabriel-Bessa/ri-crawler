# -*- coding: utf-8 -*-
import scrapy


class ScieloArticlesSpider(scrapy.Spider):
    name = 'scielo-articles'
    allowed_domains = ['http://www.scielo.br']
    start_urls = ['http://scielo.com/'  ]

    def parse(self, response):
        pass
