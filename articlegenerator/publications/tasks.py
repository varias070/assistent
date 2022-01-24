from celery import shared_task
from selenium import webdriver
from publications.post_publicator import *


@shared_task
def start_post_publicator(instance_id):
    driver = webdriver.Chrome()
    try:
        client = SeleniumClient(driver)
        publicator = Publicator(client, instance_id)
        publicator.run()
    finally:
        driver.quit()
