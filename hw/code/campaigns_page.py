from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base_page import BasePage, DEFAULT_TIMEOUT
from campaigns_locators import CampaignPageLocators
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from os import path
from datetime import date
import logging

logger = logging.getLogger(__name__)


class TargetActions():
    SITE = 'site'
    GROUP = 'group'


class CampaignsPage(BasePage):
    url = 'https://ads.vk.com/hq/dashboard'
    locators = CampaignPageLocators()
    target_actions = TargetActions()

    def ensure_on_page(self, timeout=DEFAULT_TIMEOUT):
        if not self.url:
            logger.warning(f"{self.__class__.__name__} has no URL defined. Cannot ensure on page.")
            return

        try:
            WebDriverWait(self.driver, 1).until(
                lambda d: d.current_url is not None and d.current_url.rstrip('/') == self.url.rstrip('/')
            )
            logger.debug(f"Already on {self.url}")
        except TimeoutException:
            logger.info(f"Not on {self.url} (current: {self.driver.current_url}). Navigating...")
            self.driver.get(self.url)
            WebDriverWait(self.driver, timeout).until(
                EC.url_to_be(self.url)
            )
            logger.info(f"Navigated to {self.url}")

    def click_learning_modal_dismiss(self, timeout=1):
        try:
            if self.is_element_clickable(self.locators.DISMISS_BUTTON, timeout=timeout):
                self.click(self.locators.DISMISS_BUTTON, timeout=timeout)
        except TimeoutException:
            logger.info("Модальное окно обучения не появилось или не кликабельно в течение заданного времени.")

    def click_create_campaign_button(self, timeout=DEFAULT_TIMEOUT):
        self.click(self.locators.CREATE_CAMPAIGN_BUTTON, timeout=timeout)

    def enter_campaign_name(self, name, prev_name='Кампания', timeout=DEFAULT_TIMEOUT):
        header_locator = self.locators.get_editable_campaign_header(name=prev_name)
        self.click(locator=header_locator, timeout=timeout)
        element = self.find(header_locator, timeout)
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(
            Keys.DELETE).perform()
        ActionChains(self.driver).send_keys(name).send_keys(Keys.ENTER).perform()

    def enter_group_name(self, name, timeout=DEFAULT_TIMEOUT):
        self.click(locator=self.locators.EDITABLE_GROUP_HEADER, timeout=timeout)
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(
            Keys.DELETE).perform()
        ActionChains(self.driver).send_keys(name).send_keys(Keys.ENTER).perform()

    def enter_ad_name(self, name, prev_name='Объявление', timeout=DEFAULT_TIMEOUT):
        header_locator = self.locators.get_editable_ad_header(name=prev_name)
        self.click(locator=header_locator, timeout=timeout)
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(
            Keys.DELETE).perform()
        ActionChains(self.driver).send_keys(name).send_keys(Keys.ENTER).perform()

    def click_target_action(self, action, timeout=DEFAULT_TIMEOUT):
        locator = None
        if action == self.target_actions.SITE:
            locator = self.locators.SITE_OPTION
        elif action == self.target_actions.GROUP:
            locator = self.locators.GROUP_OPTION
        else:
            raise ValueError("Incorrect target action")
        self.click(locator=locator, timeout=timeout)

    def select_target_group(self, group_tag, timeout=DEFAULT_TIMEOUT):
        self.click(locator=self.locators.GROUP_SELECTOR, timeout=timeout)
        self.click(locator=self.locators.ENTER_OTHER_GROUP, timeout=timeout)
        ActionChains(self.driver).send_keys(group_tag).send_keys(Keys.ENTER).perform()
        self.click(locator=self.locators.ADD_GROUP_BUTTON, timeout=timeout)

    def enter_site_url(self, url, timeout=DEFAULT_TIMEOUT):
        self.send_keys_to_input(locator=self.locators.ADVERTISED_SITE_FIELD, keys=url, timeout=timeout)

    def enter_budget(self, budget_value, timeout=DEFAULT_TIMEOUT):
        budget_field = self.find(self.locators.BUDGET, timeout=timeout)
        budget_field.click()
        self.driver.execute_script("arguments[0].value='';", budget_field)
        budget_field.send_keys(str(budget_value))
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: str(budget_value) in budget_field.get_attribute("value").replace(' ', '').replace('₽',
                                                                                                                 '')
            )
        except TimeoutException:
            logger.warning(
                f"Budget value {budget_value} might not have been set correctly. Current value: {budget_field.get_attribute('value')}")

    def enter_start_date(self, date_str: str, timeout=DEFAULT_TIMEOUT):
        self.click(self.locators.START_DATE, timeout=timeout)
        ActionChains(self.driver).send_keys(date_str).send_keys(Keys.ENTER).perform()

    def enter_end_date(self, date_str: str, timeout=DEFAULT_TIMEOUT):
        self.click(self.locators.END_DATE, timeout=timeout)
        ActionChains(self.driver).send_keys(date_str).send_keys(Keys.ENTER).perform()

    def click_continue(self, timeout=DEFAULT_TIMEOUT):
        self.click(self.locators.CONTINUE, timeout=timeout)

    def click_region(self, timeout=DEFAULT_TIMEOUT):
        self.click(locator=self.locators.REGION, timeout=timeout)

    def wait_until_ad_logo_loaded(self, timeout=50):
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.locators.AD_LOGO_PREVIEW)
        )

    def click_close_button(self, timeout=DEFAULT_TIMEOUT):
        self.click(locator=self.locators.CLOSE_BUTTON, timeout=timeout)

    def enter_ad_header(self, header, timeout=DEFAULT_TIMEOUT):
        self.click(locator=self.locators.AD_HEADER, timeout=timeout)
        ad_header_element = self.find(self.locators.AD_HEADER, timeout=timeout)
        ad_header_element.clear()
        ad_header_element.send_keys(header)

    def enter_short_description(self, description, timeout=DEFAULT_TIMEOUT):
        self.click(locator=self.locators.AD_SHORT_DESCRIPTION, timeout=timeout)
        ad_desc_element = self.find(self.locators.AD_SHORT_DESCRIPTION, timeout=timeout)
        ad_desc_element.clear()
        ad_desc_element.send_keys(description)

    def load_media(self, file1='img.png', file2='img_1.png', timeout=DEFAULT_TIMEOUT):
        filepath = self._get_static_filepath(filename=file1)
        filepath2 = self._get_static_filepath(filename=file2)
        file_input = self.find(locator=self.locators.ADD_MEDIA_FILE_INPUT, timeout=timeout)
        file_input.send_keys(f"{filepath}\n{filepath2}")
        WebDriverWait(self.driver, 50).until(
            EC.invisibility_of_element_located(self.locators.MEDIA_PLACEHOLDER)
        )

    def close_err(self, timeout=DEFAULT_TIMEOUT):
        try:
            self.wait_until_clickable(self.locators.CLOSE_ERR_BUTTON, timeout=timeout)
            self.click(locator=self.locators.CLOSE_ERR_BUTTON, timeout=timeout)
        except (TimeoutException, NoSuchElementException) as e:
            logger.info(f"Error closing error message: {e}. It might not have been present.")

    def click_publish(self, timeout=DEFAULT_TIMEOUT):
        self.click(locator=self.locators.PUBLISH_BUTTON, timeout=timeout)

    def get_campaign_name_element(self, name, timeout=DEFAULT_TIMEOUT):
        campaign_name_locator = self.locators.get_campaign_name_locator(name=name)
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(campaign_name_locator)
        )
        return self.find(locator=campaign_name_locator, timeout=timeout)

    def is_campaign_visible(self, name, timeout=DEFAULT_TIMEOUT):
        try:
            element = self.get_campaign_name_element(name, timeout)
            return element.is_displayed() and element.text == name
        except TimeoutException:
            return False

    def hover_actions_icon(self, campaign_name: str, timeout=DEFAULT_TIMEOUT):
        campaign_row_locator = self.locators.get_campaign_name_locator(name=campaign_name)
        self.hover(campaign_row_locator)
        self.hover(self.locators.ACTIONS_ICON)

    def enter_description(self, description, timeout=DEFAULT_TIMEOUT):
        self.click(locator=self.locators.DESCRIPTION, timeout=timeout)
        desc_element = self.find(self.locators.DESCRIPTION, timeout)
        desc_element.clear()
        desc_element.send_keys(description)

    def click_confirm(self, timeout=5):
        try:
            if self.is_element_clickable(locator=self.locators.CONFIRM_CAMPAIGN, timeout=timeout):
                self.click(locator=self.locators.CONFIRM_CAMPAIGN, timeout=timeout)
        except TimeoutException:
            logger.warning("Кнопка 'Отправить' (CONFIRM_CAMPAIGN) не была кликабельна.")

    def click_shot_in_video(self, timeout=DEFAULT_TIMEOUT):
        self.click(locator=self.locators.SHOT_IN_VIDEO, timeout=timeout)

    def delete_campaign(self, name, timeout=DEFAULT_TIMEOUT):
        logger.info(f"Попытка удалить кампанию: {name}")
        self.ensure_on_page()

        if not self.is_campaign_visible(name, timeout=5):
            logger.warning(f"Кампания '{name}' не найдена перед попыткой удаления.")
            return

        campaign_name_element_in_list = self.locators.get_campaign_name_locator(name=name)
        self.click(locator=campaign_name_element_in_list, timeout=timeout)
        self.hover_actions_icon(campaign_name=name, timeout=timeout)
        self.click(self.locators.DELETE_BUTTON, timeout=timeout)
        self.click_confirm()
        self.ensure_on_page()
        if self.is_campaign_visible(name, timeout=5):
            logger.error(f"Кампания '{name}' все еще видна после попытки удаления.")
        else:
            logger.info(f"Кампания '{name}' успешно удалена (или невидима).")

    def go_to_create_campaign(self):
        self.ensure_on_page()
        self.click_learning_modal_dismiss()
        self.click_create_campaign_button()

    def assert_campaign_visible(self, name, timeout=DEFAULT_TIMEOUT):
        self.ensure_on_page()
        assert self.is_campaign_visible(name, timeout), f"Кампания '{name}' не видима."

    def assert_campaign_not_visible(self, name, timeout=DEFAULT_TIMEOUT):
        self.ensure_on_page()
        assert not self.is_campaign_visible(name, timeout), f"Кампания '{name}' все еще видима, хотя не должна."

    def enter_dates(self, start_date_str=None, end_date_str=None):
        start_date_str = start_date_str or date.today().strftime('%d.%m.%Y')
        end_date_str = end_date_str or date.today().strftime('%d.%m.%Y')
        self.enter_start_date(start_date_str)
        self.enter_end_date(end_date_str)

    def create_campaign_site(self, name, group_name, ad_name, url, budget, header, description):
        self.go_to_create_campaign()
        self.enter_campaign_name(name=name)
        self.click_target_action(self.target_actions.SITE)
        self.enter_site_url(url=url)
        self.enter_budget(budget)
        self.enter_dates()
        self.click_continue()
        self.enter_group_name(name=group_name)
        self.click_region()
        self.click_continue()
        self.load_media()

        self.enter_ad_header(header=header)
        self.enter_short_description(description=description)
        self.enter_ad_name(name=ad_name)
        self.wait_until_ad_logo_loaded()
        self.click_publish()

        try:
            self.close_err(timeout=3)
            self.click_publish()
        except Exception as e:
            logger.warning(f"Не удалось опубликовать кампанию '{name}' после закрытия ошибки: {e}")

    def create_campaign_group(self, name, group_name, ad_name, group_tag, description):
        self.go_to_create_campaign()
        self.enter_campaign_name(name=name)
        self.click_target_action(self.target_actions.GROUP)
        self.select_target_group(group_tag)
        self.enter_dates()
        self.click_continue()
        self.enter_group_name(name=group_name)
        self.click_region()
        self.click_continue()
        self.enter_description(description=description)
        self.click_shot_in_video()
        self.load_media()
        self.wait_until_ad_logo_loaded()
        self.enter_ad_name(name=ad_name)

        self.click_publish()
        try:
            self.close_err(timeout=3)
            self.click_publish()
        except Exception as e:
            logger.warning(f"Не удалось опубликовать кампанию (группа) '{name}' после закрытия ошибки: {e}")

    def search_for_campaign(self, name, timeout=DEFAULT_TIMEOUT):
        self.ensure_on_page()
        self.send_keys_to_input(locator=self.locators.SEARCH_INPUT, keys=name, timeout=timeout)
        self.find(self.locators.SEARCH_INPUT).send_keys(Keys.ENTER)

    def clear_search(self, timeout=DEFAULT_TIMEOUT):
        self.ensure_on_page()
        self.click(self.locators.FILTER_BUTTON, timeout=timeout)
        self.click(self.locators.FILTERS_RESET_BUTTON, timeout=timeout)
        self.click(self.locators.FILTERS_APPLY_BUTTON, timeout=timeout)

    def create_folder(self, name, timeout=DEFAULT_TIMEOUT):
        self.ensure_on_page()
        self.click(locator=self.locators.TAGS_SELECTOR, timeout=timeout)
        self.click(locator=self.locators.CREATE_TAG, timeout=timeout)
        folder_name_field = self.find(self.locators.FOLDER_NAME_INPUT)
        folder_name_field.clear()
        folder_name_field.send_keys(name + Keys.ENTER)

    def assert_folder_visible(self, name, timeout=DEFAULT_TIMEOUT):
        self.ensure_on_page()
        self.click(locator=self.locators.TAGS_SELECTOR, timeout=timeout)
        loc = self.locators.get_folder_name_locator(name=name)
        assert self.is_element_visible(locator=loc, timeout=timeout), f"Папка '{name}' не видима."
        self.click(locator=self.locators.TAGS_SELECTOR, timeout=timeout)

    def assert_folder_not_visible(self, name, timeout=DEFAULT_TIMEOUT):
        self.ensure_on_page()
        self.click(locator=self.locators.TAGS_SELECTOR, timeout=timeout)
        loc = self.locators.get_folder_name_locator(name=name)
        assert not self.is_element_visible(locator=loc, timeout=timeout), f"Папка '{name}' видима, хотя не должна."
        self.click(locator=self.locators.TAGS_SELECTOR, timeout=timeout)

    def click_edit_folder(self, name, timeout=DEFAULT_TIMEOUT):
        self.ensure_on_page()
        self.click(locator=self.locators.TAGS_SELECTOR, timeout=timeout)
        name_loc = self.locators.get_folder_name_locator(name=name)
        self.hover(name_loc, timeout=timeout)
        edit_loc = self.locators.get_folder_edit_icon_locator(name=name)
        self.click(edit_loc, timeout=timeout)

    def delete_folder(self, name, timeout=DEFAULT_TIMEOUT):
        self.ensure_on_page()
        self.click_edit_folder(name=name, timeout=timeout)
        self.click(self.locators.DELETE_FOLDER_BUTTON, timeout=timeout)
        self.click(self.locators.CONFIRM_DELETE_FOLDER_BUTTON, timeout=timeout)
        self.assert_folder_not_visible(name=name, timeout=timeout)

    def add_campaign_to_folder(self, folder_name, campaign_name, timeout=DEFAULT_TIMEOUT):
        self.ensure_on_page()
        self.click_edit_folder(name=folder_name, timeout=timeout)
        self.click(locator=self.locators.ADD_CAMPAIGNS_TO_FOLDER, timeout=timeout)
        checkbox_locator = self.locators.get_select_campaign_element(name=campaign_name)
        self.click(locator=checkbox_locator, timeout=timeout)
        self.click(locator=self.locators.SAVE, timeout=timeout)

    def select_folder(self, name, timeout=DEFAULT_TIMEOUT):
        self.ensure_on_page()
        self.click(locator=self.locators.TAGS_SELECTOR, timeout=timeout)
        name_loc = self.locators.get_folder_name_locator(name=name)
        self.click(name_loc, timeout=timeout)

    def assert_folder_selected(self, name, timeout=DEFAULT_TIMEOUT):
        self.ensure_on_page()
        select_element = self.find(locator=self.locators.TAGS_SELECTOR, timeout=timeout)
        assert select_element.text == name, f"Папка '{name}' не выбрана. Текущий текст селектора: '{select_element.text}'"

    def edit_campaign(self, original_name: str, new_name: str, budget: str, timeout=DEFAULT_TIMEOUT):
        logger.info(f"Редактирование кампании '{original_name}' в '{new_name}' с бюджетом {budget}")
        self.ensure_on_page()
        campaign_name_locator = self.locators.get_campaign_name_locator(name=original_name)
        try:
            self.click(locator=campaign_name_locator, timeout=timeout)
        except TimeoutException:
            logger.error(f"Не удалось найти или кликнуть кампанию '{original_name}' для редактирования.")
            raise
        try:
            self.wait_until_clickable(self.locators.EDIT_BUTTON, timeout)
            self.click(locator=self.locators.EDIT_BUTTON, timeout=timeout)
        except TimeoutException:
            logger.error(
                f"Кнопка 'Редактировать' не найдена или не кликабельна на странице кампании '{original_name}'.")
            raise
        self.enter_budget(budget_value=budget, timeout=timeout)
        self.enter_campaign_name(name=new_name, prev_name=original_name, timeout=timeout)
        self.click(locator=self.locators.SAVE, timeout=timeout)
        logger.info(f"Кампания '{original_name}' должна быть переименована в '{new_name}'.")
        self.ensure_on_page()
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.locators.get_campaign_name_locator(new_name))
        )

    def edit_ad(self, original_ad_name: str, new_name: str, header: str, description: str, timeout=DEFAULT_TIMEOUT):
        logger.info(f"Редактирование объявления '{original_ad_name}' в '{new_name}'")

        self.click(locator=self.locators.ADS_MENU_ITEM, timeout=timeout)

        logger.warning(
            "Логика выбора КОНКРЕТНОГО объявления для редактирования не реализована полностью. Используется общий EDIT_BUTTON.")
        ad_name_link_locator = self.locators.get_ad_name_locator(original_ad_name)
        try:
            self.click(ad_name_link_locator, timeout=timeout)
            self.wait_until_clickable(self.locators.EDIT_BUTTON, timeout)
            self.click(locator=self.locators.EDIT_BUTTON, timeout=timeout)
        except TimeoutException:
            logger.error(f"Не удалось найти/кликнуть объявление '{original_ad_name}' или его кнопку редактирования.")
            raise
        self.enter_ad_name(name=new_name, prev_name=original_ad_name)
        self.enter_ad_header(header=header)
        self.enter_short_description(description=description)
        self.click(locator=self.locators.SAVE, timeout=timeout)
        assert self.became_invisible(locator=self.locators.EDIT_HEADER,
                                     timeout=timeout), "Форма редактирования не закрылась после сохранения."
        logger.info(f"Объявление '{original_ad_name}' должно быть переименовано в '{new_name}'.")

    def assert_ad_visible(self, name, timeout=DEFAULT_TIMEOUT):
        self.click(locator=self.locators.ADS_MENU_ITEM, timeout=timeout)
        ad_locator = self.locators.get_ad_name_locator(name=name)
        assert self.is_element_visible(locator=ad_locator, timeout=timeout), f"Объявление '{name}' не видимо."

    def assert_ad_not_visible(self, name, timeout=DEFAULT_TIMEOUT):
        self.click(locator=self.locators.ADS_MENU_ITEM, timeout=timeout)
        ad_locator = self.locators.get_ad_name_locator(name=name)
        assert not self.is_element_visible(locator=ad_locator, timeout=timeout), f"Объявление '{name}' все еще видимо."

    def load_logo(self, filename='img.png', timeout=DEFAULT_TIMEOUT):
        filepath = self._get_static_filepath(filename=filename)

        logger.info(f"Attempting to upload logo from: {filepath}")
        if not path.exists(filepath):
            logger.error(f"ERROR: Logo file does not exist at path: {filepath}")
            raise FileNotFoundError(f"Logo file not found at: {filepath}")

        logger.info("Clicking 'Select Logo' button...")
        self.click(self.locators.SELECT_LOGO_BUTTON, timeout=timeout)

        logger.info(f"Sending filepath '{filepath}' to logo file input...")
        logo_input_element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.locators.LOGO_FILE_INPUT_IN_MODAL)
        )
        logo_input_element.send_keys(filepath)

        logger.info("Waiting for logo preview (in uploader) to appear...")
        WebDriverWait(self.driver, 50).until(
            EC.visibility_of_element_located(self.locators.LOADED_LOGO_PREVIEW)
        )
        logger.info("Logo preview in uploader is visible.")

        logger.info("Clicking 'Add' button to confirm logo selection from modal...")
        self.click(self.locators.ADD_BUTTON, timeout=timeout)
        logger.info("Logo added from modal.")

    def _get_static_filepath(self, filename: str) -> str:
        if filename == 'img.png' or filename == 'img_1.png':
            p = path.abspath(filename)
            if not path.exists(p):
                with open(p, 'w') as f: f.write("dummy content")
            return p
        raise FileNotFoundError(f"Static file {filename} mapping not found in dummy _get_static_filepath")