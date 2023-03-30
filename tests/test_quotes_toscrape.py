import unittest

from scraping_library import QuotesToScrapeScrapper


class TestQuotesToScrape(unittest.TestCase):

    def test_scraping(self):
        # Scrape all quotes.
        scrapper = QuotesToScrapeScrapper(verbose=True)
        quotes = scrapper.scrape(max_quotes=0)

        # Check that there are more than 0 quotes.
        self.assertGreater(len(quotes), 0)


if __name__ == '__main__':
    unittest.main()
