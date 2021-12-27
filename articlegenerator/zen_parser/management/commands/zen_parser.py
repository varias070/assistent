import time

from django.core.management import BaseCommand
from selenium import webdriver

from zen_parser.parser import SeleniumClient, Parser


class Command(BaseCommand):
    help = 'Parser zena'

    def handle(self, *args, **options):
        driver = webdriver.Chrome()
        PROXY = "182.92.242.11"
        client = SeleniumClient(driver, PROXY)
        parser = Parser(client)
        parser.run()
