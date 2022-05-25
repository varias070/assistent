import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from articles.models import Article
from .models import ParserState


class Parser:

    def __init__(self, client):
        self.client = client
        self.pages = [1, 100]

    def run(self):
        page = 0
        articles_numbers = []
        list_link = self.client.get_page(self.pages)
        i = 0
        for link in list_link:
            article = Article(link=link)
            article.save()
            articles_numbers.append(article.id)
            i += 1
            if i == 50:  # 50 links per page
                i = 0   # reset page links
                page += 1
                state = ParserState(page_number=page)
                state.save()

        return articles_numbers


class SeleniumClient:

    def __init__(self, driver, PROXY):
        self.driver = driver
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy": PROXY,
            "ftpProxy": PROXY,
            "sslProxy": PROXY,
            "proxyType": "MANUAL",
        }

    def login(self):
        self.driver.get('https://zenstat.ru/user/login/')
        email = self.driver.find_element(By.NAME, 'email')
        email.send_keys('mobileoptroz@mail.ru')
        password = self.driver.find_element(By.NAME, 'password')
        password.send_keys('kekulu007')
        log_in = self.driver.find_element(By.CSS_SELECTOR, 'input[class="btn btn-primary btn-submit"]')
        log_in.click()

        time.sleep(1)

        self.driver.get('https://zenstat.ru/stat/posts/?search=&sort=views&order=desc&offset=0&limit=50&type_post=card&date_from=2021-01-01&date_to=2021-12-31&period=2021&post_title=&views_min=3000&views_max=&views_till_end_min=&views_till_end_max=&views_till_end_percent_min=&views_till_end_percent_max=&channel_subscribers_min=&channel_subscribers_max=1500&fast_load=1')

    def get_links(self):
        next_page = self.driver.find_element(By.CSS_SELECTOR, 'li[class="page-item page-next"]')
        next_page.click()

    def get_page(self, pages):
        links = []
        SeleniumClient.login(self)
        start_page = pages[0]
        stop_page = pages[1]
        i = 1

        while i < start_page:
            SeleniumClient.get_links(self)
            i += 1
        while i <= stop_page:

            time.sleep(2)

            table_link = self.driver.find_element(By.ID, 'data-table')
            table_link_body = table_link.find_element(By.TAG_NAME, 'tbody')
            list_tr = table_link_body.find_elements(By.TAG_NAME, 'tr')
            for tr in list_tr:
                list_td = tr.find_elements(By.TAG_NAME, 'td')
                link_td = list_td[1]
                link = link_td.find_element(By.TAG_NAME, 'a')
                href = (link.get_attribute('href'))
                links.append(href)

            SeleniumClient.get_links(self)
            i += 1
        self.driver.quit()
        return links
