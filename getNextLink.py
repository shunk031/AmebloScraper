# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://ameblo.jp/ogurayui-0815/")
soup = BeautifulSoup(html, "lxml")

nextPage = soup.find("a", {"class": "pagingNext"})

if 'href' in nextPage.attrs:
    print(nextPage.attrs['href'])
