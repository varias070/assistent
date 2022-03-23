import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from articlegenerator.settings import *

from articles.models import PublishedVideo


class Publicator:

    def __init__(self, client, instance_id):
        self.client = client
        self.instance_id = instance_id

    def run(self):
        published = PublishedVideo.objects.get(id=self.instance_id)
        if published.state:
            pass
        else:
            self.client.publish(published)
            # published.state = True
            # published.save()


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
            button_add = button_add_list[2]
            button_add.click()
        except Exception as exc:
            print(exc)

    def publish(self, published):
        self.driver.get('https://zen.yandex.ru/')
        time.sleep(1)
        self.login(published)
        self.navigate()
        try:
            window = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="ReactModal__Content ReactModal__Content--after-open up-popup video-upload-dialog__up-popup"]')))
            link_input = window.find_element(By.CSS_SELECTOR, 'input[class="video-upload-dialog__file"]')
            # link_input = WebDriverWait(self.driver, 10).until(
            #     EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[class="video-upload-dialog__file"]')))
            link_input.send_keys(str(BASE_DIR) + published.video.link.url)
            blank = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="ui-lib-modal__content publication-modal video-settings-redesign__modal-3X')))

            header = blank.find_element(By.CSS_SELECTOR, 'textarea[class="Textarea-Control Textarea-Control_withMargin"]')
            header.send_keys(published.video.header)

            cover = blank.find_element(By.CSS_SELECTOR, 'input[type="file"]')
            cover.send_keys(str(BASE_DIR) + published.video.cover.url)

            prodashka = blank.find_element(By.CSS_SELECTOR, 'textarea[class="Textarea-Control Textarea-Control_withMargin"]')
            prodashka.send_keys(published.prodashka.text)
            time.sleep(15)
            button_published = WebDriverWait(self.driver, 100).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[class="Button2 Button2_view_action Button2_size_l form-actions__action-15"]')))
            button_published.click()
        except Exception as exc:
            print(exc)
