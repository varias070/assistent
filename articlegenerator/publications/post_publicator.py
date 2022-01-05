import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from articles.models import PublishedPost


class Publicator:

    def __init__(self, client):
        self.client = client

    def run(self):
        post = PublishedPost.objects.get(id=1)
        self.client.publish()



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
        pass

    def navigate(self):
        avatar_button = self.driver.find_element(By.CSS_SELECTOR, 'button[class="zen-ui-avatar _is-button _icon-size_40"]')
        avatar_button.click()
        avatar_link_list = self.driver.find_elements(By.CSS_SELECTOR,
                                                 'a["zen-ui-header-popup__item _type_action desktop-header__item"]')
        avatar_link = avatar_link_list[1]
        avatar_link.click()
        button_action = self.driver.find_element(By.CSS_SELECTOR, 'div[class="zen-header__add-button"]')
        button_action.click()
        button_add_list = self.driver.find_elements(By.CSS_SELECTOR,
                                                 'button["ui-lib-context-menu__item new-publication-dropdown__button"]')
        button_add = button_add_list[1]
        button_add.click()

    def publish(self):
        self.driver.get('https://zen.yandex.ru/')
        time.sleep(1)
        self.login()
        self.navigate()

