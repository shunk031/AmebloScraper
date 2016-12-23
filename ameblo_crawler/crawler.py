# -*- coding: utf-8 -*-

from __future__ import print_function
from ameblo_crawler.scraper import AmebloScraper
from bs4 import BeautifulSoup

try:
    from urllib.request import urlopen
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import urlopen
    from urllib2 import HTTPError


class AmebloCrawler:

    def __init__(self, target_url, save_dir="./data"):
        self.target_url = target_url
        self.before_url = None
        self.save_dir = save_dir

    def make_soup(self, url):
        try:
            with urlopen(url) as response:
                html = response.read()
        except HTTPError as e:
            print("[ DEBUG ] in AmebloCrawler#make_soup: {}".format(e))
            return None

        return BeautifulSoup(html, "lxml")

    def get_next_page_link(self, url):

        self.before_url = url
        soup = self.make_soup(self.target_url)
        next_page_tag = soup.find("a", {"class": "pagingNext"})

        # 次ページヘのリンクが存在し、タグ内にリンクアドレスが存在する場合
        if next_page_tag is not None and "href" in next_page_tag.attrs:
            next_page_link = next_page_tag.attrs["href"]

            # 前ページと現在のページのURLが違う場合
            if self.before_url != next_page_link:
                print("\n{}".format(next_page_link))
                return next_page_link
            else:
                return None
        else:
            return None

    def crawl(self):

        while True:
            scraper = AmebloScraper(self.target_url)
            scraper.scrap()
            self.target_url = self.get_next_page_link(self.target_url)

            # 次ページがない場合は終了
            if self.target_url is None:
                break

        print("Finish!")
