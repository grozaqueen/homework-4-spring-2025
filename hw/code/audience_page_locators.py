from selenium.webdriver.common.by import By
from base_locators import BasePageLocators

class AudiencePageLocators(BasePageLocators):
    def select_by_span(self, name):
        return (By.XPATH, f'//span[text()="{name}"]')

    USER_LIST_OPTION = select_by_span("Список пользователей")
    LOAD_NEW_OPTION = select_by_span("Загрузить новый")
    SAVE = select_by_span("Сохранить")
    PUBLIC_KEY_OPTION = select_by_span("Публичный ключ")
    CREATE_USER_LIST_BUTTON = select_by_span("Загрузить список")
    DELETE_BUTTON = select_by_span("Удалить")

    def select_by_h2(self, name):
        return (By.XPATH, f'//h2[contains(text(), "{name}")]')

    ADD_AUDIENCE_HEADER = select_by_h2("Создание аудитории")
    ADD_USER_LIST_HEADER = select_by_h2("Список пользователей")

    def get_by_data_testid(self, name):
        return (By.XPATH, f'//*[@data-testid="{name}"]')

    SEARCH_INPUT = get_by_data_testid("search-input")
    CREATE_AUDIENCE_BUTTON = get_by_data_testid("create-audience")
    SHARE_BUTTON = get_by_data_testid("share-button")

    ADD_SOURCE = (By.XPATH, '//span[text()="Добавить источник"]')
    NAME_INPUT = (By.XPATH, '//input[@type="text"]')
    LIST_NAME_INPUT = (By.XPATH, '//input[@placeholder="Введите название списка"]')
    LIST_TYPE_SELECT = (By.XPATH, '//div[contains(@class, "vkuiCustomSelect")]//input[@role="combobox"]')
    UNIFIED_LIST_OPTION = (By.XPATH, '//div[contains(@class, "vkuiCustomSelect")]//*[text()="Единый список"]')
    FILE_INPUT = (By.XPATH, '//input[@type="file"]')
    SUBMIT_LIST_BUTTON = (By.XPATH, '//div[contains(@class, "ModalSidebarPage_container")]//*[@data-testid="submit"]')
    SUBMIT_BUTTON = (By.XPATH, '//div[contains(@class, "ModalSidebarPage")]//*[@data-testid="submit"]')
    USER_LIST_MENU_ITEM = (By.XPATH, '//*[@id="tab_audience.users_list"]')
    AUDIENCES_MENU_ITEM = (By.XPATH, '//*[@id="tab_audience"]')
    CLOSE = (By.XPATH, '//button[@aria-label="Close"]')
    CLOSE_DIV = (By.XPATH, '//div[@aria-label="Закрыть"]')
    CHECKBOX_ALL = (By.XPATH, '//label[*[@id="checkbox-all"]]')
    ACCESS_GRANTED = (By.XPATH, '//*[text()="Доступ открыт"]')

    def get_audience_name(self, name):
        return (By.XPATH, f'//h5[text()="{name}"]')

    def get_user_list_name(self, name):
        return (By.XPATH, f'//div[text()="{name}"]')