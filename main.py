import threading
from fastapi import FastAPI
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

from ri_final.spiders.scielo_articles import ScieloArticlesSpider

app = FastAPI()
settings = get_project_settings()
process = CrawlerProcess(settings)


def run_crawler():
    process.crawl(ScieloArticlesSpider)
    process.start()


@app.get("/run-script")
async def read_root():
    thread = threading.Thread(target=run_crawler)
    thread.start()
    return {"crawled": True}
