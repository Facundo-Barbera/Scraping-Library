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
        logging.basicConfig(level=logging.INFO, format='[QuotesToScrape] %(levelname)s - %(message)s')
        self._logger = logging.getLogger(__name__)

    def scrape(self):
        """
        Scrapes quotes from http://quotes.toscrape.com asynchronously.

        Returns:
            A list of quotes.
        """
        scrape_start_time = time.time()
        self._logger.info('Scraping..')

        tasks = [self._scrape_page(parsed_html) for parsed_html in self._get_all_pages()]
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            quotes = loop.run_until_complete(asyncio.gather(*tasks))
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

        quotes = [quote for page_quotes in quotes for quote in page_quotes]
        self._logger.info(f'Scraped {len(quotes)} quotes in {time.time() - scrape_start_time} seconds.')
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
            parsed_htmls = await self._get_all_pages_preloaded(url_list)
            tasks = [self._scrape_page(parsed_html) for parsed_html in parsed_htmls]
            return await asyncio.gather(*tasks)

        urls = [self.BASE_URL]
        for page_number in range(2, 11):
            urls.append(self.BASE_URL + f'/page/{page_number}/')

        quotes = [quote for page_quotes in asyncio.run(_scrape_all_pages_and_quotes(urls)) for quote in page_quotes]
        self._logger.info(f'Scraped {len(quotes)} quotes in {time.time() - start_time} seconds.')
        return quotes

    def _get_all_pages(self):
        """
        Gets all pages from http://quotes.toscrape.com.

        Returns:
            A list of parsed HTML pages.
        """
        self._logger.info('Getting all pages..')
        parsed_htmls = [self._parse_html_from_url(self.BASE_URL)]

        while True:
            next_button = parsed_htmls[-1].find('li', class_='next') or None
            next_page = next_button.find('a')['href'] if next_button else None

            if not next_page:
                break
            else:
                parsed_htmls.append(self._parse_html_from_url(self.BASE_URL + next_page))

        self._logger.info(f'Got {len(parsed_htmls)} pages.')
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

        async with aiohttp.ClientSession() as _:
            tasks = [self._get_page_async(url) for url in urls]
            parsed_htmls = await asyncio.gather(*tasks)

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

        quotes = []
        for quote in parsed_html.find_all('div', class_='quote'):
            quotes.append({'text': quote.find('span', class_='text').text,
                           'author': quote.find('small', class_='author').text,
                           'tags': str([tag.text for tag in quote.find_all('a', class_='tag')])})

        self._logger.info(f'Scraped {len(quotes)} quotes.')
        return quotes

    def _parse_html_from_url(self, url):
        """
        Parses HTML from a URL.
        """
        self._logger.info(f'Parsing HTML from {url}..')
        html = requests.get(url).text
        parsed_html = BeautifulSoup(html, 'html.parser')
        return parsed_html
