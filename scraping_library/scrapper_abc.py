from abc import ABC, abstractmethod

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

    @abstractmethod
    def _parse_html_from_url(self, url):
        """
        Parses HTML from a URL.
        """
        # Get HTML from URL and parse it
        html = requests.get(url).text
        parsed_html = BeautifulSoup(html, 'html.parser')

        # Return parsed HTML
        return parsed_html
