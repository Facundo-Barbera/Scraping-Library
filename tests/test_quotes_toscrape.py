import unittest

from scraping_library import QuotesToScrapeScrapper


class TestQuotesToScrape(unittest.TestCase):

    def test_scrape_no_limit(self):
        # Scrape all quotes.
        scrapper = QuotesToScrapeScrapper()
        scrapper.scrape(max_quotes=0)

        # Check that there are more than 0 quotes.
        self.assertGreater(len(scrapper.quotes), 0)

    def test_scrape_no_limit_verbose(self):
        # Scrape all quotes.
        scrapper = QuotesToScrapeScrapper(verbose=True)
        scrapper.scrape(max_quotes=0)

        # Check that there are more than 0 quotes.
        self.assertGreater(len(scrapper.quotes), 0)

    def test_scrape_limit_10(self):
        # Scrape 10 quotes.
        scrapper = QuotesToScrapeScrapper()
        scrapper.scrape(max_quotes=10)

        # Check that there are 10 quotes.
        self.assertEqual(len(scrapper.quotes), 10)

    def test_scrape_quality(self):
        # Scrape 1 quote.
        scrapper = QuotesToScrapeScrapper()
        scrapper.scrape(max_quotes=1)

        # Check that there is 1 quote.
        self.assertEqual(len(scrapper.quotes), 1)

        # Check the dictionary keys.
        self.assertEqual(set(scrapper.quotes[0].keys()), {'text', 'author', 'tags'})


if __name__ == '__main__':
    unittest.main()
