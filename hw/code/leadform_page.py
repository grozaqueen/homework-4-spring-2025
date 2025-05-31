import os

from base_page import BasePage, DEFAULT_TIMEOUT
from leadform_locators import LeadFormPageLocators


class LeadFormPage(BasePage):
    url = 'https://ads.vk.com/hq/leadads'
    locators = LeadFormPageLocators()

    def click_create_lead_form_button(self, timeout=DEFAULT_TIMEOUT):
        self.click(self.locators.CREATE_LEAD_FORM_BUTTON, timeout=timeout)

    def enter_lead_form_internal_name(self, name, timeout=DEFAULT_TIMEOUT):
        elem = self.send_keys_to_input(self.locators.LEAD_FORM_INTERNAL_NAME_INPUT, name, timeout=timeout)
        return elem.get_attribute("value")

    def upload_logo(self, filename="logo.png", timeout_short=10):

        filepath = self._get_static_filepath(filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Logo file not found at: {filepath}")

        self.click(self.locators.UPLOAD_LOGO_BUTTON, timeout=timeout_short)

        file_input_mediateka = self.find(self.locators.LOGO_FILE_INPUT_IN_MODAL, timeout=timeout_short)
        file_input_mediateka.send_keys(filepath)

        try:
            confirm_button = self.find(self.locators.MODAL_MEDIATEKA_IMAGE, timeout=timeout_short)
            confirm_button.click()
        except Exception as e:
            raise Exception(f"Mediateka confirmation button not found or not clickable, proceeding. Error: {e}")

        try:
            save_button_editor = self.find(self.locators.MODAL_IMAGE_EDITOR_SAVE_BUTTON, timeout=timeout_short)
            save_button_editor.click()

        except Exception as e:
            raise Exception(f"Error during Image Editor step (modal appearance or save). Error: {e}")


    def enter_company_name(self, name, timeout=DEFAULT_TIMEOUT):
        elem = self.send_keys_to_input(self.locators.COMPANY_NAME_INPUT, name, timeout=timeout)
        return elem.get_attribute("value")

    def enter_form_title(self, title, timeout=DEFAULT_TIMEOUT):
        elem = self.send_keys_to_input(self.locators.FORM_TITLE_INPUT, title, timeout=timeout)
        return elem.get_attribute("value")

    def enter_form_description(self, description, timeout=DEFAULT_TIMEOUT):
        elem = self.send_keys_to_input(self.locators.FORM_DESCRIPTION_INPUT, description, timeout=timeout)
        return elem.get_attribute("value")

    def click_modal_continue_button(self, timeout=DEFAULT_TIMEOUT):
        elem = self.click(self.locators.MODAL_CONTINUE_BUTTON, timeout=timeout)
        return elem.get_attribute("value")

    def click_next_button(self, timeout=DEFAULT_TIMEOUT):
        self.click(self.locators.NEXT_BUTTON, timeout=timeout)

    def click_add_question_button(self, timeout=DEFAULT_TIMEOUT):
        self.click(self.locators.ADD_QUESTION_BUTTON, timeout=timeout)

    def enter_question_text(self, question, timeout=DEFAULT_TIMEOUT):
        elem = self.send_keys_to_input(self.locators.QUESTION_TEXT_INPUT, question, timeout=timeout)
        return elem.get_attribute("value")

    def enter_answer_text(self, answer_text, answer_number, timeout=DEFAULT_TIMEOUT):
        if answer_number == 1:
            locator = self.locators.ANSWER_TEXT_INPUT_1
        elif answer_number == 2:
            locator = self.locators.ANSWER_TEXT_INPUT_2
        else:
            raise ValueError("Wrong number")

        elem = self.send_keys_to_input(locator, answer_text, timeout=timeout)

        return elem.get_attribute("value")

    def click_add_contact_data(self, timeout=DEFAULT_TIMEOUT):
        self.click(self.locators.ADD_CONTACT_DATA_BUTTON, timeout=timeout)

    def click_email_checkbox(self, timeout=DEFAULT_TIMEOUT):
        self.click(self.locators.EMAIL_CHECKBOX_LABEL, timeout=timeout)

    def click_city_checkbox(self, timeout=DEFAULT_TIMEOUT):
        self.click(self.locators.CITY_CHECKBOX_LABEL, timeout=timeout)

    def click_add_button(self, timeout=DEFAULT_TIMEOUT):
        self.click(self.locators.ADD_BUTTON_IN_MODAL, timeout=timeout)