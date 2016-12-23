# -*- coding: utf-8 -*-

from __future__ import print_function
from bs4 import BeautifulSoup

import os
import datetime
import re
import csv
import time

try:
    from urllib.request import urlopen
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import urlopen
    from urllib2 import HTTPError


class AmebloScraper:

    def __init__(self, target_url, save_dir="./data"):
        self.target_url = target_url
        self.save_dir = save_dir

    def _make_soup(self, url):
        try:
            with urlopen(url) as response:
                html = response.read()
        except HTTPError as e:
            print("[ DEBUG ] in AmebloCrawler#make_soup: {}".format(e))
            return None

        return BeautifulSoup(html, "lxml")

    def scrap_article_text(self):

        soup = self._make_soup(self.target_url)

        # 日付情報の処理
        date = self.get_article_date(soup)
        # ブログ記事タイトルの取得
        title = self.get_article_title(soup)
        # ブログ記事本文を取得
        article = self.get_article_text(soup)

        return dict(date=date, title=title, article=article)

    def get_article_date(self, soup):
        date = soup.find("time").string
        d = datetime.datetime.strptime(date, '%Y年%m月%d日')
        return d.strftime('%Y-%m-%d')

    def get_article_title(self, soup):
        return soup.find(class_="skinArticleTitle").string.replace("\n", "").strip()

    def get_article_text(self, soup):
        law_article_text = soup.find(class_="articleText")

        # if len(law_article_text) == 0:
        #     print("[DEBUG] law_article_text is None")
        #     law_article_text = soup.find(class_="articleText").find_all("div")

        return self._clean_article_text(law_article_text)

    def save_scrap_dict(self, scrap_dict):

        # データの保存先が存在しない場合は作成
        if not os.path.isdir(self.save_dir):
            os.makedirs(self.save_dir)

        # ファイル名を定義
        csv_filename = self._convert_filename(self.target_url)
        csv_filename = "{}_{}_{}.csv".format(csv_filename, scrap_dict["date"], scrap_dict["title"].replace("/", ""))

        # スクレイピングしてきたデータをCSV形式で保存
        with open(os.path.join(self.save_dir, csv_filename), "w") as wf:
            writer = csv.writer(wf)

            for sentence in scrap_dict["article"]:
                writer.writerow([scrap_dict["date"], scrap_dict["title"], sentence])

    def scrap(self):
        scrap_dict = self.scrap_article_text()

        if scrap_dict is None:
            print("Can't find the text.")
        else:
            print("{}\n{}".format(scrap_dict["date"], scrap_dict["title"]))
            for sentence in scrap_dict["article"]:
                print(sentence)

            self.save_scrap_dict(scrap_dict)
            time.sleep(2)

    def _clean_article_text(self, law_article_text):

        # 取得したHTMLファイル内のbrタグを改行文字に変更
        # article_text = "\n".join(law_article_text)
        article_text_list = [lat.replace("\n", "") for lat in law_article_text.stripped_strings]
        article_text_list = [sentence.replace(u"\xa0", "") for sentence in article_text_list]

        # 不要な文字列を改行文字に変更
        # article_text = article_text.replace(u"\xa0", "\n")

        # 改行文字で文字列を区切り、リストに変更
        # article_text_list = article_text.split("\n")

        # リスト内に要素が存在しないものを取り除く
        while article_text_list.count("") > 0:
            article_text_list.remove("")

        return article_text_list

    def _convert_filename(self, url):
        filename = re.search('^http:\/\/ameblo.jp\/(.*?)\/', url)
        return filename.group(1)
