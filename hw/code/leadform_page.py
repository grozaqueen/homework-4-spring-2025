import os

from base_page import BasePage, DEFAULT_TIMEOUT
from leadform_locators import LeadFormPageLocators


class LeadFormPage(BasePage):
    url = 'https://ads.vk.com/hq/leadads'
    locators = LeadFormPageLocators()

    def click_create_lead_form_button(self, timeout=DEFAULT_TIMEOUT):
        self.click(self.locators.CREATE_LEAD_FORM_BUTTON, timeout=timeout)
        print("Clicked 'Create Lead Form' button and modal appeared.")

    def enter_lead_form_internal_name(self, name, timeout=DEFAULT_TIMEOUT):
        self.send_keys_to_input(self.locators.LEAD_FORM_INTERNAL_NAME_INPUT, name, timeout=timeout)
        print(f"Entered internal lead form name: {name}")

    def upload_logo(self, filename="logo.png", timeout_short=10):

        filepath = self._get_static_filepath(filename)
        if not os.path.exists(filepath):
            print(f"ERROR: Logo file does not exist at path: {filepath}")
            raise FileNotFoundError(f"Logo file not found at: {filepath}")

        print("Clicking 'Upload Logo' button on the main form...")
        self.click(self.locators.UPLOAD_LOGO_BUTTON, timeout=timeout_short)

        print("Waiting for Mediateka modal to appear...")
        print("Mediateka modal is visible.")

        print(f"Sending filepath '{filepath}' to Mediateka file input...")
        file_input_mediateka = self.find(self.locators.LOGO_FILE_INPUT_IN_MODAL, timeout=timeout_short)
        file_input_mediateka.send_keys(filepath)
        print("Filepath sent to Mediateka input.")

        try:
            print("Attempting to click Mediateka confirmation button (e.g., 'Добавить')...")
            confirm_button = self.find(self.locators.MODAL_MEDIATEKA_IMAGE, timeout=timeout_short)
            confirm_button.click()

            print("Clicked Mediateka confirmation button.")
        except Exception as e:
            print(f"Mediateka confirmation button not found or not clickable, proceeding. Error: {e}")

        print("Waiting for Image Editor modal to appear (by title)...")
        try:
            print("Image Editor modal is visible (by title).")

            print("Waiting for 'Save' button in Image Editor modal to be clickable...")
            save_button_editor = self.find(self.locators.MODAL_IMAGE_EDITOR_SAVE_BUTTON, timeout=timeout_short)

            print("'Save' button in Image Editor is now clickable.")
            save_button_editor.click()
            print("Clicked 'Save' in Image Editor.")

        except Exception as e:
            print(f"Error during Image Editor step (modal appearance or save). Error: {e}")

        print("Waiting for logo preview to appear on the main lead form...")
        print("Logo preview is visible on the main lead form.")

    def enter_company_name(self, name, timeout=DEFAULT_TIMEOUT):
        self.send_keys_to_input(self.locators.COMPANY_NAME_INPUT, name, timeout=timeout)
        print(f"Entered company name: {name}")

    def enter_form_title(self, title, timeout=DEFAULT_TIMEOUT):
        self.send_keys_to_input(self.locators.FORM_TITLE_INPUT, title, timeout=timeout)
        print(f"Entered form title: {title}")

    def enter_form_description(self, description, timeout=DEFAULT_TIMEOUT):
        self.send_keys_to_input(self.locators.FORM_DESCRIPTION_INPUT, description, timeout=timeout)
        print(f"Entered form description: {description}")

    def click_modal_continue_button(self, timeout=DEFAULT_TIMEOUT):
        self.click(self.locators.MODAL_CONTINUE_BUTTON, timeout=timeout)
        print("Clicked modal 'Continue' button.")

    def click_next_button(self, timeout=DEFAULT_TIMEOUT):
        self.click(self.locators.NEXT_BUTTON, timeout=timeout)
        print("Clicked NEXT 'NEXT' button.")

    def click_add_question_button(self, timeout=DEFAULT_TIMEOUT):
        self.click(self.locators.ADD_QUESTION_BUTTON, timeout=timeout)
        print("Clicked add question button.")

    def enter_question_text(self, question, timeout=DEFAULT_TIMEOUT):
        self.send_keys_to_input(self.locators.QUESTION_TEXT_INPUT, question, timeout=timeout)
        print(f"Entered question text: {question}")

    def enter_answer_text(self, answer_text, answer_number, timeout=DEFAULT_TIMEOUT):
        if answer_number == 1:
            locator = self.locators.ANSWER_TEXT_INPUT_1
        elif answer_number == 2:
            locator = self.locators.ANSWER_TEXT_INPUT_2
        else:
            raise ValueError("Wrong number")

        self.send_keys_to_input(locator, answer_text, timeout=timeout)
        print(f"Entered answer text for answer #{answer_number}: {answer_text}")