# Scrapper
A python based project to scrape web-sites.

## Installation
### Clone the repository
```bash
git clone https://github.com/Facundo-Barbera/Scrapper.git
```

### Install the requirements
```bash
pip install -r requirements.txt
```

## Usage
### Run the script
```bash
python3 scrapper.py <site-to-scrape> (output-file)
```

- `(site-to-scrape)` is the site to scrape, see the list below. 
  - This argument is not required
  - If it is not specified, the script will ask for it, and default database will be used.

- `(output-file)` this is an optional argument, that specifies the output file.
  - This needs to be a `.db` file since the data is saved using `sqlite3`
  - The default value is `data/output.db`


Note: the database file will be created each time the script is run. 
If you want to keep the data, move the file to a different location before running the script again.

### Sites to scrape (`<site-to-scrape>`)
| Site   | Parameter name | Status  | Link                                                |
|--------|----------------|---------|-----------------------------------------------------|
| Quotes | quotes         | Ready   | http://quotes.toscrape.com                          |
| Books  | books          | W.I.P   | http://books.toscrape.com                           |
| Jobs   | jobs           | Planned | https://www.timesjobs.com/candidate/job-search.html |
| WHO    | who            | Planned | https://www.who.int/                                |

## Contributing
Pull requests are welcome, 
although I prefer to keep this project as a personal project and would rather receive issues and suggestions.