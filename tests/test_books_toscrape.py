import unittest

from scraping_library import BooksToScrape


class TestBooksToScrape(unittest.TestCase):

    def test_scraping_no_async(self):
        scrapper = BooksToScrape()
        books = scrapper.scrape(semaphore_=1)
        self.assertGreater(len(books), 0)

    def test_scraping_async(self):
        scrapper = BooksToScrape()
        books = scrapper.scrape(semaphore_=15)
        self.assertGreater(len(books), 0)


if __name__ == '__main__':
    unittest.main()
