import os

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from crawler.models import Page
import logging
import time
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invenio.settings"')
django.setup()


def process_page(url, soup):
    title = soup.title.string if soup.title else 'No title'
    content = soup.get_text()

    try:
        page, created = Page.objects.get_or_create(url=url)
        page.title = title
        page.content = content
        page.save()
        if created:
            logging.info(f"Saved new page: {title} ({url})")
        else:
            logging.info(f"Updated existing page: {title} ({url})")
    except Exception as e:
        logging.error(f"Error saving page {url}: {e}")


class WebCrawler:
    def __init__(self, start_urls, max_depth=3, delay=1):
        self.start_urls = start_urls
        self.visited = set()
        self.max_depth = max_depth
        self.delay = delay

    def crawl(self):
        for url in self.start_urls:
            self._crawl(url, depth=0)

    def _crawl(self, url, depth):
        if url in self.visited or depth > self.max_depth:
            return

        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                self.visited.add(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                process_page(url, soup)

                for link in soup.find_all('a'):
                    href = link.get('href')
                    full_url = urljoin(url, href)
                    if full_url not in self.visited:
                        time.sleep(self.delay)
                        self._crawl(full_url, depth + 1)
        except requests.RequestException as e:
            logging.error(f"Error crawling {url}: {e}")

