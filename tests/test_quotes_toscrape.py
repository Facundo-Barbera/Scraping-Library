import unittest

from scraping_library import QuotesToScrapeScrapper


class TestQuotesToScrape(unittest.TestCase):

    def test_quotes_max_0(self):
        # Create instance of QuotesToScrapeScrapper
        scrapper = QuotesToScrapeScrapper(max_quotes=0)

        # Scrape quotes
        scrapper.scrape()

        # Get quotes
        quotes = scrapper.get_quotes()

        # Check if all quotes have the correct format and key
        for quote in quotes:
            self.assertEqual(len(quote), 3)
            self.assertIn('text', quote)
            self.assertIn('author', quote)
            self.assertIn('tags', quote)

    def test_quotes_max_20(self):
        # Create instance of QuotesToScrapeScrapper
        scrapper = QuotesToScrapeScrapper(max_quotes=20)

        # Scrape quotes
        scrapper.scrape()

        # Get quotes
        quotes = scrapper.get_quotes()

        # Check if the number of quotes is correct
        self.assertEqual(len(quotes), 20)

        # Check if all quotes have the correct format and key
        for quote in quotes:
            self.assertEqual(len(quote), 3)
            self.assertIn('text', quote)
            self.assertIn('author', quote)
            self.assertIn('tags', quote)

    def test_quotes_database(self):
        # Create instance of QuotesToScrapeScrapper
        scrapper = QuotesToScrapeScrapper(max_quotes=20)

        # Scrape quotes
        scrapper.scrape()

        # Save quotes to database
        scrapper.save_to_database()


if __name__ == '__main__':
    unittest.main()
