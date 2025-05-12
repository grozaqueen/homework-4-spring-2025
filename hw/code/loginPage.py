import re
import time
import os
from dotenv import load_dotenv
from loginLocators import LoginPageLocators
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

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

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = os.getenv("BASE_URL")
        print(f"LoginPage: URL из .env = {self.url}")
        if not self.url:
            raise ValueError("BASE_URL не найден в .env файле")

    def open(self):
        print(f"Открываем URL: {self.url}")
        self.driver.get(self.url)
        self.is_opened()

    def click_registration(self):
        print("Ищем кнопку регистрации...")
        button = self.find(LoginPageLocators.REGISTRATION_BUTTON)
        print(f"Кнопка регистрации найдена: {button.is_displayed()}")
        self.click(LoginPageLocators.REGISTRATION_BUTTON)
        modal = self.find(LoginPageLocators.REGISTRATION_MODAL)
        assert modal.is_displayed(), "Модальное окно входа не отображается"

    def click_profile_creation(self):
        print("Ищем кнопку создания профиля бизнеса...")
        button = self.find(LoginPageLocators.PROFILE_CREATION)
        print(f"Кнопка создания профиля бизнеса найдена: {button.is_displayed()}")
        self.click(LoginPageLocators.PROFILE_CREATION)
        welcome_words = self.find(LoginPageLocators.WELCOME_WORDS)
        print("Првиетственая страница ВК рекламы не отображается")
        assert welcome_words.is_displayed(), "Првиетственая страница ВК рекламы не отображается"

    def check_header(self):
        print("Ищем кнопку кабинета...")
        button = self.find(LoginPageLocators.DROPDOWN_BUTTON)
        print(f"Кнопка кабинета найдена: {button.is_displayed()}")
        self.click(LoginPageLocators.DROPDOWN_BUTTON)
        button_of_current_lk = self.find(LoginPageLocators.CURRENT_LK)
        print(f"Кнопка текущего кабинета найдена: {button_of_current_lk.is_displayed()}")
        print("Находим элемент с ID...")
        time.sleep(5)
        id_element = self.find(LoginPageLocators.COPY_ID)
        print("Проверяем начальное состояние (текст должен быть ID)...")
        id_pattern = r"^ID: \d{8}$"
        assert re.fullmatch(id_pattern, id_element.text), (
            f"ID должен быть в формате 'ID 12345678', получено: '{id_element.text}'"
        )
        print("Наводим курсор на элемент...")
        time.sleep(5)
        ActionChains(self.driver).move_to_element(id_element).pause(0.5).perform()
        time.sleep(5)
        print("Проверяем текст после наведения...")
        text_item = self.find(LoginPageLocators.COPY_TEXT)
        WebDriverWait(self.driver, 7).until(
            lambda d: "Скопировать ID" in d.find_element(*LoginPageLocators.COPY_TEXT).text
        )
        assert "Скопировать ID" in text_item.text, f"Текст после наведения: {text_item.text}"

        print("Кликаем на элемент...")
        id_element.click()
        print("Проверяем текст после клика...")
        assert "Готово!" in id_element.text, f"Текст после клика: {id_element.get_dom_attribute('class')}"

        print("Проверяем возврат в исходное состояние...")
        ActionChains(self.driver).move_by_offset(10, 10).perform()
        WebDriverWait(self.driver, 5).until(
            lambda d: "ID_" in d.find_element(*LoginPageLocators.COPY_ID).text
        )
        assert "ID_" in id_element.text, "Элемент не вернулся в исходное состояние"

