import json
import logging

import pytest
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
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
    logger.info(f"Навигация на {BASE_URL_FOR_AUTH} для установки cookie/localStorage")

    try:
        with open('cookies.json', 'r') as f:
            COOKIES_DATA = json.load(f)
    except FileNotFoundError:
        logger.warning("Файл cookies.json не найден.")
        COOKIES_DATA = []
    except json.JSONDecodeError:
        logger.error("Ошибка декодирования cookies.json.")
        COOKIES_DATA = []

    try:
        with open('localstorage.json', 'r') as f:
            LOCAL_STORAGE_DATA = json.load(f)
    except FileNotFoundError:
        logger.warning("Файл localstorage.json не найден.")
        LOCAL_STORAGE_DATA = {}
    except json.JSONDecodeError:

        print("Ошибка декодирования localstorage.json.")
        print("Файл localstorage.json не найден.")
        LOCAL_STORAGE_DATA = {}
    except json.JSONDecodeError:
        print("Ошибка декодирования localstorage.json.")

        LOCAL_STORAGE_DATA = {}

    if COOKIES_DATA:
        logger.info("Установка Cookies...")
        added_cookies_count = 0
        for cookie_data_raw in COOKIES_DATA:
            cookie_to_add = {}

            if "name" not in cookie_data_raw or "value" not in cookie_data_raw:
                logger.warning(
                    f"Неполные данные (отсутствует name или value) для cookie, cookie не добавлен: {cookie_data_raw}")
                continue

            cookie_to_add['name'] = cookie_data_raw['name']
            cookie_to_add['value'] = cookie_data_raw['value']

            if 'path' in cookie_data_raw: cookie_to_add['path'] = cookie_data_raw['path']
            if 'domain' in cookie_data_raw: cookie_to_add['domain'] = cookie_data_raw['domain']
            if 'secure' in cookie_data_raw: cookie_to_add['secure'] = cookie_data_raw['secure']
            if 'httpOnly' in cookie_data_raw: cookie_to_add['httpOnly'] = cookie_data_raw['httpOnly']

            if 'expirationDate' in cookie_data_raw:
                try:
                    cookie_to_add['expiry'] = int(cookie_data_raw['expirationDate'])
                except (ValueError, TypeError):
                    logger.warning(
                        f"Некорректное значение expirationDate для cookie {cookie_data_raw['name']}, поле expiry не установлено: {cookie_data_raw['expirationDate']}")

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
                    logger.warning(
                        f"Неподдерживаемое значение sameSite '{cookie_data_raw['sameSite']}' для cookie {cookie_data_raw['name']}. Поле sameSite не будет установлено.")

            if cookie_to_add.get('sameSite') == "None" and not cookie_to_add.get('secure', False):
                logger.info(
                    f"Cookie {cookie_to_add['name']} имеет SameSite='None', но 'secure' не True. Устанавливаю 'secure': True.")
                cookie_to_add['secure'] = True

            try:
                driver.add_cookie(cookie_to_add)
                added_cookies_count += 1
            except Exception as e:
                logger.error(
                    f"Ошибка при добавлении cookie {cookie_to_add.get('name', 'UNKNOWN_NAME')} (данные: {cookie_to_add}): {e!r}")

        logger.info(f"{added_cookies_count} cookie из {len(COOKIES_DATA)} (попытка установки).")
    else:
        logger.info("Данные для Cookies не предоставлены или файл не найден/поврежден.")

    if LOCAL_STORAGE_DATA:
        logger.info("Установка Local Storage...")
        items_set = 0
        for key, value in LOCAL_STORAGE_DATA.items():
            try:
                str_value = json.dumps(value) if not isinstance(value, str) else value
                driver.execute_script(f"window.localStorage.setItem(arguments[0], arguments[1]);", key, str_value)
                items_set += 1
            except Exception as e:
                logger.error(f"Ошибка при установке localStorage для ключа {key}: {e!r}")
        logger.info(f"{items_set} элемент(ов) localStorage из {len(LOCAL_STORAGE_DATA)} (попытка установки).")
    else:
        logger.info("Данные для Local Storage не предоставлены или файл не найден/поврежден.")

    logger.info("Обновление страницы для применения cookie/localStorage...")
    driver.refresh()

    driver.maximize_window()
    yield driver
    logger.info("Закрытие браузера")
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
def all_drivers(config, request):
    browser = get_driver(request.param)

    if config and 'url' in config:
        browser.get(config['url'])

    yield browser
    browser.quit()


@pytest.fixture

def leadform_page(driver):

    driver.get(LeadFormPage.url)
    return LeadFormPage(driver=driver)

def campaigns_page(driver):
    return CampaignsPage(driver=driver)


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.url = None

    def find_element(self, locator, time=10):
        from selenium.webdriver.support import expected_conditions as EC
        return WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator))

    def is_opened(self, timeout=10):
        expected_url = getattr(self, 'url', None)
        if not expected_url:
            logger.warning(f"Page {self.__class__.__name__} has no 'url' attribute. Cannot verify if opened by URL.")
            return True

        expected_url_stripped = expected_url.rstrip('/')

        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.current_url is not None and \
                          d.current_url.rstrip('/') == expected_url_stripped
            )
            return True
        except TimeoutException:
            current_url = self.driver.current_url
            logger.error(
                f"Page with expected URL '{expected_url_stripped}' was not opened within {timeout} seconds. "
                f"Current URL: '{current_url}'"
            )
            return False


class MainPage(BasePage):
    url = "https://ads.vk.com/main"

    def __init__(self, driver):
        super().__init__(driver)


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def main_page(driver):
    return MainPage(driver=driver)

