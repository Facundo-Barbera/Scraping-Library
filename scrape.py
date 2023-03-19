import sys

import requests
from bs4 import BeautifulSoup

from scrappers import QuotesToScrapeScrapper


def main():
    if len(sys.argv) < 2:
        # Ask the user for the scrapper name
        scrapper = input("Please enter the name of the scrapper you want to use: ")

        # Set the database file to None
        print('Using default database file (data/quotes.db)')
        database_file = None
    else:
        # Get the scrapper name from the first argument
        scrapper = sys.argv[1]

        # Check if a database file was provided
        if len(sys.argv) > 2 and sys.argv[2].endswith('.db'):
            database_file = sys.argv[2]
        else:
            print('Using default database file (data/quotes.db)')
            print('To use a different database file, provide it as the second argument.')
            print('Example: python scrape.py quotes data/quotes.db')
            print('Note: if you provided a database file and it did not work, make sure the file ends with .db')
            database_file = None

    match scrapper:
        case 'quotes':
            scrapper = QuotesToScrapeScrapper(database_file if database_file else None)
            scrapper.scrape()
        case _:
            print(f'No scrapper named {scrapper} found.')


if __name__ == '__main__':
    main()
