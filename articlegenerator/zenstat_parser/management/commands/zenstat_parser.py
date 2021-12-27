import time

from django.core.management import BaseCommand
from selenium import webdriver

from zenstat_parser.parser import SeleniumClient, Parser


class Command(BaseCommand):
    help = 'Parser zenstata'

    def handle(self, *args, **options):
        driver = webdriver.Chrome()
        PROXY = "182.92.242.11"
        client = SeleniumClient(driver, PROXY)
        client.login()
        page = 500
        while page < 3096:
            time.sleep(1)
            start_page = page - 99
            stop_page = page
            try:
                parser = Parser(client, start_page, stop_page)
                parser.run()
                page += 100
            except UnboundLocalError:
                page += 100
                start_page = page - 99
                stop_page = page
                parser = Parser(client, start_page, stop_page)
                parser.run()
