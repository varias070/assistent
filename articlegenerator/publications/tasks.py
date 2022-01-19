import random

from celery import shared_task
from publications.post_publicator import *


@shared_task
def start_post_publicator(instance):
    driver = webdriver.Chrome()
    list_proxy = ["182.92.242.11", '200.239.64.36', '168.61.33.21', '188.214.23.66', '212.68.227.166', '162.144.57.157']
    PROXY = random.choice(list_proxy)
    client = SeleniumClient(driver, PROXY)
    publicator = Publicator(client, instance)
    publicator.run()
