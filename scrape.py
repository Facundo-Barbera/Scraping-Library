import sys

import requests
from bs4 import BeautifulSoup

from scrappers import QuotesToScrapeScrapper


def main():
    if len(sys.argv) < 2:
        print('Please provide a scrapper name as an argument.')
        return

    if len(sys.argv) > 2 and sys.argv[2].endswith('.db'):
        database_file = sys.argv[2]
    else:
        print('Using default database file (data/quotes.db)')
        print('To use a different database file, provide it as the second argument.')
        print('Example: python scrape.py quotes data/quotes.db')
        print('Note: if you provided a database file and it did not work, make sure the file ends with .db')
        database_file = None

    match sys.argv[1]:
        case 'quotes':
            scrapper = QuotesToScrapeScrapper(database_file if database_file else None)
            scrapper.scrape()


if __name__ == '__main__':
    main()
