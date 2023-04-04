import unittest

from scraping_library import QuotesToScrape


class TestQuotesToScrape(unittest.TestCase):

    def test_scraping(self):
        # Scrape all quotes.
        scrapper = QuotesToScrape()
        quotes = scrapper.scrape()

        # Check that there are more than 0 quotes.
        self.assertGreater(len(quotes), 0)

    def test_scraping_preloaded(self):
        # Scrape all quotes.
        scrapper = QuotesToScrape()
        quotes = scrapper.scrape_preloaded()

        # Check that there are more than 0 quotes.
        self.assertGreater(len(quotes), 0)


if __name__ == '__main__':
    unittest.main()
