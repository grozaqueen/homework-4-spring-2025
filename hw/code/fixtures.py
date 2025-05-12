import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope='function')
def driver():
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    print("Запуск браузера")
    yield driver
    print("Закрытие браузера")
    driver.quit()


def get_driver(browser_name):
    if browser_name == 'chrome':
        browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    elif browser_name == 'firefox':
        browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    else:
        raise RuntimeError(f'Unsupported browser: "{browser_name}"')
    browser.maximize_window()
    return browser


@pytest.fixture(scope='session', params=['chrome', 'firefox'])
def all_drivers(config, request):
    url = config['url']
    browser = get_driver(request.param)
    browser.get(url)
    yield browser
    browser.quit()


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def main_page(driver):
    return MainPage(driver=driver)
