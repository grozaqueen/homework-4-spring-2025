import os
import time
import re
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
        self.loginPage.open_dropdown()
        current_lk_element, id_element = self.loginPage.get_header_elements()

        id_pattern = r"^ID: \d{8}$"
        assert re.fullmatch(id_pattern, id_element.text), (
            f"ID должен быть в формате 'ID 12345678', получено: '{id_element.text}'"
        )

        text_item = self.loginPage.hover_over_id_and_get_text(id_element)
        assert "Скопировать ID" in text_item.text, f"Текст после наведения: {text_item.text}"

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
        assert self.driver.current_url == os.getenv("BASE_URL")

    def test_registration_agency_success(self):
        self.loginPage.registration_agency_success()
        assert self.driver.current_url == os.getenv("BASE_URL")

    @pytest.mark.parametrize("invalid_email", [
        'ex11mple',
        'xample@',
        'example@mail.',
        'example@mail.r',
        pytest.param('valid@mail.ru', marks=pytest.mark.xfail),
    ])

    def test_invalid_email_registration(self, invalid_email):
        error_text = self.loginPage.check_single_invalid_email(invalid_email)
        assert error_text == 'Некорректный email адрес', f"Ошибка для email: {invalid_email}"

    def test_empty_registration(self):
        alert = self.loginPage.empty_registration()
        assert alert.text == 'Нужно заполнить'

    def test_invalid_inn_registration(self):
        alert = self.loginPage.invalid_inn_registration()
        assert alert.text == 'Напишите не меньше 12 символов'

    def test_currency_availability(self):
        result = self.loginPage.select_country_currency()
        assert result is True