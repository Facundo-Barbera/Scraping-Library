# Scrapper

A python based project to scrape web-sites.
This is a personal project to explore web scraping and better understand how it works.
I also made this project a library, mostly to practice packaging and publishing a python library.
If you have any suggestions or issues, please open an issue.

## Installation

This project requires
[Python 3.10](https://www.python.org/downloads/release/python-3100/)
or higher.

### Clone the repository

```bash
pip install git+https://github.com/Facundo-Barbera/Scrapper.git
```

## Usage

### Quotes to Scrape

```python
from scraping_library import QuotesToScrapeScrapper

# Scrap quotes.toscrape.com
scrapper = QuotesToScrapeScrapper()
scrapper.scrape()

# Get quotes
quotes = scrapper.get_quotes()
```

Each quote is a dictionary which is built like this:

```python
quote = {
    "text": "The text of the quote",
    "author": "The author of the quote",
    "tags": ["a", "list", "of", "tags"]
}
```

The `QuotesToScrapeScrapper` can also be initialized with a quote limit and a database file.

```python
from scraping_library import QuotesToScrapeScrapper

# Scrap quotes.toscrape.com
scrapper = QuotesToScrapeScrapper(max_quotes=10, database_file="data/my_database.db")
scrapper.scrape()

# Save the scrapped data to a data file
# Default database is data/output.db
scrapper.save_to_database()
```

### More functionality coming soon

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contributing

Pull requests are welcome,
although I prefer to keep this project as a personal project and would rather receive issues and suggestions.

## Socials and extras

Join my [Discord server](https://discord.gg/8Z7Y4Z9).