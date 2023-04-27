import json

import scrapy
import urllib.parse
import uuid
import os

def getIndex(index):
    return str(index + 1)


def isFileEmpty(path):
    return os.path.getsize(path) == 0

def save(items):
    demiliter = "#"
    path = "response.csv"
    f = open(path, 'a+')

    if isFileEmpty(path):
        f.write(f"id{demiliter}title{demiliter}link{demiliter}authors{demiliter}authorsLinks\n")

    for item in items:
        f.write(f"{item['id']}{demiliter}{item['title']}{demiliter}{item['link']}{demiliter}{item['authors']}{demiliter}{item['authorsLinks']}\n")
    f.close()


def getNextUrl(url):
    url_parts = urllib.parse.urlparse(url)
    query = dict(urllib.parse.parse_qsl(url_parts.query))
    params = {'page': int(query['page']) + 1, 'from': int(query['from']) + 100}
    query.update(params)
    return url_parts._replace(query=urllib.parse.urlencode(query)).geturl()


class ScieloSpider(scrapy.Spider):
    name = 'scielo'
    start_urls = ['https://search.scielo.org/?fb=&q=&lang=pt&count=100&from=1&output=site&sort=&format=summary&page=1&where=&filter%5Bin%5D%5B%5D=scl&filter%5Bla%5D%5B%5D=pt']

    def parse(self, response):
        items = []
        for i, item in enumerate(response.xpath("//div[@class='results']/div[@class='item']/div[2]")):
            title = item.xpath(f"(//div[@class='line']//strong)[{getIndex(i)}]/text()").extract()
            link = item.xpath(f"(//img[@data-toggle='tooltip']/following-sibling::a)[{getIndex(i)}]/@href").get()
            authors = item.xpath(f"(//div[@class='line']/following-sibling::div[@class='line authors'])[{getIndex(i)}]//a[@class='author']/text()").extract()
            authorsLinks = item.xpath(f"(//div[@class='line']/following-sibling::div[@class='line authors'])[{getIndex(i)}]//a[@class='author']/@href").extract()
            items.append({
                'id': str(uuid.uuid4()),
                'title': title,
                'link': link,
                'authors': authors,
                'authorsLinks': authorsLinks
            })
        save(items)
        hasNext = response.xpath("(//a[@class='pageNext'])[2]")
        if hasNext:
            yield scrapy.Request(getNextUrl(response.request.url), callback=self.parse)
