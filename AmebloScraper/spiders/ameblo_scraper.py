# -*- coding: utf-8 -*-

import scrapy
from AmebloScraper.items import AmebloscraperItem


class AmebloScraperBaseSpider(scrapy.Spider):
    name = 'ameblo_base_scraper'
    allowed_domains = ['ameblo.jp']
    start_urls = ['https://ameblo.jp/']

    elements = {
        'article_url': 'article div.skinArticleHeader h1 a::attr("href")',
        'article_title': 'article div.skinArticleHeader h1 a::text',
        'article_datetime': 'article span.articleTime time::text',
        'article_body': 'article div.skinArticleBody div.articleText ::text',
        'next_page': 'article div.pagingArea a.pagingNext::attr("href")',
    }

    def parse(self, response):

        urls = response.css(self.elements['article_url']).extract()
        for url in urls:
            yield scrapy.Request(response.urljoin(url), self.parse_articles)

        next_page = response.css(self.elements['next_page']).extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), self.parse)

    def parse_articles(self, response):

        item = AmebloscraperItem()
        item['article_url'] = response.url
        item['article_title'] = response.css(self.elements['article_title']).extract_first()
        item['article_datetime'] = response.css(self.elements['article_datetime']).extract_first()
        item['article_body'] = response.css(self.elements['article_body']).extract()

        yield item


class AmebloScraperSpider(AmebloScraperBaseSpider):
    name = 'ameblo_scraper'

    def __init__(self, *args, **kwargs):
        super(AmebloScraperSpider, self).__init__(*args, **kwargs)

        self.start_urls = [kwargs.get('start_url')]
