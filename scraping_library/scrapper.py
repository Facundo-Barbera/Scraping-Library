import os

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

    @staticmethod
    def _make_dirs_to_path(path: str):
        """
        Make directories to a path if they don't exist.
        """
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
