# RSS Feed Finder

This Python package is designed to find RSS feed URLs for a given webpage. It utilizes the `requests` library for making HTTP requests and `BeautifulSoup` for parsing HTML content.

## Requirements

- Python 3.x
- Requests library
- BeautifulSoup library

## Installation

### From the source

To install the RSS Feed Finder package from the source, follow these steps:

1. **Clone the Repository**: First, clone the repository to your local machine using git. If you don't have git installed, you can download it from [git-scm.com](https://git-scm.com/).

    ```
    git clone https://github.com/yourusername/rssfeedfinder.git
    cd rssfeedfinder
    ```

    Replace `https://github.com/yourusername/rssfeedfinder.git` with the actual URL of your repository.

2. **Install the Package**: You can install the package using `pip`. Make sure you are in the root directory of the cloned repository (where `setup.py` is located).

    ```
    pip install .
    ```

    This command will install the package along with its dependencies.

## Usage

### As a package

After installation, you can use the RSS Feed Finder in your Python projects by importing it:

```python
import rssfeedfinder as ff
ff.show_feeds_urls("www.example.com")
```

### Command line

You can also use RSS Feed Finder directly from the command line. Navigate to the directory containing feed_finder.py and run the script by providing the URL of the webpage you want to check for RSS feed URLs:

```
python -m feed_finder.py https://example.com
```

The script will output the found RSS feed URLs for the provided webpage.

**Note:** If the script encounters an error while trying to fetch the feed URLs, it will print an error message indicating the issue.

Feel free to integrate this script into your projects or use it as a standalone tool to discover RSS feeds for various websites.