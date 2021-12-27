import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from articles.models import Article, Image


class Parser:

    def __init__(self, client):
        self.client = client

    def run(self):
        for n in range(802, 812):
            article = Article.objects.get(id=n)
            data = self.client.extract(article)
            # article.text = data[:2]
            # article.header = data[2]
            # article.save()
            #
            # list_src = data[0]
            # for src in list_src:
            #     image = Image()
            #     image.link = src
            #     image.article = article
            #     image.save()


class SeleniumClient:

    def __init__(self, driver, PROXY):
        self.driver = driver
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy": PROXY,
            "ftpProxy": PROXY,
            "sslProxy": PROXY,
            "proxyType": "MANUAL",
        }

    def extract(self, article):
        result = []
        self.driver.get(article.link)
        time.sleep(1)
        body = self.driver.find_element(By.TAG_NAME, 'article')

        images = body.find_elements(By.TAG_NAME, 'img')
        list_src = []
        for img in images:
            src = img.get_attribute("src")
            print(src)
            list_src.append(src)
        header = body.find_element(By.TAG_NAME, 'h1').text
        elements = body.find_elements(By.TAG_NAME, 'p').is_enabled()
        if elements:
            elements = body.find_elements(By.TAG_NAME, 'p')
            text = []
            for element in elements:
                print(element.text)
                el_text = element.text
                text.append(el_text)
            result.extend([list_src, text, header])
        else:
            result.extend([list_src, header])
        return result
