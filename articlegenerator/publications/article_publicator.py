import time
import pyperclip

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from articlegenerator.settings import *

from articles.models import PublishedArticle, ArticleBlock


class Publicator:

    def __init__(self, client, instance_id):
        self.client = client
        self.instance_id = instance_id

    def run(self):
        published = PublishedArticle.objects.get(id=self.instance_id)
        article_blocks = ArticleBlock.objects.filter(article=published.article.id)
        self.client.publish(published, article_blocks)
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
            button_add = button_add_list[0]
            button_add.click()
        except Exception as exc:
            print(exc)

    def publish(self, published, article_blocks):
        self.driver.get('https://zen.yandex.ru/')
        time.sleep(1)
        self.login(published)
        self.navigate()
        # клик в свободной точки для что бы закрыть диалоговое окно
        self.driver.execute_script('el = document.elementFromPoint(440, 120); el.click();')

        try:
            header = WebDriverWait(self.driver, 100).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="public-DraftStyleDefault-block public-DraftStyleDefault-ltr"]')))
            header.send_keys(published.article.header)
            content = WebDriverWait(self.driver, 100).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, 'div[class="zen-editor-block zen-editor-block-paragraph"]')))
            button_image = WebDriverWait(self.driver, 100).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[class="side-button side-button_logo_image"]')))

            if published.prodaska:
                content.send_keys(published.prodaska.text)
                content.send_keys(Keys.ENTER)

            for block in article_blocks:
                if block.text:
                    content.send_keys(block.text)
                    content.send_keys(Keys.ENTER)

                elif block.src:
                    time.sleep(1)
                    button_image.click()
                    input_image = WebDriverWait(self.driver, 100).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Ссылка"]')))
                    pyperclip.copy(block.src)
                    input_image.click()
                    input_image.send_keys(Keys.CONTROL + 'v')

            if published.prodaska:
                content.send_keys(published.prodaska.text)
                content.send_keys(Keys.CONTROL + 'a')

            button_publication = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[class="Button2 Button2_view_action Button2_size_s editor-header__edit-btn"]')))
            button_publication.click()

            button_publication2 = WebDriverWait(self.driver, 100).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[class="ui-lib-button-base _is-transition-enabled ui-lib-button _size_l _view-type_yellow _width-type_regular publication-settings-actions__action"]')))
            button_publication2.click()

            time.sleep(5)
        except Exception as exc:
            print(exc)
