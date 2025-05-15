import re
import time
import os
from dotenv import load_dotenv
from login_locators import LoginPageLocators
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

load_dotenv()

class PageNotOpenedException(Exception):
    pass

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def is_opened(self, timeout=15):
        started = time.time()
        while time.time() - started < timeout:
            if self.driver.current_url.startswith(self.url):
                return True
        raise PageNotOpenedException(f'{self.url} did not open in {timeout} sec, current url {self.driver.current_url}')

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def click(self, locator, timeout=None):
        elem = self.wait(timeout).until(EC.element_to_be_clickable(locator))
        elem.click()

    def input(self, locator, data, timeout=None):
        elem = self.find(locator, timeout=timeout)
        elem.send_keys(data)

    def clear(self, locator, timeout=None):
        elem = self.find(locator, timeout=timeout)
        elem.clear()

VALID_EMAIL = 'example@mail.ru'
INVALID_INN = '1234567890'

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = os.getenv("BASE_URL")
        print(f"LoginPage: URL из .env = {self.url}")
        if not self.url:
            raise ValueError("BASE_URL не найден в .env файле")

    def open(self):
        self.driver.get(self.url)
        self.is_opened()

    def click_profile_creation(self):
        self.find(LoginPageLocators.PROFILE_CREATION)
        self.click(LoginPageLocators.PROFILE_CREATION)
        welcome_words = self.find(LoginPageLocators.WELCOME_WORDS)
        assert welcome_words.is_displayed(), "Првиетственая страница ВК рекламы не отображается"

    def check_header(self):
        self.find(LoginPageLocators.DROPDOWN_BUTTON)
        self.click(LoginPageLocators.DROPDOWN_BUTTON)
        self.find(LoginPageLocators.CURRENT_LK)
        id_element = self.find(LoginPageLocators.COPY_ID)
        id_pattern = r"^ID: \d{8}$"
        assert re.fullmatch(id_pattern, id_element.text), (
            f"ID должен быть в формате 'ID 12345678', получено: '{id_element.text}'"
        )
        ActionChains(self.driver).move_to_element(id_element).pause(0.5).perform()
        text_item = self.find(LoginPageLocators.COPY_TEXT)
        WebDriverWait(self.driver, 7).until(
            lambda d: "Скопировать ID" in d.find_element(*LoginPageLocators.COPY_TEXT).text
        )
        assert "Скопировать ID" in text_item.text, f"Текст после наведения: {text_item.text}"

    def setup(self):
        self.click(LoginPageLocators.CREATE_NEW_BUTTON)

    def input_valid_email(self):
        self.input(LoginPageLocators.EMAIL_INPUT, VALID_EMAIL)

    def input_email(self, email):
        self.input(LoginPageLocators.EMAIL_INPUT, email)

    def clear_email(self):
        self.clear(LoginPageLocators.EMAIL_INPUT)

    def input_invalid_inn(self):
        self.input(LoginPageLocators.INN_INPUT, INVALID_INN)

    def success_lk_creation(self):
        self.setup()

        title = self.find(LoginPageLocators.TITLE_NEW)

        Select(self.find(LoginPageLocators.COUNTRY_SELECT)).select_by_visible_text('')
        Select(self.find(LoginPageLocators.CURRENCY_SELECT)).select_by_visible_text('')

        self.input_valid_email()

        self.click(LoginPageLocators.MAILING_CHECKBOX)

        return title

    def registration_ads_ind_rus_success(self):
        self.setup()

        self.click(LoginPageLocators.ADS_TYPE)

        self.click(LoginPageLocators.COUNTRY_SELECT_BUTTON)
        self.click(LoginPageLocators.COUNTRY_SELECT_RUSSIA)

        self.click(LoginPageLocators.CURRENCY_SELECT_BUTTON)
        self.click(LoginPageLocators.CURRENCY_SELECT_RUB)

        self.input_valid_email()

        self.find(LoginPageLocators.IND_TYPE)
        self.find(LoginPageLocators.LEGAL_TYPE)

        self.click(LoginPageLocators.IND_TYPE)

        self.find(LoginPageLocators.INN_INPUT)
        self.find(LoginPageLocators.NAME_INPUT)

        self.click(LoginPageLocators.MAILING_CHECKBOX)

    def registration_agency_success(self):
        self.setup()

        self.click(LoginPageLocators.AGENCY_TYPE)

        self.input_valid_email()

        self.find(LoginPageLocators.LEGAL_TYPE)
        self.click(LoginPageLocators.LEGAL_TYPE)

        self.click(LoginPageLocators.MAILING_CHECKBOX_LEGAL)

    def invalid_email_registration(self, emails_list):
        self.setup()

        self.click(LoginPageLocators.ADS_TYPE)
        self.click(LoginPageLocators.IND_TYPE)

        for email in emails_list:
            self.clear_email()
            self.input_email(email)
            self.click(LoginPageLocators.ADS_TYPE)
            alert = self.find(LoginPageLocators.ALERT_CONTAINER)

            yield alert.text

    def empty_registration(self):
        self.setup()

        self.click(LoginPageLocators.SUBMIT_BUTTON)

        alert = self.find(LoginPageLocators.ALERT_CONTAINER)

        return alert

    def invalid_inn_registration(self):
        self.setup()

        self.click(LoginPageLocators.ADS_TYPE)
        self.click(LoginPageLocators.IND_TYPE)

        self.input_valid_email()
        self.input_invalid_inn()

        self.click(LoginPageLocators.SUBMIT_BUTTON)

        alert = self.find(LoginPageLocators.ALERT_CONTAINER)

        return alert

    def select_country_currency(self):
        self.setup()

        rub_countries = [
            LoginPageLocators.COUNTRY_SELECT_RUSSIA,
            LoginPageLocators.COUNTRY_SELECT_BELARUS,
            LoginPageLocators.COUNTRY_SELECT_KAZAKHSTAN,
            LoginPageLocators.COUNTRY_SELECT_TAJIKISTAN
        ]

        for country_locator in rub_countries:
            self.click(LoginPageLocators.COUNTRY_SELECT_BUTTON)
            self.click(country_locator)

            self.click(LoginPageLocators.CURRENCY_SELECT_BUTTON)
            self.find(LoginPageLocators.CURRENCY_SELECT_RUB)