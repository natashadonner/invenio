import csv
import os
import django
from django.core.management.base import BaseCommand
from crawler.crawler import WebCrawler

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "invenio.settings")
django.setup()


class Command(BaseCommand):
    help = 'Run the web crawler'

    def handle(self, *args, **kwargs):
        urls = self.load_urls_from_csv('crawler/resources/test.csv')
        crawler = WebCrawler(urls)
        crawler.crawl()

    def load_urls_from_csv(self, file_path):
        urls = []
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Skip header row
                for row in csv_reader:
                    if len(row) > 1:
                        urls.append(row[1].strip())
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'File not found: {file_path}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error reading file: {e}'))

        return urls
