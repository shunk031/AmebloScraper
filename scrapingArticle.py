# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup


def scrapingArticleText(url):
    """
    引数から得たURLからブログ本文を取得して
    一文ずつ区切ったstringのlistをreturnする
    """
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        return None
    try:
        soup = BeautifulSoup(html.read(), "lxml")
        lawArticleText = ""

        date = soup.find('time').string

        for i in soup.findAll("", {"class": "articleText"}):
            lawArticleText += i.get_text()

        articleText = lawArticleText.replace(u"\xa0", "\n")
        articleText = articleText.split("\n")

        while articleText.count("") > 0:
            articleText.remove("")

    except AttributeError as e:
        return None

    return dict(date=date, article=articleText)


def main():
    url = "http://ameblo.jp/ogurayui-0815/entry-12145717070.html"
    result = scrapingArticleText(url)

    if result == None:
        print("Can't find the text")

    else:
        print(result['date'])

        for i in result['article']:
            print(i)


if __name__ == '__main__':
    main()
