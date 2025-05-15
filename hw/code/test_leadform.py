import pytest
from base_case import BaseCase
from leadform_page import LeadFormPage

class TestLeadForms(BaseCase):
    _valid_internal_lead_form_name = "Test Lead Form Automation"
    _valid_logo_filename = "test_logo.png"
    _valid_company_name = "Selenium QA Solutions"
    _valid_form_title = "Эксклюзивное предложение для QA!"
    _valid_form_description = "Получите доступ к лучшим инструментам"

    _another_internal_name = "Другая Тестовая Форма"
    _another_logo = "another_logo.jpg"


    def test_upload_image(self, leadform_page):
        leadform_page.click_create_lead_form_button()

        leadform_page.enter_lead_form_internal_name(self._valid_internal_lead_form_name)

        leadform_page.upload_logo(filename=self._valid_logo_filename)
        print("Лого успешно загружено")

    def test_create_decoration(self, leadform_page):

        leadform_page.click_create_lead_form_button()

        leadform_page.enter_lead_form_internal_name(self._valid_internal_lead_form_name)


        leadform_page.upload_logo(filename=self._valid_logo_filename)

        leadform_page.enter_company_name(self._valid_company_name)
        leadform_page.enter_form_title(self._valid_form_title)
        leadform_page.enter_form_description(self._valid_form_description)


        print(
            f"Test 'test_create_lead_form_step1_design' for form '{self._valid_internal_lead_form_name}' completed up to design step.")

    def test_proceed_to_questions_page(self, leadform_page: LeadFormPage):
        leadform_page.click_create_lead_form_button()

        leadform_page.enter_lead_form_internal_name(self._valid_internal_lead_form_name)


        leadform_page.upload_logo(filename=self._valid_logo_filename)

        leadform_page.enter_company_name(self._valid_company_name)
        leadform_page.enter_form_title(self._valid_form_title)
        leadform_page.enter_form_description(self._valid_form_description)

        leadform_page.click_next_button()


        print(
            f"Test 'test_create_lead_form_step1_design' for form '{self._valid_internal_lead_form_name}' completed up to design step.")

    def test_add_question(self, leadform_page: LeadFormPage):
        leadform_page.click_create_lead_form_button()

        leadform_page.enter_lead_form_internal_name(self._valid_internal_lead_form_name)

        leadform_page.upload_logo(filename=self._valid_logo_filename)

        leadform_page.enter_company_name(self._valid_company_name)
        leadform_page.enter_form_title(self._valid_form_title)
        leadform_page.enter_form_description(self._valid_form_description)

        leadform_page.click_next_button()
        leadform_page.click_add_question_button()

        leadform_page.enter_question_text("Question")
        leadform_page.enter_answer_text("Answer1", 1)
        leadform_page.enter_answer_text("Answer2", 2)

        print(
            f"Test 'test_create_lead_form_step1_design' for form '{self._valid_internal_lead_form_name}' completed up to design step.")