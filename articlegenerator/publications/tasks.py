from celery import shared_task
from selenium import webdriver

from publications.params_driver import get_chromedriver, get_chromedriver_remote
from publications.post_publicator import *


@shared_task
def start_post_publicator(instance_id):
    driver = get_chromedriver(instance_id, use_proxy=True)
    # driver = get_chromedriver_remote(instance_id, use_proxy=True)

    try:
        client = SeleniumClient(driver)
        publicator = Publicator(client, instance_id)
        publicator.run()
    finally:
        driver.quit()
