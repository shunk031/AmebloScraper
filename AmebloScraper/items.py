# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmebloscraperItem(scrapy.Item):

    article_url = scrapy.Field()
    article_title = scrapy.Field()
    article_datetime = scrapy.Field()
    article_body = scrapy.Field()

    image_urls = scrapy.Field()
    images = scrapy.Field()
