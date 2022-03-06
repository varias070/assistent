import time
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from articlegenerator.settings import *

from articles.models import PublishedPost, Published


class Publicator:

    def __init__(self, client, instance_id):
        self.client = client
        self.instance_id = instance_id

    def run(self):
        published = Published.objects.get(id=self.instance_id)
        self.client.publish(published)


class SeleniumClient:

    def __init__(self, driver):
        self.driver = driver

    def login(self, published):
        try:
            links_login = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'a[class="auth-header-buttons-view__right-link"]')))
            link_login = links_login[1]
            link_login.click()
            input_login = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[class="Textinput-Control"]')))
            input_login.click()
            input_login.send_keys(published.channel.title)
            button = self.driver.find_element(By.ID, 'passp:sign-in')
            button.click()
            password = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.ID, 'passp-field-passwd')))
            password.click()
            password.send_keys(published.channel.login_data)
            password_button = self.driver.find_element(By.ID, 'passp:sign-in')
            password_button.click()
        except Exception as exc:
            print(exc)

    def navigate(self):
        try:
            avatar_button = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[class="zen-ui-avatar _is-button _icon-size_40"]')))
            avatar_button.click()
            avatar_link_list = self.driver.find_elements(By.CSS_SELECTOR,
                                                         'a[class="zen-ui-header-popup__item _type_action desktop-header__item"]')
            avatar_link = avatar_link_list[1]
            avatar_link.click()
            button_add = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="zen-header__add-button"]')))
            button_add.click()
            button_add_list = self.driver.find_elements(By.CSS_SELECTOR,
                                                        'button[class="ui-lib-context-menu__item new-publication-dropdown__button"]')
            button_add = button_add_list[0]
            button_add.click()
        except Exception as exc:
            print(exc)

    def publish(self, published):
        self.driver.get('https://zen.yandex.ru/')
        time.sleep(1)
        self.login(published)
        self.navigate()
        time.sleep(2)
        blank = WebDriverWait(self.driver, 100).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[class="ReactModal__Content ReactModal__Content--after-open help-popup"]')))


        try:
            editor = WebDriverWait(self.driver, 100).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="editor__content"]')))
            header = WebDriverWait(editor, 100).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="editable-input editor__title-input"]')))
            header.send_keys(published.article.header)

            image = WebDriverWait(self.driver, 100).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[class="side-button side-button_logo_image"]')))
            image.click()
        except Exception as exc:
            print(exc)
