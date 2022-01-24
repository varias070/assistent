import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from articlegenerator.settings import *

from articles.models import PublishedPost


class Publicator:

    def __init__(self, client, instance_id):
        self.client = client
        self.instance_id = instance_id

    def run(self):
        published = PublishedPost.objects.get(id=self.instance_id)
        if published.state:
            pass
        else:
            self.client.publish(published)
            published.state = True
            published.save()


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
            button_add = button_add_list[1]
            button_add.click()
        except Exception as exc:
            print(exc)

    def publish(self, published):
        self.driver.get('https://zen.yandex.ru/')
        time.sleep(1)
        self.login(published)
        self.navigate()
        editor = self.driver.find_element(By.CSS_SELECTOR, 'div[class="ql-editor ql-blank"]')

        editor.send_keys(published.prodashka.text)
        p = editor.find_element(By.CSS_SELECTOR, 'p')
        p.send_keys(Keys.CONTROL + 'a')
        time.sleep(1)
        link_input = WebDriverWait(self.driver, 100).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[class="ui-lib-input__control"]')))
        link_input.send_keys(published.prodashka.link)

        p.click()
        p.send_keys(published.post.text)
        p.send_keys(Keys.ENTER)

        label = WebDriverWait(self.driver, 100).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'label[class="brief-desktop-editor-image-button brief-desktop-editor-content__add-image"]')))
        label_input = label.find_element(By.CSS_SELECTOR, 'input[class="brief-desktop-editor-image-button__file-input"]')
        label_input.send_keys(str(BASE_DIR) + published.post.image.url)

        button_publish = self.driver.find_element(By.CSS_SELECTOR, 'button[class="Button2 Button2_view_action Button2_size_m brief-desktop-editor-content__publish-button"]')
        button_publish.click()
