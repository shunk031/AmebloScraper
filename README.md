# Ameblo Crawler

Easily crawl and scrape [Ameblo](http://ameblo.jp/).

## Dependency

* BeautifulSoup4
* lxml

## Install

``` shell
pip install git+https://github.com/shunk031/ameblo-crawler.git
```

## Usage

``` python
from ameblo_crawler.crawler import AmebloCrawler

target_url = "http://ameblo.jp/foo/"
save_dir = "/path/to/save/dir"

crawler = AmebloCrawler(target_url, save_dir)
crawler.crawl()
```
