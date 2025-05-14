import time

import pytest
import allure
from login_page import LoginPage
from login_locators import LoginPageLocators
from dotenv import load_dotenv

load_dotenv()

class BaseCase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.loginPage = LoginPage(driver)
        if self.authorize:
            self.loginPage.open()


class TestLogin(BaseCase):
    authorize = True

    def test_header(self):
        self.loginPage.check_header()

    def test_switch_language(self):
        title = self.loginPage.find(LoginPageLocators.WELCOME_WORDS)

        self.loginPage.click(LoginPageLocators.RUSSIAN_SELECT)
        assert title.text == 'Добро пожаловать\nв VK Рекламу'

        self.loginPage.click(LoginPageLocators.ENGLISH_SELECT)
        assert title.text == 'Welcome \nto VK Ads'

    def test_success_lk_login(self):
        title = self.loginPage.success_lk_creation()
        assert title.text == 'Регистрация кабинета'

    def test_registration_ads_individual_rus_success(self):
        self.loginPage.registration_ads_ind_rus_success()

    def test_registration_agency_success(self):
        self.loginPage.registration_agency_success()

    def test_invalid_email_registration(self):
        INVALID_EMAILS = ['ex11mple', 'xample@', 'example@mail.', 'example@mail.r']

        for text in self.loginPage.invalid_email_registration(INVALID_EMAILS):
            assert text == 'Некорректный email адрес'

    def test_empty_registration(self):
        alert = self.loginPage.empty_registration()

        assert alert.text == 'Нужно заполнить'

    def test_invalid_inn_registration(self):
        alert = self.loginPage.invalid_inn_registration()

        assert alert.text == 'Напишите не меньше 12 символов'

    def test_currency_availability(self):
        self.loginPage.select_country_currency()
