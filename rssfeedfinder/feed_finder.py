import argparse
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin


def is_valid_feed(soup):
    """
    Check if the BeautifulSoup object contains a valid feed structure.

    Parameters:
    soup (BeautifulSoup): BeautifulSoup object of the parsed feed content.

    Returns:
    bool: True if a valid feed structure is found, False otherwise.
    """
    # Common structures for different feed types
    feed_structures = {
        'rss': ('rss', 'channel'),
        'atom': ('feed',),
        'rdf': ('rdf:RDF',)
    }

    for feed_type, tags in feed_structures.items():
        if all(soup.find(tag) is not None for tag in tags):
            return True

    return False


def modify_feed_url(base_url: str, extracted_url: str) -> str:
    """
    Modify the extracted feed URL based on its format.

    Parameters:
    base_url (str): The base URL of the website.
    extracted_url (str): The extracted feed URL.

    Returns:
    str: The modified feed URL.
    """
    if extracted_url.startswith('//'):
        return 'https:' + extracted_url
    elif extracted_url.startswith('/'):
        return urljoin(base_url, extracted_url)
    elif not extracted_url.startswith(('http://', 'https://')):
        return urljoin(base_url, extracted_url)

    return extracted_url


def get_feed_url_by_appending_path(tab_url: str) -> dict:
    """
    Try to find a feed URL by appending common feed paths to the base URL.

    Parameters:
    tab_url (str): The base URL of the website.

    Returns:
    dict: The feed URL, or None if not found.
    """
    feed = None
    is_found = False

    paths = ['/feed', '/rss', '/rss.xml', '/feed.xml']

    for path in paths:
        if not is_found:
            feed_url = urljoin(tab_url, path)

            try:
                response = requests.get(feed_url, timeout=10)
                response.raise_for_status()

                if response.status_code != 404 and response.text:
                    o_parser = BeautifulSoup(response.text, 'html.parser')

                    if is_valid_feed(o_parser):
                        feed = {
                            'type': '',
                            'url': feed_url,
                            'title': feed_url
                        }
                        is_found = True

            except requests.exceptions.RequestException as e:
                print(f"Error while trying to get feed URL: {e}")
                return None

    return feed


def get_feeds_urls(url: str) -> list:
    """
    Get the feed URLs from a website.

    Parameters:
    url (str): The URL of the website.

    Returns:
    list: The feed URLs.
    """
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        feeds_urls = []
        types = [
            'application/rss+xml',
            'application/atom+xml',
            'application/rdf+xml',
            'application/rss',
            'application/atom',
            'application/rdf',
            'text/rss+xml',
            'text/atom+xml',
            'text/rdf+xml',
            'text/rss',
            'text/atom',
            'text/rdf'
        ]

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract links with specified types
        links = soup.find_all('link', {'type': types})

        for link in links:
            if link.has_attr('type') and link['type'] in types:
                feed_url = link.get('href')

                feed_url = modify_feed_url(url, feed_url)

                feed = {
                    'type': link['type'],
                    'url': feed_url,
                    'title': link.get('title', feed_url)
                }

                feeds_urls.append(feed)

        if not feeds_urls:
            appendix_feed = get_feed_url_by_appending_path(url)
            if appendix_feed is not None:
                feeds_urls.append(appendix_feed)

        return feeds_urls

    except requests.exceptions.RequestException as e:
        return f"Unable to find feed. Error: {e}"


def show_feeds_urls(url: str) -> None:
    """
    Show the feed URLs from a website.

    Parameters:
    url (str): The URL of the website.
    """
    feeds = get_feeds_urls(url)
    if isinstance(feeds, list):
        for feed in feeds:
            print(feed.get('url', 'Unknown URL'))
    else:
        print(feeds)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'url', help='URL to check for feed'
        )
    url = parser.parse_args().url
    show_feeds_urls(url)
