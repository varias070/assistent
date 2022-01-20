from celery import shared_task
from publications.post_publicator import *


@shared_task
def start_post_publicator(instance):
    driver = webdriver.Chrome()
    try:
        client = SeleniumClient(driver)
        publicator = Publicator(client, instance)
        publicator.run()
    finally:
        driver.quit()
