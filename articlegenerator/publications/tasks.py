from celery import shared_task

from publications.params_driver import get_chromedriver, get_chromedriver_remote


@shared_task
def start_post_publicator(instance_id):
    from publications.post_publicator import SeleniumClient
    from publications.post_publicator import Publicator
    index = 1
    driver = get_chromedriver(index, instance_id, use_proxy=True)
    # driver = get_chromedriver_remote(instance_id, use_proxy=True)

    try:
        client = SeleniumClient(driver)
        publicator = Publicator(client, instance_id)
        publicator.run()
    finally:
        driver.quit()


@shared_task
def start_video_publicator(instance_id):
    from publications.video_publicator import SeleniumClient
    from publications.video_publicator import Publicator
    index = 2
    # driver = get_chromedriver(index, instance_id, use_proxy=True)
    driver = get_chromedriver_remote(index, instance_id, use_proxy=True)
    try:
        client = SeleniumClient(driver)
        publicator = Publicator(client, instance_id)
        publicator.run()
    finally:
        driver.quit()
