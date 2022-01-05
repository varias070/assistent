import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from articles.models import Article, Image


class Parser:

    def __init__(self, client):
        self.client = client

    def run(self):
        # for n in range(802, 812):
        article = Article.objects.get(id=808)
        data = self.client.extract(article)
        if data is None:
            print(article.link + 'none')
        else:
            article.text = data[1]
            article.header = data[0]
            article.save()


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
        content = []
        list_src = []
        self.driver.get(article.link)
        print(article.link)
        time.sleep(1)
        try:
            body = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="article-render"]')))
            header = self.driver.find_element(By.TAG_NAME, 'h1').text
            element = body.find_elements(By.CSS_SELECTOR, '*')

            result = [header, content, list_src]
            for e in element:
                if e.tag_name == 'p':
                    content.append(e.text)
                elif e.tag_name == 'img':
                    src = e.get_attribute("src")
                    content.append(src)
                    list_src.append(src)
            return result
        except Exception as exc:
            return exc
