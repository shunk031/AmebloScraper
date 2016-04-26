# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import time

html = urlopen("http://ameblo.jp/ogurayui-0815/")
soup = BeautifulSoup(html, "lxml")

nextPage = soup.find("a", {"class": "apagingNext"})

print(nextPage)

print(nextPage is not None)

if 'href' in nextPage.attrs:
    print(nextPage.attrs['href'])
