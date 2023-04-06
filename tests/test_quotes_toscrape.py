import unittest

from scraping_library import QuotesToScrape


class TestQuotesToScrape(unittest.TestCase):

    def test_scraping(self):
        scrapper = QuotesToScrape()
        quotes = scrapper.scrape()
        self.assertGreater(len(quotes), 0)

    def test_scraping_preloaded(self):
        scrapper = QuotesToScrape()
        quotes = scrapper.scrape_preloaded()
        self.assertGreater(len(quotes), 0)


if __name__ == '__main__':
    unittest.main()
