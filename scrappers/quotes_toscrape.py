import requests
from bs4 import BeautifulSoup


class QuotesToScrapeScrapper:
    """
    Scrapes quotes from http://quotes.toscrape.com/

    Saves the quotes in a csv file.
    """

    def __init__(self, csv_file: str = 'quotes.csv'):
        self._base_url = 'http://quotes.toscrape.com/'
        self._csv_file = csv_file

    def scrape(self):
        """
        Scrapes quotes from http://quotes.toscrape.com/

        :return:
            None
        """
        url = self._base_url

        # Delete file if exists
        with open('quotes.csv', 'w') as file:
            file.write('text,author,tags \n')

        # Loop through all pages
        while True:
            print(f'Now scraping {url}...')
            next_page = self._scrape_quotes(url)

            if next_page:
                url = self._base_url + next_page
            else:
                break

    def _scrape_quotes(self, url: str):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        quotes = soup.find_all('div', class_='quote')

        for quote in quotes:
            self._save_quote(quote)

        next_button = soup.find('li', class_='next')
        if next_button:
            return next_button.find('a')['href']
        else:
            return None

    def _save_quote(self, quote):
        quote_dict = {
            'text': quote.find('span', class_='text').get_text(),
            'author': quote.find('small', class_='author').get_text(),
            'tags': str([tag.get_text() for tag in quote.find('div', class_='tags').find_all('a', class_='tag')])
        }

        with open(self._csv_file, 'a') as file:
            file.write(f"{quote_dict['text']},{quote_dict['author']},{quote_dict['tags']} \n")
