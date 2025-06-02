import pytest
from _pytest.fixtures import FixtureRequest
from base_page import PageNotOpenedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BaseCase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest):
        self.driver = driver
        self.config = config

    def is_opened(self, url, timeout=None):
        if timeout is None:
            timeout = 5

        try:
            WebDriverWait(self.driver, timeout).until(EC.url_matches(url))
            return True
        except TimeoutException:
            raise PageNotOpenedException(
                f'{url} did not open in {timeout} sec. Current URL: {self.driver.current_url}'
            )