from bs4 import BeautifulSoup

from .scrapper import Scrapper, DEFAULT_DATABASE_FILE


class BooksToScrapeScrapper(Scrapper):
    """
    Scrapes books from http://books.toscrape.com

    Saves the books in a sqlite3 (.db) file.
    """

    BASE_URL = 'http://books.toscrape.com'

    def __init__(self):
        """
        Initializes the BooksToScrapeScrapper.
        """
        self._books = []
        self._current_url = self.BASE_URL

    def scrape(self, max_books: int = 0):
        """
        Scrapes books from http://books.toscrape.com.

        Args:
            max_books: The maximum number of books to scrape. If 0, all books will be scraped.
                If the number of books is less than max_books, all books will be scraped.
        """
        # Scrape books
        pass

    def save_to_database(self, database_file: str = DEFAULT_DATABASE_FILE):
        """
        Saves the scraped books to the database.

        Args:
            database_file: The database file to save the books to. Must be a .db file.
        """
        pass

    def get_books(self):
        """
        Returns:
            A list of books.
        """
        return self._books

    def _scrape_books(self, parsed_html: BeautifulSoup):
        """
        Scrapes books from a parsed HTML.

        Args:
            parsed_html: The parsed HTML to scrape books from.

        Returns:
            A list of books.
        """
        books = []



book = {
    'title': 'A Light in the Attic',
    'author': 'Suzanne Collins',
    'price': '£51.77',
    'rating': 'Three',
    'image_url': 'http://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg',
    'book_url': 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html',

}
