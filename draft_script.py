# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import time
import csv
import datetime

html = urlopen("http://ameblo.jp/ogurayui-0815/page-2.html")
soup = BeautifulSoup(html.read(), "lxml")

date = soup.find('time').string
d = datetime.datetime.strptime(date, '%Y年%m月%d日')
date_string = d.strftime('%Y-%m-%d')

title = soup.find(class_="skinArticleTitle").string
title

lawArticleTexts = soup.find("div", {"class": "articleText"})

articleTexts = "\n".join(lawArticleTexts.strings)
articleTexts = articleTexts.replace(u"\xa0", "\n")
articleTexts = articleTexts.split('\n')

while articleTexts.count("") > 0:
    articleTexts.remove("")

for articleText in articleTexts:
    print(articleText)

csvFile = open("data.csv", 'w+', newline='', encoding='utf-8')

try:
    writer = csv.writer(csvFile)
    writer.writerow(('date', 'article'))

    for articleText in articleTexts:
        writer.writerow((date_string, articleText))
finally:
    csvFile.close()
