import sqlite3
import time

from .scrapper import ScrapperABC, DEFAULT_DATABASE_FILE


class QuotesToScrapeScrapper(ScrapperABC):
    """
    Scrapes quotes from http://quotes.toscrape.com
    """
    BASE_URL = 'http://quotes.toscrape.com'

    def __init__(self, verbose: bool = False):
        """
        Initializes the QuotesToScrapeScrapper.

        Args:
            verbose: If True, the progress of the scraping will be printed to the console.
        """
        self.quotes = []
        self._verbose = verbose

    def scrape(self, max_quotes: int = 0):
        """
        Scrapes quotes from http://quotes.toscrape.com.

        Args:
            max_quotes: The maximum number of quotes to scrape. If 0, all quotes will be scraped.
        """
        if self._verbose:
            print('Scraping quotes')
            start_time = time.time()

        # Set the current URL to the base URL
        current_url = self.BASE_URL

        # Scrape quotes
        while current_url:
            # Get quotes and next page
            parsed_html = self._parse_html(current_url)
            quotes, next_page = self._scrape_page(parsed_html)

            # Save quotes to quotes list
            for quote in quotes:
                if not max_quotes or len(self.quotes) < max_quotes:
                    self.quotes.append(quote)
                else:
                    break

            # Set the next page if there is one, and we haven't reached the max number of quotes
            if next_page and (not max_quotes or len(self.quotes) < max_quotes):
                current_url = self.BASE_URL + next_page
            else:
                current_url = None

        if self._verbose:
            print(f'Scraped {len(self.quotes)} quotes in {time.time() - start_time:.2f} seconds.')

    def _scrape_page(self, parsed_html):
        """
        Scrapes quotes from a page.

        Args:
            parsed_html: The parsed HTML of the page.

        Returns:
            A list of quotes and the next page.
        """
        if self._verbose:
            print(f'Scraping page: {parsed_html.find("title").text}')

        # Get all quotes
        quotes = []
        for quote in parsed_html.find_all('div', class_='quote'):
            # Add quote to list
            quotes.append({'text': quote.find('span', class_='text').text,
                           'author': quote.find('small', class_='author').text,
                           'tags': str([tag.text for tag in quote.find_all('a', class_='tag')])})

        if self._verbose:
            print(f'Scraped {len(quotes)} quotes from page.')

        # Get next page
        next_button = parsed_html.find('li', class_='next') or None
        next_page = next_button.find('a')['href'] if next_button else None

        # Return quotes
        return quotes, next_page

    def save_to_database(self, database_file: str = DEFAULT_DATABASE_FILE):
        """
        Saves the scraped quotes to the database.

        Args:
            database_file: The path to the database file.
        """
        if self._verbose:
            print(f'Saving quotes to database: {database_file}')

        if not database_file.endswith('.db'):
            raise ValueError('Database file must end with .db')

        self._make_dirs_to_path(database_file)
        self._create_tables()

        if not self.quotes:
            print('No quotes to save to database.')
            return

        with sqlite3.connect(database_file) as connection:
            for quote in self.quotes:
                connection.execute('INSERT INTO quotes (text, author, tags) VALUES (?, ?, ?)',
                                   (quote['text'], quote['author'], quote['tags']))

    def _create_tables(self, database_file: str = DEFAULT_DATABASE_FILE):
        """
        Creates the tables in the database.
        
        Args:
            database_file: The path to the database file.
        """
        if self._verbose:
            print(f'Creating tables in database: {database_file}')

        # Create table if it doesn't exist
        with sqlite3.connect(database_file) as connection:
            connection.execute('CREATE TABLE IF NOT EXISTS quotes ('
                               'text TEXT NOT NULL,'
                               'author TEXT NOT NULL,'
                               'tags TEXT NOT NULL'
                               ')')

        # Delete all contents of the table before scraping
        with sqlite3.connect(database_file) as connection:
            connection.execute('DELETE FROM quotes WHERE TRUE')
