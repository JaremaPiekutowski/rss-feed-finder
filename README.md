# RSS Feed Finder
This Python script aims to find RSS feed URLs for a given webpage. It utilizes the requests library for making HTTP requests and BeautifulSoup for parsing HTML content.

## Requirements
- Python 3.x
- Requests library (`pip install requests`)
- BeautifulSoup library (`pip install beautifulsoup4`)

## Installation
Make sure you have Python installed on your system. You can download it from [python.org](python.org).

Install the required libraries using the following commands:

```
pip install requests
pip install beautifulsoup4
```

## Usage as a package

```
import feed_finder as ff
ff.show_feeds_urls("www.example.com")
```

## Usage - command line
Run the script from the command line, providing the URL of the webpage you want to check for RSS feed URLs.

```
python feed_finder.py https://example.com
```
The script will output the found RSS feed URLs for the provided webpage.

**Note:** If the script encounters an error while trying to fetch the feed URLs, it will print an error message indicating the issue.

Feel free to integrate this script into your projects or use it as a standalone tool to discover RSS feeds for various websites.
