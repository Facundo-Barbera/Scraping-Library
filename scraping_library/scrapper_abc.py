import os
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

DEFAULT_DATABASE_FILE = 'data/output.db'


class ScrapperABC(ABC):
    """
    A base class for all scraping_library.
    """

    @abstractmethod
    def __init__(self, verbose: bool = False):
        """
        Initializes the ScrapperABC.

        Args:
            verbose: If True, the progress of the scraping will be printed to the console.
        """
        self._verbose = verbose

    @abstractmethod
    def scrape(self):
        """
        Scrape a website.
        This is a blueprint for all scraping_library scrapers.
        """
        raise NotImplementedError

    @abstractmethod
    def _scrape_page(self, parsed_html):
        """
        Scrape a page.
        This is a blueprint for all scraping_library scrapers.
        """
        raise NotImplementedError

    def _parse_html(self, url: str):
        """
        Parse HTML from a URL using BeautifulSoup with html.parser.
        """
        if self._verbose:
            print(f'Parsing HTML from {url}')
        response = requests.get(url, timeout=5)
        return BeautifulSoup(response.text, 'html.parser')

    def _make_dirs_to_path(self, path: str):
        """
        Make directories to a path if they don't exist.
        This function is used when the scrapper wants to save a file to a path that doesn't exist.
        """
        if self._verbose:
            print(f'Making directories to {path}')

        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
