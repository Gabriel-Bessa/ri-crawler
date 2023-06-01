# -*- coding: utf-8 -*-
import json
import scrapy
import requests


def saveItems(items, articleId):
    URL = "http://localhost:8080/v1/article-section/receive"
    body = json.dumps({
        'articleId': articleId,
        'sections': items
    })
    r = requests.post(url=URL, params={}, data=body, headers={'Content-Type': 'application/json'})
    pass

def getArticles():
    quantity = 100
    links = []
    URL = f"http://localhost:8080/v1/article/not-crawled?size={quantity}"
    r = requests.get(url=URL, params={})
    for i, item in enumerate(r.json()['content']):
        links.append({'link': item['link'], 'id': item['id']})
    return links


class ScieloArticlesSpider(scrapy.Spider):
    name = 'scielo-articles'
    teste = getArticles()

    def start_requests(self):
        for item in getArticles():
            yield scrapy.Request(item['link'], self.parse, meta={'id': item['id']})

    def parse(self, response):
        currentId = response.meta['id']
        items = []
        for i, item in enumerate(response.xpath('//div[@class="articleSection"]')):
            section = item.xpath(f"((//div[@class='articleSection']//h1)[{i + 1}])/text()").extract()
            is_filled_with_empty_strings = all(element == "" for element in section)
            if is_filled_with_empty_strings:
                section = ""
            else:
                section = section[0]
            paragraphs = item.xpath(f"//div[@class='articleSection'][{i + 1}]//p/text()").extract()
            if paragraphs:
                items.append({
                    'section': section,
                    'paragraphs': paragraphs
                })
        saveItems(items, currentId)
        pass
