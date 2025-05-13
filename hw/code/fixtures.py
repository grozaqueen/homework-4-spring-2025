import json
import time  # Required for BasePage.is_opened, but also good practice here if needed

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager  # For get_driver

# Assuming BasePage, MainPage, CampaignsPage are defined elsewhere
# from base_page import BasePage
# from main_page import MainPage
from campaigns_page import CampaignsPage

BASE_URL_FOR_AUTH = "https://ads.vk.com/"


@pytest.fixture(scope='function')
def driver():
    service = Service(executable_path=ChromeDriverManager().install())
    # Options can be added here if needed, e.g., headless, user-agent
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless') # Example
    # driver = webdriver.Chrome(service=service, options=options)
    driver = webdriver.Chrome(service=service)
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

    # Load localStorage
    try:
        with open('localstorage.json', 'r') as f:
            LOCAL_STORAGE_DATA = json.load(f)
    except FileNotFoundError:
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

            # Optional standard attributes
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
                    # Selenium expects 'expiry' as an integer (seconds since epoch)
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
                    # Selenium doesn't support "unspecified". Omitting it lets the browser use its default.
                    pass
                else:
                    print(
                        f"Предупреждение: Неподдерживаемое значение sameSite '{cookie_data_raw['sameSite']}' для cookie {cookie_data_raw['name']}. Поле sameSite не будет установлено.")

            # If SameSite is "None", "secure" must be True.
            if cookie_to_add.get('sameSite') == "None":
                if not cookie_to_add.get('secure', False):
                    # print(f"Информация: Cookie {cookie_to_add['name']} имеет SameSite='None', но 'secure' не True. Устанавливаю 'secure': True.")
                    cookie_to_add['secure'] = True

            try:
                driver.add_cookie(cookie_to_add)
                added_cookies_count += 1
            except Exception as e:
                # Use !r for a more detailed representation of the exception
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
                # Ensure value is a string, as localStorage stores strings
                str_value = json.dumps(value) if not isinstance(value, str) else value
                driver.execute_script(f"window.localStorage.setItem(arguments[0], arguments[1]);", key, str_value)
                items_set += 1
            except Exception as e:
                print(f"Ошибка при установке localStorage для ключа {key}: {e!r}")
        print(f"{items_set} элемент(ов) localStorage из {len(LOCAL_STORAGE_DATA)} (попытка установки).")
    else:
        print("Данные для Local Storage не предоставлены или файл не найден/поврежден.")

    print("Обновление страницы для применения cookie/localStorage...")
    driver.refresh()  # Crucial: refresh to apply session data

    yield driver
    print("Закрытие браузера")
    driver.quit()


def get_driver(browser_name, config=None):  # Added config as optional if needed by url line
    if browser_name == 'chrome':
        service = Service(executable_path=ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service)
    elif browser_name == 'firefox':
        service = Service(executable_path=GeckoDriverManager().install())  # Corrected for Firefox
        browser = webdriver.Firefox(service=service)
    else:
        raise RuntimeError(f'Unsupported browser: "{browser_name}"')
    browser.maximize_window()
    return browser


@pytest.fixture(scope='session', params=['chrome', 'firefox'])
def all_drivers(config, request):  # config is used here
    # Ensure config is available if you're using it, or pass it to get_driver if needed
    # If config['url'] is not essential for the basic driver setup, it can be handled differently.
    # For now, assuming config is passed and contains 'url'.
    # If 'config' is not defined for the 'driver' fixture context, this 'all_drivers' fixture might be separate.
    # The error is with the 'driver' fixture, so focusing on that. This 'all_drivers' fixture seems for a different purpose.

    # If config is not available in this specific context, this part may need adjustment
    # url = config.get('url', 'http://example.com') # Fallback or ensure config is passed

    browser = get_driver(request.param)  # Removed config from get_driver call if not used there

    # If you need to navigate, do it here.
    # For instance, if config fixture provides the URL:
    if 'url' in config:
        browser.get(config['url'])

    yield browser
    browser.quit()


@pytest.fixture
def campaigns_page(driver):
    # Ensure CampaignsPage.url is a valid, accessible URL
    driver.get(CampaignsPage.url)
    return CampaignsPage(driver=driver)


# Dummy BasePage and MainPage for completeness if they are not imported from actual files
# These should be imported from your project structure.
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        # self.is_opened() # Call this only if appropriate for all base pages on init

    def find_element(self, locator, time=10):
        # Dummy find_element
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        return WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator))

    def is_opened(self, timeout=10):  # Reduced timeout for example
        started = time.time()
        while time.time() - started < timeout:
            if self.driver.current_url:  # Check if current_url is not None
                # Assuming self.url is defined in subclasses like CampaignsPage
                if self.driver.current_url.rstrip('/') == getattr(self, 'url', '').rstrip('/'):
                    return True
            time.sleep(0.1)  # Small delay before retrying
        raise TimeoutError(f"Page {getattr(self, 'url', '')} not opened. Current URL: {self.driver.current_url}")


class MainPage(BasePage):
    url = "https://ads.vk.com/main"  # Example URL

    def __init__(self, driver):
        super().__init__(driver)
        self.is_opened()  # Example: Check if opened on initialization


# Make sure CampaignsPage is correctly defined, e.g.:
# from campaigns_page import CampaignsPage
# If CampaignsPage.url is not static, it needs to be set appropriately.

@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)  # Note: BasePage usually isn't instantiated directly for tests


@pytest.fixture
def main_page(driver):
    # driver.get(MainPage.url) # Navigation should be part of page object action or fixture setup
    return MainPage(driver=driver)