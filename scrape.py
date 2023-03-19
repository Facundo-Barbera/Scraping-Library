import sys

import requests
from bs4 import BeautifulSoup

from scrappers import QuotesToScrapeScrapper


def main():
    if len(sys.argv) < 2:
        print('Usage: python scrape.py <site_to_scrape>')
        print('Sites to scrape: quotes')
        sys.exit(1)

    if sys.argv[1] == 'quotes':
        scrapper = QuotesToScrapeScrapper()
        scrapper.scrape()


if __name__ == '__main__':
    main()
