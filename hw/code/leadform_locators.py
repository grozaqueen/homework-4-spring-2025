from selenium.webdriver.common.by import By

from base_locators import BasePageLocators


class LeadFormPageLocators(BasePageLocators):

    def select_by_placeholder(self, placeholder):
        return By.XPATH, f'//input[@placeholder="{placeholder}"]'

    def select_button_by_text(self, text):
        return By.XPATH, f'//button[.//span[text()="{text}"]]'


    CREATE_LEAD_FORM_BUTTON = (By.XPATH, '//button[.//span[text()="Создать лид-форму"]]')

    MODAL_TITLE_NEW_LEAD_FORM = (By.XPATH, '//h2[text()="Новая лид-форма"]')
    UPLOAD_LOGO_BUTTON = (By.XPATH, '//*[@data-testid="set-global-image"]')
    MODAL_CONTINUE_BUTTON = (By.XPATH, '//div[contains(@class, "ModalSidebarPage_footer")]//button[@data-testid="submit" and .//span[text()="Продолжить"]]')
    MODAL_CANCEL_BUTTON = (By.XPATH, '//div[contains(@class, "ModalSidebarPage_footer")]//button[@data-testid="cancel" and .//span[text()="Отмена"]]')
    COVER_IMAGE_FILE_INPUT = (By.XPATH, '//label[contains(@class, "LocalFileSelector_file")]//input[@type="file"]')
    COVER_IMAGE_MEDIATEKA_BUTTON = (By.XPATH, '//button[.//span[text()="Выбрать из медиатеки"]]')

    MODAL_MEDIATEKA_TITLE = (By.XPATH, '//h2[contains(@class, "MediaLibraryModal_header__") and text()="Медиатека"]')
    LOGO_FILE_INPUT_IN_MODAL = (
        By.XPATH,
        '//div[contains(@class, "MediaLibraryModal_container__") or contains(@class, "MediaLibrary_container__")]'
        '//input[@type="file" and @class="vkuiVisuallyHidden"]'
    )
    MODAL_MEDIATEKA_SELECT_FILE_BUTTON_VISIBLE = (
        By.XPATH,
        '//div[contains(@class, "MediaLibraryModal_container__") or contains(@class, "MediaLibrary_container__")]'
        '//label[contains(@class, "LocalFileSelector_file__")]//span[text()="Выберите файл"]'
    )
    MODAL_MEDIATEKA_FIRST_IMAGE = (
        By.XPATH,
        '(//div[contains(@class, "MediaLibrary_container__")]//div[contains(@class, "ImageItem_imageItem__")])[1]'
    )

    MODAL_MEDIATEKA_IMAGE = (
        By.XPATH,
        '//div[starts-with(@class, "ImageItem_image__")]'
    )

    MODAL_IMAGE_EDITOR_TITLE = (By.XPATH, '//h2[contains(@class, "modal_title__") and text()="Обрезать логотип"]')

    MODAL_IMAGE_EDITOR_SAVE_BUTTON = (
        By.XPATH,
        '//div[contains(@class, "ImageCropper_footer__")]//button[.//span[text()="Сохранить"]]'
    )

    LOADED_LEAD_FORM_LOGO_PREVIEW = (By.XPATH, '//div[contains(@class, "vkuiImageBase--loaded") and .//img and ancestor::div[contains(@class, "Preview_logoWrapper")]]//img')

    QUESTION_TEXT_INPUT = (
        By.XPATH,
        '//textarea[@placeholder="Напишите вопрос"]'
    )

    ANSWER_TEXT_INPUT_1 = (
        By.XPATH,
        '(//input[@placeholder="Введите ответ"])[1]'
    )

    ANSWER_TEXT_INPUT_2 = (
        By.XPATH,
        '(//input[@placeholder="Введите ответ"])[2]'
    )

    ADD_CONTACT_DATA_BUTTON = (
        By.XPATH,
        '//button[.//span[text()="Добавить контактные данные"]]'
    )

    EMAIL_CHECKBOX_LABEL = (
        By.XPATH,
        '//label[contains(@class, "vkuiCheckbox") and .//span[text()="Электронная почта"]]'
    )

    CITY_CHECKBOX_LABEL = (
        By.XPATH,
        '//label[contains(@class, "vkuiCheckbox") and .//span[text()="Город"]]'
    )

    ADD_BUTTON_IN_MODAL = (
        By.XPATH,
        '//div[contains(@class, "ModalManagerPage_footer")]//button[.//span[@class="vkuiButton__content" and text()="Добавить"]]'
    )