import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from articles.models import Article, ArticleBlock


class Parser:
    counter = 0

    def __init__(self, client):
        self.client = client

    def run(self):
        article = Article.objects.get(id=25802)
        data = self.client.extract(article)

        for e in data:
            block = ArticleBlock(article=article, text=e.text, ordering_number=self.increment(), src=e.get_attribute('src'))
            block.save()

    def increment(self):
        self.counter += 1
        counterString = self.counter.__str__()
        return counterString


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
        self.driver.get(article.link)
        time.sleep(1)
        try:
            body = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="article-render"]')))
            element = body.find_elements(By.CSS_SELECTOR, '*')

            result = []
            for e in element:
                if e.tag_name == 'span':
                    result.append(e)
                elif e.tag_name == 'img':
                    result.append(e)
            return result
        except Exception as exc:
            return exc
