# AmebloScraper

Scraper for [Ameblo](https://ameblo.jp/) in Scrapy.

## Requirements

* Python 3.5.1
* Scrapy 1.4.0

## How to run

crawl https://ameblo.jp/TARGET_BLOG and output blog.json

``` shell
scrapy crawl ameblo_scraper -a start_url='https://ameblo.jp/TARGET_BLOG' -o blog.json
```
