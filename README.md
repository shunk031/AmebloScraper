# Ameblo Crawler

Easily crawl and scrape [Ameblo](http://ameblo.jp/).

## Dependency

* BeautifulSoup4
* lxml

## Usage

``` python
from ameblo_crawler.crawler import AmebloCrawler

target_url = "http://ameblo.jp/foo/"
save_dir = "/path/to/save/dir"

crawler = AmebloCrawler(target_url, save_dir)
crawler.crawl()
```
