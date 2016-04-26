# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import time
import csv


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
        lawArticleTexts = soup.find("div", {"class": "articleText"})

        articleTexts = cleanArticleTexts(lawArticleTexts)

    except AttributeError as e:
        return None

    return dict(date=date, article=articleTexts)


def cleanArticleTexts(lawArticle):
    """
    記事データをクリーニングする
    """

    cleanTexts = "\n".join(lawArticle.strings)
    cleanTexts = cleanTexts.replace(u"\xa0", "\n")
    cleanTexts = cleanTexts.split("\n")

    while cleanTexts.count("") > 0:
        cleanTexts.remove("")

    return cleanTexts


def saveArticleTexts(articleTexts):
    """
    date, articleTextを保持する辞書を受け取り、
    CSVファイルにアウトプットする
    """

    csvFile = open("data.csv", 'w+', newline='', encoding='utf-8')

    try:
        writer = csv.writer(csvFile)
        writer.writerow(('date', 'article'))

        for articleText in articleTexts['article']:
            writer.writerow((articleTexts['date'], articleText))

    finally:
        csvFile.close()


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
        results = scrapingArticleText(nextPage.attrs['href'])

        if results == None:
            print("Can't find the text")

        else:
            print(results['date'])

            for result in results['article']:
                print(result)

            saveArticleTexts(results)
            crawler(nextPage.attrs['href'])


def main():

    crawler("http://ameblo.jp/ogurayui-0815/")
    print("Finish!")

if __name__ == '__main__':
    main()
