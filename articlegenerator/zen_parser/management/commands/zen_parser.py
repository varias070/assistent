import random

from django.core.management import BaseCommand
from selenium import webdriver

from zen_parser.parser import SeleniumClient, Parser


class Command(BaseCommand):
    help = 'Parser dzena'

    def handle(self, *args, **options):
        driver = webdriver.Chrome()
        list_proxy = ["182.92.242.11", '200.239.64.36', '168.61.33.21', '188.214.23.66', '212.68.227.166', '162.144.57.157']
        PROXY = random.choice(list_proxy)
        client = SeleniumClient(driver, PROXY)
        parser = Parser(client)
        parser.run()
