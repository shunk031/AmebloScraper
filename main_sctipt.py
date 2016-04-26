# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import time


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

        date = soup.find('time').string
        lawArticleText = soup.find("div", {"class": "articleText"})

        articleText = cleanArticleText(lawArticleText)

    except AttributeError as e:
        return None

    return dict(date=date, article=articleText)


def cleanArticleText(lawArticle):

    cleanText = "\n".join(lawArticle.strings)
    cleanText = cleanText.replace(u"\xa0", "\n")
    cleanText = cleanText.split("\n")

    while cleanText.count("") > 0:
        cleanText.remove("")

    return cleanText


def crawler(url):
    """
    次の記事のリンクを再帰的に所得する
    """

    html = urlopen(url)
    soup = BeautifulSoup(html, "lxml")

    nextPage = soup.find("a", {"class": "pagingNext"})

    if nextPage is not None:

        if 'href' in nextPage.attrs:
            print(nextPage.attrs['href'])

        time.sleep(5)
        result = scrapingArticleText(nextPage.attrs['href'])

        if result == None:
            print("Can't find the text")

        else:
            print(result['date'])

            for i in result['article']:
                print(i)

            crawler(nextPage.attrs['href'])


def main():

    crawler("http://ameblo.jp/ogurayui-0815/")
    print("Finish!")

if __name__ == '__main__':
    main()
