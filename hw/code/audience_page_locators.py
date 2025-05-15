from selenium.webdriver.common.by import By
from base_locators import BasePageLocators

class AudiencePageLocators(BasePageLocators):
    CREATE_AUDIENCE_BUTTON = (By.XPATH, '//*[@data-testid="create-audience"]')
    ADD_SOURCE = (By.XPATH, '//span[text()="Добавить источник"]')
    NAME_INPUT = (By.XPATH, '//input[@type="text"]')
    SAVE = (By.XPATH, '//span[text()="Сохранить"]')
    USER_LIST_OPTION = (By.XPATH, '//span[text()="Список пользователей"]')
    LOAD_NEW_OPTION = (By.XPATH, '//span[text()="Загрузить новый"]')
    LIST_NAME_INPUT = (By.XPATH, '//input[@placeholder="Введите название списка"]')
    LIST_TYPE_SELECT = (By.XPATH, '//div[contains(@class, "vkuiCustomSelect")]//input[@role="combobox"]')
    UNIFIED_LIST_OPTION = (By.XPATH, '//div[contains(@class, "vkuiCustomSelect")]//*[text()="Единый список"]')
    FILE_INPUT = (By.XPATH, '//input[@type="file"]')
    SUBMIT_LIST_BUTTON = (By.XPATH, '//div[contains(@class, "ModalSidebarPage_container")]//*[@data-testid="submit"]')
    SUBMIT_BUTTON = (By.XPATH, '//div[contains(@class, "ModalSidebarPage")]//*[@data-testid="submit"]')
    DELETE_BUTTON = (By.XPATH, '//span[text()="Удалить"]')
    USER_LIST_MENU_ITEM = (By.XPATH, '//*[@id="tab_audience.users_list"]')
    AUDIENCES_MENU_ITEM = (By.XPATH, '//*[@id="tab_audience"]')
    ADD_AUDIENCE_HEADER = (By.XPATH, '//h2[contains(text(), "Создание аудитории")]')
    ADD_USER_LIST_HEADER = (By.XPATH, '//h2[contains(text(), "Список пользователей")]')
    CLOSE = (By.XPATH, '//button[@aria-label="Close"]')
    CLOSE_DIV = (By.XPATH, '//div[@aria-label="Закрыть"]')
    SEARCH_INPUT = (By.XPATH, '//*[@data-testid="search-input"]')

    CREATE_USER_LIST_BUTTON = (By.XPATH, '//span[text()="Загрузить список"]')

    CHECKBOX_ALL = (By.XPATH, '//label[*[@id="checkbox-all"]]')
    SHARE_BUTTON = (By.XPATH, '//*[@data-testid="share-button"]')
    PUBLIC_KEY_OPTION = (By.XPATH, '//span[text()="Публичный ключ"]')
    ACCESS_GRANTED = (By.XPATH, '//*[text()="Доступ открыт"]')

    def get_audience_name(self, name):
        return (By.XPATH, f'//h5[text()="{name}"]')

    def get_user_list_name(self, name):
        return (By.XPATH, f'//div[text()="{name}"]')

    def get_edit_icon(self, name):
        return (By.XPATH, f'//*[@data-testid="audience-item-menu"]')
