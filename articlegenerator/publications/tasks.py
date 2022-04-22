from celery import shared_task

from publications.params_driver import get_chromedriver, get_chromedriver_remote
from publications.post_publicator import SeleniumClient as PostClient
from publications.post_publicator import Publicator as PublicatorPost
from publications.video_publicator import SeleniumClient as VideoClient
from publications.video_publicator import Publicator as PublicatorVideo
from publications.article_publicator import SeleniumClient as ArticleClient
from publications.article_publicator import Publicator as PublicatorArticle


@shared_task
def start_post_publicator(instance_id):
    index = 1
    driver = get_chromedriver(index, instance_id, use_proxy=True)
    # driver = get_chromedriver_remote(index, instance_id, use_proxy=True)

    try:
        client = PostClient(driver)
        publicator = PublicatorPost(client, instance_id)
        publicator.run()
    finally:
        driver.quit()


@shared_task
def start_video_publicator(instance_id):
    index = 2
    driver = get_chromedriver(index, instance_id, use_proxy=True)
    # driver = get_chromedriver_remote(index, instance_id, use_proxy=True)
    try:
        client = VideoClient(driver)
        publicator = PublicatorVideo(client, instance_id)
        publicator.run()
    finally:
        driver.quit()


@shared_task
def start_article_publicator(instance_id):
    index = 3
    driver = get_chromedriver(index, instance_id, use_proxy=True)

    # driver = get_chromedriver_remote(index, instance_id, use_proxy=True)
    try:
        client = ArticleClient(driver)
        publicator = PublicatorArticle(client, instance_id)
        publicator.run()
    finally:
        driver.quit()
