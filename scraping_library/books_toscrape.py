import asyncio
import logging
import time

import aiohttp
import requests
from bs4 import BeautifulSoup

from scraping_library.scrapper_abc import ScrapperABC


class BooksToScrape(ScrapperABC):
    """
    Scrapes books from https://books.toscrape.com
    """
    BASE_URL = 'http://books.toscrape.com'
    RATING_TO_STARS = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5,
    }

    def __init__(self):
        """
        Initializes the BooksToScrapeScrapper.
        """
        logging.basicConfig(level=logging.INFO, format='[BooksToScrape] %(levelname)s - %(message)s')
        self._logger = logging.getLogger(__name__)

    def scrape(self, semaphore_=15):
        """
        Scrapes books from http://books.toscrape.com asynchronously.

        Args:
            semaphore_: The semaphore to use when scraping asynchronously.

        Returns:
            A list of books.
        """
        start_time = time.time()
        self._logger.info('Scraping...')

        parsed_catalogue_htmls = self._get_all_catalogue_pages()

        async def get_all_book_htmls(parsed_htmls):
            book_html_start_time = time.time()
            self._logger.info('Getting all book pages...')
            sem = asyncio.Semaphore(semaphore_)

            async def _get_book_html_with_semaphore(parsed_html):
                async with sem:
                    return await self._get_books_htmls(parsed_html)

            tasks = [_get_book_html_with_semaphore(parsed_html) for parsed_html in parsed_htmls]
            book_pages = [book for books in await asyncio.gather(*tasks) for book in books]
            self._logger.info(f'Got {len(book_pages)} book pages in {time.time() - book_html_start_time} seconds.')
            return book_pages

        parsed_book_htmls = asyncio.run(get_all_book_htmls(parsed_catalogue_htmls))

        async def get_all_book_data(parsed_htmls):
            book_data_start_time = time.time()
            self._logger.info('Getting all book data...')
            sem = asyncio.Semaphore(semaphore_)

            async def _get_book_data_with_semaphore(parsed_html):
                async with sem:
                    return await self._extract_book_data(parsed_html)

            tasks = [_get_book_data_with_semaphore(parsed_html) for parsed_html in parsed_htmls]
            book_data = await asyncio.gather(*tasks)
            self._logger.info(f'Got {len(book_data)} book data in {time.time() - book_data_start_time} seconds.')
            return book_data

        parsed_book_data = asyncio.run(get_all_book_data(parsed_book_htmls))

        self._logger.info(f'Scraped {len(parsed_book_htmls)} books in {time.time() - start_time} seconds.')
        return parsed_book_data

    def _get_all_catalogue_pages(self):
        """
        Gets all catalogue pages.

        Returns:
            A list of parsed HTMLs.
        """
        parsed_htmls = [self._parse_html_from_url(self.BASE_URL)]

        while True:
            next_button = parsed_htmls[-1].find('li', {'class': 'next'})
            next_page = next_button.find('a')['href'] if next_button else None

            if not next_page:
                break
            else:
                parsed_htmls.append(self._parse_html_from_url(
                    self.BASE_URL + f'{"/" if next_page.startswith("catalogue") else "/catalogue/"}' + next_page)
                )

        return parsed_htmls

    async def _get_books_htmls(self, parsed_html):
        """
        Gets all books htmls from a parsed html asynchronously.

        Args:
            parsed_html: The parsed HTML of the page.

        Returns:
            A list of books URLs.
        """
        books_urls = []
        books = parsed_html.find_all('article', {'class': 'product_pod'})

        for book in books:
            url = book.find('a')['href']
            books_urls.append(self.BASE_URL + f'{"/" if url.startswith("catalogue") else "/catalogue/"}' + url)

        async with aiohttp.ClientSession() as _:
            tasks = [self._get_page_async(book_url) for book_url in books_urls]
            return await asyncio.gather(*tasks)

    async def _extract_book_data(self, parsed_html):
        """
        Extracts book data from a parsed HTML.

        Args:
            parsed_html: The parsed HTML of the book page.

        Returns:
            A dictionary of book data.
        """

        def get_element_safe(soup, func, *args, **kwargs):
            try:
                return func(soup, *args, **kwargs)
            except AttributeError:
                return None
            except ValueError:
                return None

        book_data = {
            'title': get_element_safe(parsed_html, lambda s: s.find('h1').text),
            'genre': get_element_safe(parsed_html,
                                      lambda s: s.find('ul', {'class': 'breadcrumb'}).find_all('li')[2].text),
            'price': get_element_safe(parsed_html, lambda s: float(s.find('p', {'class': 'price_color'}).text[2:])),
            'rating': get_element_safe(parsed_html, lambda s: self.RATING_TO_STARS[
                s.find('p', {'class': 'star-rating'})['class'][1]]),
            'image_url': get_element_safe(parsed_html, lambda s: self.BASE_URL + '/' + s.find('img')['src'][6:]),
            'stock': get_element_safe(parsed_html, lambda s: int(
                s.find('p', {'class': 'instock availability'}).text.split()[2][1:-1])),
            'description': get_element_safe(parsed_html,
                                            lambda s: s.find('div', {'id': 'product_description'}).find_next_sibling(
                                                'p').text),
            'reviews': get_element_safe(parsed_html, lambda s: int(
                s.find('table', {'class': 'table table-striped'}).find_all('tr')[6].find_all('td')[0].text))
        }

        return book_data

    def _parse_html_from_url(self, url):
        """
        Parses HTML from a URL.
        """
        self._logger.info(f'Parsing HTML from {url}...')
        html = requests.get(url).text
        parsed_html = BeautifulSoup(html, 'html.parser')
        return parsed_html
