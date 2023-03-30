import asyncio
import time

from .scrapper_abc import ScrapperABC


class QuotesToScrapeScrapper(ScrapperABC):
    """
    Scrapes quotes from http://quotes.toscrape.com asynchronously.
    """
    BASE_URL = 'http://quotes.toscrape.com'

    def __init__(self, verbose: bool = False):
        """
        Initializes the QuotesToScrapeScrapper.

        Args:
            verbose: If True, the progress of the scraping will be printed to the console.
        """
        self._verbose = verbose

    def scrape(self):
        """
        Scrapes quotes from http://quotes.toscrape.com asynchronously.

        Returns:
            A list of quotes.
        """
        start_time = time.time()
        if self._verbose:
            print('Starting to scrape quotes..')

        # Get all the pages to scrape
        parsed_htmls = self._get_all_pages()

        # Create an async task for each page
        tasks = []
        for parsed_html in parsed_htmls:
            tasks.append(self._scrape_page(parsed_html))

        # Run all tasks
        loop = asyncio.get_event_loop()

        # Get all quotes
        quotes = loop.run_until_complete(asyncio.gather(*tasks))

        # Flatten quotes list
        quotes = [quote for page_quotes in quotes for quote in page_quotes]

        if self._verbose:
            print(f'Scraped {len(quotes)} quotes in {time.time() - start_time} seconds.')

        # Return quotes
        return quotes

    async def _scrape_page(self, parsed_html):
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

        # Return quotes
        return quotes

    def _get_all_pages(self):
        """
        Gets all the pages to scrape.

        Returns:
            A list of parsed HTML pages.
        """
        if self._verbose:
            print('Getting all pages..')

        parsed_htmls = []

        # Parse the base URL
        parsed_html = self._parse_html(self.BASE_URL)

        while True:
            # Add parsed HTML to list
            parsed_htmls.append(parsed_html)

            # Get first next button
            next_button = parsed_html.find('li', class_='next') or None
            next_page = next_button.find('a')['href'] if next_button else None

            # If there is no next page, break
            if not next_page:
                break

            # Parse the next page
            parsed_html = self._parse_html(self.BASE_URL + next_page)

        # Return parsed HTMLs
        return parsed_htmls
