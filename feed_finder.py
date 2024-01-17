import requests
import sys

from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_feed_url_based_on_appendix(tab_url):
    feed = None
    is_found = False

    appendices = ['/feed', '/rss', '/rss.xml', '/feed.xml']

    for appendice in appendices:
        if not is_found:
            feed_url = urljoin(tab_url, appendice)

            try:
                response = requests.get(feed_url, timeout=10)
                response.raise_for_status()

                if response.status_code != 404 and response.text:
                    o_parser = BeautifulSoup(response.text, 'html.parser')

                    # Check if the HTML contains an RSS tag
                    rss_tag = o_parser.find('rss')

                    # Check if the RSS tag is present
                    if rss_tag is not None:
                        channel_tag = o_parser.find('channel')

                        # Check if the channel tag is present
                        if channel_tag is not None:
                            is_found = True

                            feed = {
                                'type': '',
                                'url': feed_url,
                                'title': feed_url
                            }

            except requests.exceptions.RequestException as e:
                print(f"Error while trying to get feed URL: {e}")

    return feed


def get_feeds_urls(url):
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

                # Modify feed URL as needed
                if feed_url.startswith('//'):
                    feed_url = 'http:' + feed_url
                elif feed_url.startswith('/'):
                    feed_url = urljoin(url, feed_url)
                elif not feed_url.startswith(('http://', 'https://')):
                    feed_url = urljoin(url, feed_url)

                feed = {
                    'type': link['type'],
                    'url': feed_url,
                    'title': link.get('title', feed_url)
                }

                feeds_urls.append(feed)

        if not feeds_urls:
            appendix_feed = get_feed_url_based_on_appendix(url)
            if appendix_feed is not None:
                feeds_urls.append(appendix_feed)

        return feeds_urls

    except requests.exceptions.RequestException as e:
        return f"Unable to find feed. Error: {e}"


if __name__ == "__main__":
    url_to_check = sys.argv[1]
    for feed in get_feeds_urls(url_to_check):
        print(feed['url'])
