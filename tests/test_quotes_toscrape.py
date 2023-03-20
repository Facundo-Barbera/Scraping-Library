import os
import unittest

from scraping_library import QuotesToScrapeScrapper


class TestQuotesToScrape(unittest.TestCase):

    def test_quotes_max_0(self):
        # Get quotes
        scrapper = QuotesToScrapeScrapper()
        scrapper.scrape()
        quotes = scrapper.get_quotes()

        # Check if all quotes have the correct format and key
        for quote in quotes:
            self.assertEqual(len(quote), 3)
            self.assertIn('text', quote)
            self.assertIn('author', quote)
            self.assertIn('tags', quote)

    def test_quotes_max_20(self):
        # Get quotes
        scrapper = QuotesToScrapeScrapper(max_quotes=20)
        scrapper.scrape()
        quotes = scrapper.get_quotes()

        # Check if the number of quotes is correct
        self.assertEqual(len(quotes), 20)

        # Check if all quotes have the correct format and key
        for quote in quotes:
            self.assertEqual(len(quote), 3)
            self.assertIn('text', quote)
            self.assertIn('author', quote)
            self.assertIn('tags', quote)

    def test_quotes_max_1000(self):
        # Get quotes
        scrapper = QuotesToScrapeScrapper(max_quotes=1000)
        scrapper.scrape()
        quotes = scrapper.get_quotes()

        # Check if all quotes have the correct format and key
        for quote in quotes:
            self.assertEqual(len(quote), 3)
            self.assertIn('text', quote)
            self.assertIn('author', quote)
            self.assertIn('tags', quote)

    def test_quotes_database(self):
        # Scrape quotes and save to database
        scrapper = QuotesToScrapeScrapper(max_quotes=20, database_file='data/output.db')
        scrapper.scrape()
        scrapper.save_to_database()

        # Check if database file exists
        self.assertTrue(os.path.isfile('data/output.db'))

        # Clean up
        os.remove('data/output.db')
        if not os.listdir('data'):
            os.rmdir('data')


if __name__ == '__main__':
    unittest.main()
