# -*- coding: utf-8 -*-

from setuptools import setup
import ameblo_crawler

setup(
    name="ameblo-crawler",
    version=ameblo_crawler.__version,
    description="Easily crawl and scrape Ameblo.",
    author="Shunsuke KITADA",
    url="https://github.com/shunk031/ameblo-crawler",
    keywords="Ameblo, ameblo, ameba, scraper, crawler, scraping, crawling",
    install_requires=["beautifulsoup4", "lxml"],
    license='http://www.apache.org/licenses/LICENSE-2.0'
)
