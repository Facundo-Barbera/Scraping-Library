DEFAULT_DATABASE_FILE = 'data/output.db'


class Scrapper:
    """
    A base class for all scraping_library.

    This is mostly used as a blueprint.
    """

    def scrape(self):
        """
        Scrape the website and save the data to the database.
        """
        raise NotImplementedError
