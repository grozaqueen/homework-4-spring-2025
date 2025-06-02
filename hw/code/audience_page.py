from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base_page import BasePage, DEFAULT_TIMEOUT
from audience_page_locators import AudiencePageLocators
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class AudiencePage(BasePage):
    url = 'https://ads.vk.com/hq/audience'
    locators = AudiencePageLocators()

    def click_create_audience(self, timeout=DEFAULT_TIMEOUT):
        self.click(locator=self.locators.CREATE_AUDIENCE_BUTTON, timeout=timeout)

    def click_add_source(self, timeout=DEFAULT_TIMEOUT):
        self.click(locator=self.locators.ADD_SOURCE, timeout=timeout)

    def enter_audience_name(self, name, timeout=DEFAULT_TIMEOUT):
        self.send_keys_to_input(locator=self.locators.NAME_INPUT, keys=name+Keys.ENTER, timeout=timeout)

    def click_user_list_option(self, timeout=DEFAULT_TIMEOUT):
        self.click(locator=self.locators.USER_LIST_OPTION, timeout=timeout)

    def click_submit_list(self, timeout=DEFAULT_TIMEOUT):
        self.click(locator=self.locators.SUBMIT_LIST_BUTTON, timeout=timeout)

    def click_submit(self, timeout=DEFAULT_TIMEOUT):
        self.click(locator=self.locators.SUBMIT_BUTTON, timeout=timeout)

    def choose_load_new(self, timeout=DEFAULT_TIMEOUT):
        self.click(locator=self.locators.LOAD_NEW_OPTION, timeout=timeout)

    def enter_list_name(self, name, timeout=DEFAULT_TIMEOUT):
        self.send_keys_to_input(locator=self.locators.LIST_NAME_INPUT, keys=name+Keys.ENTER, timeout=timeout)

    def choose_unified_list(self, timeout=DEFAULT_TIMEOUT):
        self.click(locator=self.locators.LIST_TYPE_SELECT, timeout=timeout)
        self.click(locator=self.locators.UNIFIED_LIST_OPTION, timeout=timeout)

    def load_unified_list(self, filename='list.csv', timeout=DEFAULT_TIMEOUT):
        filepath = self._get_static_filepath(filename=filename)
        inp = self.find(locator=self.locators.FILE_INPUT, timeout=timeout)
        inp.send_keys(filepath)

    def enter_user_list_info(self, name, timeout=DEFAULT_TIMEOUT):
        self.enter_list_name(name=name, timeout=timeout)
        self.choose_unified_list(timeout=timeout)
        self.load_unified_list(timeout=timeout)
        self.click_submit_list(timeout=timeout)
        assert self.became_invisible(locator=self.locators.ADD_USER_LIST_HEADER, timeout=timeout)

    def create_audience_from_user_list(self, name, list_name, timeout=DEFAULT_TIMEOUT):
        self.click(locator=self.locators.AUDIENCES_MENU_ITEM, timeout=timeout)
        self.click_create_audience(timeout=timeout)
        self.enter_audience_name(name=name, timeout=timeout)
        self.click_add_source(timeout=timeout)
        self.click_user_list_option(timeout=timeout)
        self.choose_load_new(timeout=timeout)
        self.enter_user_list_info(name=list_name, timeout=timeout)
        self.click_submit(timeout=timeout)
        assert self.became_invisible(locator=self.locators.ADD_AUDIENCE_HEADER, timeout=timeout)

    def assert_audience_visible(self, name, timeout=DEFAULT_TIMEOUT):
        loc = self.locators.get_audience_name(name=name)
        assert self.became_visible(locator=loc, timeout=timeout)

    def assert_audience_not_visible(self, name, timeout=DEFAULT_TIMEOUT):
        loc = self.locators.get_audience_name(name=name)
        assert self.became_invisible(locator=loc, timeout=timeout)

    def click_delete_and_confirm(self, name, timeout=DEFAULT_TIMEOUT):
        loc = self.locators.get_by_data_testid(name=name)
        self.hover(locator=loc, timeout=timeout)
        self.click(locator=loc, timeout=timeout)
        self.click(locator=self.locators.DELETE_BUTTON, timeout=timeout)
        self.click(locator=self.locators.DELETE_BUTTON, timeout=timeout)

    def delete_audience(self, name, timeout=DEFAULT_TIMEOUT):
        self.click(locator=self.locators.AUDIENCES_MENU_ITEM, timeout=timeout)
        self.click_delete_and_confirm(name=name, timeout=timeout)

    def delete_user_list(self, name, timeout=DEFAULT_TIMEOUT):
        self.click(locator=self.locators.USER_LIST_MENU_ITEM, timeout=timeout)
        self.click_delete_and_confirm(name=name, timeout=timeout)

    def search_for_audience(self, name, timeout=DEFAULT_TIMEOUT):
        self.send_keys_to_input(locator=self.locators.SEARCH_INPUT, keys=name+Keys.ENTER, timeout=timeout)

    def clear_search(self):
        self.locators.SEARCH_INPUT.clear()

    def create_user_list(self, name, timeout=DEFAULT_TIMEOUT):
        self.click(locator=self.locators.USER_LIST_MENU_ITEM, timeout=timeout)
        self.click(locator=self.locators.CREATE_USER_LIST_BUTTON, timeout=timeout)
        self.enter_user_list_info(name=name, timeout=timeout)

    def assert_user_list_visible(self, name, timeout=DEFAULT_TIMEOUT):
        assert self.became_visible(locator=self.locators.get_user_list_name(name=name), timeout=timeout)

    def assert_user_list_not_visible(self, name, timeout=DEFAULT_TIMEOUT):
        assert self.became_visible(locator=self.locators.get_user_list_name(name=name), timeout=timeout)

    def assert_access_granted_visible(self, timeout=DEFAULT_TIMEOUT):
        assert self.became_visible(locator=self.locators.ACCESS_GRANTED, timeout=timeout)

    def share_audience(self, timeout=DEFAULT_TIMEOUT):
        self.click(locator=self.locators.CHECKBOX_ALL, timeout=timeout)
        self.click(locator=self.locators.SHARE_BUTTON, timeout=DEFAULT_TIMEOUT)
        self.click(locator=self.locators.PUBLIC_KEY_OPTION, timeout=DEFAULT_TIMEOUT)
        self.click(locator=self.locators.SAVE, timeout=timeout)

    def close_modal_and_unselect_all(self, timeout=DEFAULT_TIMEOUT):
        self.click(locator=self.locators.CLOSE_DIV, timeout=timeout)
        self.click(locator=self.locators.CHECKBOX_ALL, timeout=timeout)
