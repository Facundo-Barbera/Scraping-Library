import unittest

from scraping_library import BooksToScrape


class TestBooksToScrape(unittest.TestCase):

    def test_scraping_no_async(self):
        # Scrape all quotes.
        scrapper = BooksToScrape()
        books = scrapper.scrape(semaphore_=1)

        # Check that there are more than 0 quotes.
        self.assertGreater(len(books), 0)

    def test_scraping_async(self):
        # Scrape all quotes.
        scrapper = BooksToScrape()
        books = scrapper.scrape(semaphore_=15)

        # Check that there are more than 0 quotes.
        self.assertGreater(len(books), 0)


if __name__ == '__main__':
    unittest.main()
