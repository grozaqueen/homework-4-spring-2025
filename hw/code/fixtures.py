import json
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from campaigns_page import CampaignsPage
from audience_page import AudiencePage
from login_page import LoginPage
from leadform_page import LeadFormPage

BASE_URL_FOR_AUTH = "https://ads.vk.com/"


@pytest.fixture(scope='function')
def driver():
    service = Service(executable_path=ChromeDriverManager().install())

    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(service=service, options=options)

    print("Запуск браузера")

    driver.get(BASE_URL_FOR_AUTH)
    print(f"Навигация на {BASE_URL_FOR_AUTH} для установки cookie/localStorage")

    # Load cookies
    try:
        with open('cookies.json', 'r') as f:
            COOKIES_DATA = json.load(f)
    except FileNotFoundError:
        print("Файл cookies.json не найден.")
        COOKIES_DATA = []
    except json.JSONDecodeError:
        print("Ошибка декодирования cookies.json.")
        COOKIES_DATA = []

    try:
        with open('localstorage.json', 'r') as f:
            LOCAL_STORAGE_DATA = json.load(f)
    except FileNotFoundError:
        print("Файл localstorage.json не найден.")
        LOCAL_STORAGE_DATA = {}
    except json.JSONDecodeError:
        print("Ошибка декодирования localstorage.json.")
        print("Файл localstorage.json не найден.")
        LOCAL_STORAGE_DATA = {}
    except json.JSONDecodeError:
        print("Ошибка декодирования localstorage.json.")
        LOCAL_STORAGE_DATA = {}

    if COOKIES_DATA:
        print("Установка Cookies...")
        added_cookies_count = 0
        for cookie_data_raw in COOKIES_DATA:
            cookie_to_add = {}

            if "name" not in cookie_data_raw or "value" not in cookie_data_raw:
                print(
                    f"Предупреждение: Неполные данные (отсутствует name или value) для cookie, cookie не добавлен: {cookie_data_raw}")
                continue

            cookie_to_add['name'] = cookie_data_raw['name']
            cookie_to_add['value'] = cookie_data_raw['value']

            if 'path' in cookie_data_raw:
                cookie_to_add['path'] = cookie_data_raw['path']
            if 'domain' in cookie_data_raw:
                cookie_to_add['domain'] = cookie_data_raw['domain']
            if 'secure' in cookie_data_raw:
                cookie_to_add['secure'] = cookie_data_raw['secure']
            if 'httpOnly' in cookie_data_raw:
                cookie_to_add['httpOnly'] = cookie_data_raw['httpOnly']

            if 'expirationDate' in cookie_data_raw:
                try:
                    cookie_to_add['expiry'] = int(cookie_data_raw['expirationDate'])
                except (ValueError, TypeError):
                    print(
                        f"Предупреждение: Некорректное значение expirationDate для cookie {cookie_data_raw['name']}, поле expiry не установлено: {cookie_data_raw['expirationDate']}")

            if 'sameSite' in cookie_data_raw:
                samesite_raw_value = str(cookie_data_raw['sameSite']).lower()
                if samesite_raw_value == "no_restriction":
                    cookie_to_add['sameSite'] = "None"
                elif samesite_raw_value == "lax":
                    cookie_to_add['sameSite'] = "Lax"
                elif samesite_raw_value == "strict":
                    cookie_to_add['sameSite'] = "Strict"
                elif samesite_raw_value == "unspecified":
                    pass
                else:
                    print(
                        f"Предупреждение: Неподдерживаемое значение sameSite '{cookie_data_raw['sameSite']}' для cookie {cookie_data_raw['name']}. Поле sameSite не будет установлено.")

            if cookie_to_add.get('sameSite') == "None":
                if not cookie_to_add.get('secure', False):
                    print(f"Информация: Cookie {cookie_to_add['name']} имеет SameSite='None', но 'secure' не True. Устанавливаю 'secure': True.")

                    cookie_to_add['secure'] = True

            try:
                driver.add_cookie(cookie_to_add)
                added_cookies_count += 1
            except Exception as e:
                print(
                    f"Ошибка при добавлении cookie {cookie_to_add.get('name', 'UNKNOWN_NAME')} (данные: {cookie_to_add}): {e!r}")

        print(f"{added_cookies_count} cookie из {len(COOKIES_DATA)} успешно (попытка установки).")
    else:
        print("Данные для Cookies не предоставлены или файл не найден/поврежден.")

    if LOCAL_STORAGE_DATA:
        print("Установка Local Storage...")
        items_set = 0
        for key, value in LOCAL_STORAGE_DATA.items():
            try:

                str_value = json.dumps(value) if not isinstance(value, str) else value
                driver.execute_script(f"window.localStorage.setItem(arguments[0], arguments[1]);", key, str_value)
                items_set += 1
            except Exception as e:
                print(f"Ошибка при установке localStorage для ключа {key}: {e!r}")
        print(f"{items_set} элемент(ов) localStorage из {len(LOCAL_STORAGE_DATA)} (попытка установки).")
    else:
        print("Данные для Local Storage не предоставлены или файл не найден/поврежден.")

    print("Обновление страницы для применения cookie/localStorage...")
    driver.refresh()

    driver.maximize_window()
    yield driver
    print("Закрытие браузера")
    driver.quit()


def get_driver(browser_name, config=None):
    if browser_name == 'chrome':
        service = Service(executable_path=ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service)

    else:
        raise RuntimeError(f'Unsupported browser: "{browser_name}"')
    browser.maximize_window()
    return browser


@pytest.fixture(scope='session', params=['chrome', 'firefox'])
def all_drivers(config, request):  # config is used here

    browser = get_driver(request.param)

    if 'url' in config:
        browser.get(config['url'])

    yield browser
    browser.quit()


@pytest.fixture

def leadform_page(driver):

    driver.get(LeadFormPage.url)
    return LeadFormPage(driver=driver)

def campaigns_page(driver):
    driver.get(CampaignsPage.url)
    return CampaignsPage(driver=driver)

def audience_page(driver):
    driver.get(AudiencePage.url)
    return AudiencePage(driver=driver)

def login_page(driver):
    driver.get(LoginPage.url)
    return LoginPage(driver=driver)


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator, time=10):
        # Dummy find_element
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        return WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator))

    def is_opened(self, timeout=10):
        started = time.time()
        while time.time() - started < timeout:
            if self.driver.current_url:  # Check if current_url is not None
                if self.driver.current_url.rstrip('/') == getattr(self, 'url', '').rstrip('/'):
                    return True
            time.sleep(0.1)
        raise TimeoutError(f"Page {getattr(self, 'url', '')} not opened. Current URL: {self.driver.current_url}")


class MainPage(BasePage):
    url = "https://ads.vk.com/main"  # Example URL

    def __init__(self, driver):
        super().__init__(driver)
        self.is_opened()


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def main_page(driver):
    return MainPage(driver=driver)

