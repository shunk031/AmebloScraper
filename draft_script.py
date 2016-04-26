# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import time
import csv

html = urlopen("http://ameblo.jp/ogurayui-0815/page-2.html")
soup = BeautifulSoup(html.read(), "lxml")

date = soup.find('time').string
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
        writer.writerow((date, articleText))
finally:
    csvFile.close()
