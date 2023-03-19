import requests
from bs4 import BeautifulSoup
import sqlite3


class QuotesToScrapeScrapper:
    """
    Scrapes quotes from http://quotes.toscrape.com

    Saves the quotes in a csv file.
    """
    BASE_URL = 'http://quotes.toscrape.com'

    def __init__(self, database_file: str = 'data/output.db'):
        self._database_file = database_file
        self._create_table()

    def _create_table(self):
        # Create table if it doesn't exist
        with sqlite3.connect(self._database_file) as connection:
            connection.execute('CREATE TABLE IF NOT EXISTS quotes ('
                               'text TEXT NOT NULL,'
                               'author TEXT NOT NULL,'
                               'tags TEXT NOT NULL'
                               ')')

        # Delete all contents of the table before scraping
        with sqlite3.connect(self._database_file) as connection:
            connection.execute('DELETE FROM quotes')

    def scrape(self):
        """
        Scrapes quotes from http://quotes.toscrape.com
        """
        # Set the base url
        url = self.BASE_URL

        # Scrape quotes from all pages
        while url:
            print(f'Now scraping {url}...')
            next_page = self._scrape_quotes(url)
            url = (self.BASE_URL + next_page) if next_page else None

    def _scrape_quotes(self, url: str):
        # Get the page
        page_html = requests.get(url)
        parsed_html = BeautifulSoup(page_html.content, 'html.parser')

        # Get all quotes and save them to the database
        for quote in parsed_html.find_all('div', class_='quote'):
            self._save_quote_to_database(quote)

        # Check if there is a next page button
        next_button = parsed_html.find('li', class_='next') or None
        return next_button.find('a')['href'] if next_button else None

    def _save_quote_to_database(self, quote):
        with sqlite3.connect(self._database_file) as connection:
            connection.execute('INSERT INTO quotes (text, author, tags) VALUES (?, ?, ?)',
                               (quote.find('span', class_='text').text,
                                quote.find('small', class_='author').text,
                                str([tag.text for tag in quote.find_all('a', class_='tag')])))
