import time

import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import allure
from loginPage import LoginPage
import os
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

    @allure.title("Тест успешной авторизации")
    @allure.step("Проверка перенаправления и отображения элементов главной страницы")
    def test_login(self):
        self.loginPage.click_registration()
        time.sleep(20)
        self.loginPage.click_profile_creation()

    def test_header(self):
        self.loginPage.click_registration()
        time.sleep(20)
        self.loginPage.click_profile_creation()
        self.loginPage.check_header()
        time.sleep(20)
