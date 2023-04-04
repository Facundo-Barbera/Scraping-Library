import asyncio
import logging
import time

import aiohttp
import requests
from bs4 import BeautifulSoup

from .scrapper_abc import ScrapperABC


class QuotesToScrape(ScrapperABC):
    """
    Scrapes quotes from http://quotes.toscrape.com asynchronously.
    """
    BASE_URL = 'http://quotes.toscrape.com'

    def __init__(self):
        """
        Initializes the QuotesToScrapeScrapper.
        """
        # Setup logger
        logging.basicConfig(level=logging.INFO, format='[QuotesToScrape] %(levelname)s - %(message)s')
        self._logger = logging.getLogger(__name__)

    def scrape(self):
        """
        Scrapes quotes from http://quotes.toscrape.com asynchronously.

        Returns:
            A list of quotes.
        """
        start_time = time.time()
        self._logger.info('Scraping..')

        # Create an async task for each page
        tasks = [self._scrape_page(parsed_html) for parsed_html in self._get_all_pages()]

        # Run all tasks
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            quotes = loop.run_until_complete(asyncio.gather(*tasks))
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())  # For Python 3.6+ only
            loop.close()

        # Clean quotes
        quotes = [quote for page_quotes in quotes for quote in page_quotes]
        self._logger.info(f'Scraped {len(quotes)} quotes in {time.time() - start_time} seconds.')

        # Return quotes
        return quotes

    def scrape_preloaded(self):
        """
        Scrapes quotes from http://quotes.toscrape.com asynchronously.
        Uses known URLs to scrape quicker.
        Returns:
            A list of quotes.
        """

        start_time = time.time()
        self._logger.info('Scraping..')

        async def _scrape_all_pages_and_quotes(url_list):
            # Get all parsed HTMLs with _get_all_pages_preloaded
            parsed_htmls = await self._get_all_pages_preloaded(url_list)

            # Create an async task for each page
            tasks = [self._scrape_page(parsed_html) for parsed_html in parsed_htmls]

            # Run all tasks
            quotes = await asyncio.gather(*tasks)

            return quotes

        # Create a list of all URLs
        urls = [self.BASE_URL]
        for i in range(2, 11):
            urls.append(self.BASE_URL + f'/page/{i}/')

        # Scrape all pages and get quotes
        quotes = asyncio.run(_scrape_all_pages_and_quotes(urls))

        # Clean quotes
        quotes = [quote for page_quotes in quotes for quote in page_quotes]
        self._logger.info(f'Scraped {len(quotes)} quotes in {time.time() - start_time} seconds.')

        # Return quotes
        return quotes

    def _get_all_pages(self):
        """
        Gets all pages from http://quotes.toscrape.com.

        Returns:
            A list of parsed HTML pages.
        """
        self._logger.info('Getting all pages..')

        # Parse the base URL
        parsed_htmls = []
        parsed_html = self._parse_html_from_url(self.BASE_URL)

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
            parsed_html = self._parse_html_from_url(self.BASE_URL + next_page)

        self._logger.info(f'Got {len(parsed_htmls)} pages.')

        # Return parsed HTMLs
        return parsed_htmls

    async def _get_all_pages_preloaded(self, urls: list):
        """
        Gets all pages from http://quotes.toscrape.com asynchronously.
        Uses preloaded URLs to scrape.

        Args:
            urls: The URLs to scrape.

        Returns:
            A list of parsed HTML pages.
        """
        self._logger.info('Getting all pages..')

        async def fetch(url, session):
            async with session.get(url) as response:
                return await response.text()

        async def _parse_html_async(url):
            async with aiohttp.ClientSession() as session:
                html_text = await fetch(url, session)
                return BeautifulSoup(html_text, 'html.parser')

        async def _get_page_async(url):
            return await _parse_html_async(url)

        async def _gather_all_pages():
            async with aiohttp.ClientSession() as _:
                tasks = [_get_page_async(url) for url in urls]
                return await asyncio.gather(*tasks)

        parsed_htmls = await _gather_all_pages()

        self._logger.info(f'Got {len(parsed_htmls)} pages.')

        return parsed_htmls

    async def _scrape_page(self, parsed_html):
        """
        Scrapes quotes from a page.

        Args:
            parsed_html: The parsed HTML of the page.

        Returns:
            A list of quotes and the next page.
        """
        self._logger.info('Scraping page..')

        # Get all quotes
        quotes = []
        for quote in parsed_html.find_all('div', class_='quote'):
            # Add quote to list
            quotes.append({'text': quote.find('span', class_='text').text,
                           'author': quote.find('small', class_='author').text,
                           'tags': str([tag.text for tag in quote.find_all('a', class_='tag')])})

        self._logger.info(f'Scraped {len(quotes)} quotes.')

        # Return quotes
        return quotes

    def _parse_html_from_url(self, url):
        """
        Parses HTML from a URL.
        """
        # Get HTML from URL and parse it
        self._logger.info(f'Parsing HTML from {url}..')
        html = requests.get(url).text
        parsed_html = BeautifulSoup(html, 'html.parser')

        # Return parsed HTML
        return parsed_html
