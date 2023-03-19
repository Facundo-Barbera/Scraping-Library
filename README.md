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

- `<site-to-scrape>` is the site to scrape. (See the list below)
- `(output-file)` this is an optional argument, that specifies the output file.
This needs to be a `.db` file since the data is saved using `sqlite3`
The default value is `output.db`

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