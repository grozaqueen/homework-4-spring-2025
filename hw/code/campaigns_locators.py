from selenium.webdriver.common.by import By

class BasePageLocators:
    pass

class CampaignPageLocators(BasePageLocators):

    @staticmethod
    def _xpath(xpath_expression: str) -> tuple[By, str]:
        return (By.XPATH, xpath_expression)

    @staticmethod
    def _by_text_contains(tag: str, text: str) -> tuple[By, str]:
        return CampaignPageLocators._xpath(f'//{tag}[contains(text(), "{text}")]')

    @staticmethod
    def _by_text_exact(tag: str, text: str) -> tuple[By, str]:
        return CampaignPageLocators._xpath(f'//{tag}[text()="{text}"]')

    @staticmethod
    def _by_class_contains(tag: str, class_name: str) -> tuple[By, str]:
        return CampaignPageLocators._xpath(f'//{tag}[contains(@class, "{class_name}")]')

    @staticmethod
    def _by_class_starts_with(tag: str, class_name_prefix: str) -> tuple[By, str]:
        return CampaignPageLocators._xpath(f'//{tag}[starts-with(@class, "{class_name_prefix}")]')

    @staticmethod
    def _by_attribute_exact(tag: str, attribute: str, value: str) -> tuple[By, str]:
        return CampaignPageLocators._xpath(f'//{tag}[@{attribute}="{value}"]')

    @staticmethod
    def _by_testid(testid: str, tag: str = '*') -> tuple[By, str]:
        return CampaignPageLocators._xpath(f'//{tag}[@data-testid="{testid}"]')

    ADD_MEDIA_AI_ELEMENT = _by_class_contains('div', 'ImageItem_imageItem')
    ADD_MEDIA_AI_BUTTON = _by_text_contains('span', 'Добавить (')
    PUBLISH_BUTTON = _by_text_contains('span', 'Опубликовать')

    DISMISS_BUTTON = _xpath('//div[@role="button" and @aria-label="Закрыть"]')
    CREATE_CAMPAIGN_BUTTON = _by_testid('create-button')
    EDITABLE_HEADER = _by_class_starts_with('div', 'EditableTitle')

    _EDITABLE_TITLE_BASE_XPATH_PART = '//div[starts-with(@class, "EditableTitle")]'
    EDITABLE_CAMPAIGN_HEADER = _xpath(f'{_EDITABLE_TITLE_BASE_XPATH_PART}[.//*[contains(text(), "Кампания")]]')
    EDITABLE_GROUP_HEADER = _xpath(f'{_EDITABLE_TITLE_BASE_XPATH_PART}[.//*[contains(text(), "Группа")]]')
    EDITABLE_AD_HEADER = _xpath(f'{_EDITABLE_TITLE_BASE_XPATH_PART}[.//*[contains(text(), "Объявление")]]')


    SITE_OPTION = _by_attribute_exact('div', 'data-id', 'site_conversions')
    GROUP_OPTION = _by_attribute_exact('div', 'data-id', 'social')
    ADVERTISED_SITE_FIELD = _by_attribute_exact('input', 'placeholder', 'Вставьте ссылку или выберите из списка')

    BUDGET = _by_testid('targeting-not-set')
    START_DATE = _by_testid('start-date')
    END_DATE = _by_testid('end-date')

    CONTINUE = _by_text_contains('span', 'Продолжить')
    REGION = _by_text_contains('span', 'Россия')
    AD_LOGO_UPLOAD = _by_testid('set-global-image')
    AD_HEADER = _by_testid('заголовок, макс. 40 символов')
    AD_SHORT_DESCRIPTION = _by_testid('описание, макс. 90 символов')
    AD_MEDIATEKA = _by_text_contains('span', 'Медиатека')
    MEDIATEKA_FILE = _by_class_starts_with('div', 'ImageItem')
    CLOSE_BUTTON = _by_attribute_exact('button', 'aria-label', 'Close')

    CLOSE_ERR_BUTTON = _by_class_starts_with('button', 'CommonError_closeButton__')

    ADD_BUTTON = _by_text_contains('span', 'Добавить')
    AD_LOAD_MEDIAFILES = _by_class_contains('div', 'Loading_loading')
    FILE_INPUT = _by_attribute_exact('input', 'type', 'file')
    ADD_MEDIA_FILE_INPUT = _xpath('//label[starts-with(@class, "LocalFileSelector_file")]//input[@type="file"]')

    LOADED_MEDIA_PREVIEW = _xpath('//*[contains(@class, "MediaContainer_image") or contains(@class, "VideoContainer_video")]')
    AD_LOGO_PREVIEW = _xpath('//img[@alt="media preview" and contains(@class, "AdMediaPreview_img")]')

    ADD_MEDIA_AI = _by_text_contains('span', 'Созданное нейросетью')
    MEDIA_PLACEHOLDER = _by_class_contains('*', 'MediaPlaceholder')
    DESCRIPTION = _by_testid('Описание 2000 знаков')

    GROUP_SELECTOR = _by_class_starts_with('div', 'VkOwnerSelector_select')
    ENTER_OTHER_GROUP = _by_text_exact('*', 'Другое сообщество')
    ADD_GROUP_BUTTON = _by_text_exact('*', 'Добавить')
    CONFIRM_CAMPAIGN = _by_text_exact('span', 'Отправить')
    SHOT_IN_VIDEO = _by_text_exact('span', 'Ролик в видео')

    SELECT_LOGO_BUTTON = _by_text_contains('span', 'Выбрать логотип')
    LOGO_FILE_INPUT_IN_MODAL = _xpath('//div[contains(@class, "MediaLibrary_container")]//input[@type="file"]')
    LOADED_LOGO_PREVIEW = _xpath('//div[contains(@class, "UploadMediaButton_image")]//img')

    ACTIONS_ICON = _by_testid('actions')
    DELETE_BUTTON = _by_text_contains('*', 'Удалить')
    CAMPAIGNS_MENU_TAB = _by_attribute_exact('*', 'id', 'dashboardV2.plans')

    SEARCH_INPUT = _by_testid('filter-search-input')
    FILTER_BUTTON = _by_testid('filter-button')
    FILTERS_RESET_BUTTON = _by_testid('filters-reset-all-button')
    FILTERS_APPLY_BUTTON = _by_testid('filters-apply-button')

    TAGS_SELECTOR = _by_testid('tags-selector')
    CREATE_TAG = _by_testid('create_tag')
    FOLDER_NAME_INPUT = _by_attribute_exact('input', 'value', 'Новая папка')
    CLOSE_CREATE_FOLDER_POPUP = _xpath('//div[contains(@class, "TagAdPlanModal_actions")]//span[text()="Отмена"]')
    DELETE_FOLDER_BUTTON = _by_text_exact('span', 'Удалить папку')
    CONFIRM_DELETE_FOLDER_BUTTON = _xpath('//div[contains(@class,"ModalConfirm_buttons")]//span[text()="Удалить"]')

    ADD_CAMPAIGNS_TO_FOLDER = _by_text_exact('span', 'Добавить кампании в папку')
    SAVE = _by_text_exact('span', 'Сохранить')

    EDIT_BUTTON = _by_testid('edit')
    ADS_MENU_ITEM = _by_attribute_exact('*', 'id', 'dashboardV2.ads')
    EDIT_HEADER = _by_text_exact('*', 'Редактирование')


    def get_campaign_name_locator(self, name: str) -> tuple[By, str]:
        return (By.XPATH, f'//div[starts-with(@class, "nameCellContent_content")]//button[text()="{name}"]')

    def get_folder_name_locator(self, name: str) -> tuple[By, str]:
        return (By.XPATH, f'//div[starts-with(@data-testid, "tag") and text()="{name}"]')

    def get_folder_edit_icon_locator(self, name: str) -> tuple[By, str]:
        folder_name_part = f'div[starts-with(@data-testid, "tag") and text()="{name}"]'
        cell_container_class = "vkuiSimpleCell"
        actions_container_class = "vkuiSimpleCell__after"

        loc = (f'//{folder_name_part}'
               f'/ancestor::div[contains(@class, "{cell_container_class}")][1]'
               f'//div[contains(@class, "{actions_container_class}")]//button[@aria-label="Редактировать"]')
        return (By.XPATH, loc)

    def get_select_campaign_element(self, name: str) -> tuple[By, str]:
        return (By.XPATH, f'//span[contains(@class, "vkuiCheckbox__titleBefore") and text()="{name}"]/ancestor::label[1]//input[@type="checkbox"]')

    def get_ad_name_locator(self, name: str) -> tuple[By, str]:
        return (By.XPATH, f'//button[text()="{name}"]')

    def get_editable_campaign_header(self, name: str) -> tuple[By, str]:
        return self._xpath(f'{self._EDITABLE_TITLE_BASE_XPATH_PART}[.//*[contains(text(), "{name}")]]')

    def get_editable_ad_header(self, name: str) -> tuple[By, str]:
        return self._xpath(
                f'{self._EDITABLE_TITLE_BASE_XPATH_PART}[.//*[contains(@class, "EditableTitle_title") and contains(text(), "{name}")]]')