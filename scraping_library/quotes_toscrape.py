import sqlite3

import requests
from bs4 import BeautifulSoup

from .scrapper import Scrapper, DEFAULT_DATABASE_FILE


class QuotesToScrapeScrapper(Scrapper):
    """
    Scrapes quotes from http://quotes.toscrape.com

    Saves the quotes in a sqlite3 (.db) file.
    """
    BASE_URL = 'http://quotes.toscrape.com'

    def __init__(self, database_file: str = DEFAULT_DATABASE_FILE, max_quotes: int = 0):
        """
        Initializes the QuotesToScrapeScrapper.

        :param database_file: The database file to save the quotes to. Must be a .db file.
        :param max_quotes: The maximum number of quotes to scrape. If 0, all quotes will be scraped.
        """
        self._database_file = database_file
        self._max_quotes = max_quotes
        self._quotes = []
        self._current_url = self.BASE_URL

    def scrape(self):
        """
        Scrapes quotes from http://quotes.toscrape.com.
        """
        # Scrape quotes
        while self._current_url and (not self._max_quotes or len(self._quotes) < self._max_quotes):
            print(f'Now scraping {self._current_url}...')
            parsed_html = self._parse_html(self._current_url)
            quotes = self._scrape_quotes(parsed_html)
            next_page = self._get_next_page(parsed_html)

            # Save quotes to database
            for quote in quotes:
                self._quotes.append(quote)

            # Set the next page
            self._current_url = self.BASE_URL + next_page if next_page else None

    def save_to_database(self):
        """
        Saves the scraped quotes to the database.
        """
        self._make_dirs_to_path(self._database_file)

        if not self._quotes:
            print('No quotes to save to database.')
            return

        self._create_table()
        for quote in self._quotes:
            self._save_quote_to_database(quote)

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
            connection.execute('DELETE FROM quotes WHERE TRUE')

    def _save_quote_to_database(self, quote: dict):
        with sqlite3.connect(self._database_file) as connection:
            connection.execute('INSERT INTO quotes (text, author, tags) VALUES (?, ?, ?)',
                               (quote['text'], quote['author'], quote['tags']))

    def _scrape_quotes(self, parsed_html):
        # Get all quotes
        quotes = []
        for quote in parsed_html.find_all('div', class_='quote'):
            # Check if we have reached the max number of quotes
            if self._max_quotes and len(self._quotes) >= self._max_quotes:
                break

            # Add quote to list
            quotes.append({'text': quote.find('span', class_='text').text,
                           'author': quote.find('small', class_='author').text,
                           'tags': str([tag.text for tag in quote.find_all('a', class_='tag')])})

        # Return quotes
        return quotes

    @staticmethod
    def _get_next_page(parsed_html):
        # Check if there is a next page button
        next_button = parsed_html.find('li', class_='next') or None
        return next_button.find('a')['href'] if next_button else None

    def get_quotes(self):
        return self._quotes
