# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import time
import csv
import datetime
import sys


class AmebloCrawler:
    """
    アメブロをクロールするためのクラス定義
    """

    def __init__(self, targetUrl):
        self.targetUrl = targetUrl
        self.beforeUrl = targetUrl
        self.afterUrl = targetUrl

    def scrapingArticleText(self, url):
        """
        引数から得たURLからブログ本文を取得して
        日付、ブログタイトル、ブログ本文を
        一文ずつ区切ったstringのlistとディクショナリとして
        returnする
        """

        try:
            html = urlopen(url)
        except HTTPError as e:
            print(e)
            return None
        try:
            soup = BeautifulSoup(html.read(), "lxml")

            # 日付情報の処理
            date = soup.find('time').string
            d = datetime.datetime.strptime(date, '%Y年%m月%d日')
            date_string = d.strftime('%Y-%m-%d')

            # ブログ記事タイトルの取得
            titleText = soup.find(class_="skinArticleTitle").string

            # ブログ記事の取得
            lawArticleTexts = soup.find("div", {"class": "articleText"})

            # ブログ記事データをクリーニング
            articleTexts = self.cleanArticleTexts(lawArticleTexts)

        except AttributeError as e:
            return None

        # 投稿日時と記事内容を格納する辞書データをリターンする
        return dict(date=date_string, title=titleText, article=articleTexts)

    def cleanArticleTexts(self, lawArticle):
        """
        記事データをクリーニングする
        """
        # 取得したHTMLファイル中のbrタグを改行文字に変更
        cleanTexts = "\n".join(lawArticle.strings)
        # 不要な文字列を改行文字に変更
        cleanTexts = cleanTexts.replace(u"\xa0", "\n")
        # 改行文字で文字列を区切る
        cleanTexts = cleanTexts.split("\n")

        # リスト内に要素が存在しない場合は取り除く
        while cleanTexts.count("") > 0:
            cleanTexts.remove("")

        return cleanTexts

    def getNextPageLink(self, url):
        """
        ブログ本文から次のページへのリンクを取得する
        リンクが存在しない場合はNoneがreturnする
        """

        html = urlopen(url)
        soup = BeautifulSoup(html.read(), "lxml")

        nextPage = soup.find("a", {"class": "pagingNext"})

        if nextPage is not None:

            if 'href' in nextPage.attrs:
                nextPageLink = nextPage.attrs['href']
                print("\n" + nextPageLink)

                return nextPageLink
        else:
            return None

    def saveArticleTexts(self, articleTexts, filename):
        """
        date, articleTextを保持する辞書を受け取り、
        CSVファイルにアウトプットする
        ブログ毎に出力ファイル名をファイル名を変更する
        """

        csvFile = open(filename, 'a', newline='', encoding='utf-8')

        try:
            writer = csv.writer(csvFile)
            # writer.writerow(('date', 'article'))

            for articleText in articleTexts['article']:
                writer.writerow(
                    (articleTexts['date'], articleTexts['title'], articleText))

        finally:
            csvFile.close()

    def crawler(self, url, filename):
        """
        次の記事のリンクを再帰的に所得する
        """
        results = self.scrapingArticleText(url)

        if results is None:
            print("Can't find the text")

        else:
            print(results['date'])
            print(results['title'])
            for result in results['article']:
                print(result)

            self.saveArticleTexts(results, filename)

            time.sleep(5)


def main():

    argvs = sys.argv
    argc = len(argvs)

    if argc == 2:
        targetUrl = argvs[1]
    else:
        # デフォルトのターゲットURLを利用する
        targetUrl = "http://ameblo.jp/ogurayui-0815/"

    ac = AmebloCrawler(targetUrl)

    filename = targetUrl.replace("http://ameblo.jp/", "")
    filename = filename.rstrip("/")
    filename = filename + ".csv"

    while True:
        ac.crawler(targetUrl, filename)
        targetUrl = ac.getNextPageLink(targetUrl)

        if targetUrl is None:
            break

    print("Finish!")

if __name__ == '__main__':
    main()
