from abc import ABC, abstractmethod

import aiohttp
import requests
from bs4 import BeautifulSoup

DEFAULT_DATABASE_FILE = 'data/output.db'


class ScrapperABC(ABC):
    """
    A base class for all scraping_library.
    """

    @abstractmethod
    def __init__(self):
        """
        Initializes the ScrapperABC.
        """
        pass

    @abstractmethod
    def _parse_html_from_url(self, url):
        """
        Parses HTML from a URL.
        """
        html = requests.get(url).text
        parsed_html = BeautifulSoup(html, 'html.parser')
        return parsed_html

    @staticmethod
    async def _get_page_async(url):
        """
        Gets a set of htmls from a URL asynchronously.

        Args:
            url: The URL to scrape.

        Returns:
            A parsed HTML page.
        """

        async def fetch(url, session):
            async with session.get(url) as response:
                return await response.text()

        async def _parse_html_async(url):
            async with aiohttp.ClientSession() as session:
                html_text = await fetch(url, session)
                return BeautifulSoup(html_text, 'html.parser')

        return await _parse_html_async(url)
