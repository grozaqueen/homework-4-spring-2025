from selenium.webdriver.common.by import By

from base_locators import BasePageLocators


class CampaignPageLocators(BasePageLocators):
    DISMISS_BUTTON = (By.XPATH, '//div[@role="button" and @aria-label="Закрыть"]')
    CREATE_CAMPAIGN_BUTTON = (By.XPATH, "//*[@data-testid='create-button']")
    EDITABLE_HEADER = (By.XPATH, '//div[starts-with(@class, "EditableTitle")]')
    EDITABLE_CAMPAIGN_HEADER = (
    By.XPATH, '//div[starts-with(@class, "EditableTitle") and *[contains(text(), "Кампания")]]')
    EDITABLE_GROUP_HEADER = (By.XPATH, '//div[starts-with(@class, "EditableTitle") and *[contains(text(), "Группа")]]')
    EDITABLE_AD_HEADER = (By.XPATH, '//div[starts-with(@class, "EditableTitle") and *[contains(text(), "Объявление")]]')
    SITE_OPTION = (By.XPATH, '//div[@data-id="site_conversions"]')
    GROUP_OPTION = (By.XPATH, '//div[@data-id="social"]')
    ADVERTISED_SITE_FIELD = (By.XPATH, '//input[@placeholder="Вставьте ссылку или выберите из списка"]')
    BUDGET = (By.XPATH, '//*[@data-testid="targeting-not-set"]')
    START_DATE = (By.XPATH, '//*[@data-testid="start-date"]')
    END_DATE = (By.XPATH, '//*[@data-testid="end-date"]')
    CONTINUE = (By.XPATH, '//span[contains(text(), "Продолжить")]')
    REGION = (By.XPATH, '//span[contains(text(), "Россия")]')
    AD_LOGO_UPLOAD = (By.XPATH, '//*[@data-testid="set-global-image"]')
    AD_HEADER = (By.XPATH, '//*[@data-testid="заголовок, макс. 40 символов"]')
    AD_SHORT_DESCRIPTION = (By.XPATH, '//*[@data-testid="описание, макс. 90 символов"]')
    AD_MEDIATEKA = (By.XPATH, '//span[contains(text(), "Медиатека")]')
    MEDIATEKA_FILE = (By.XPATH, '//div[starts-with(@class, "ImageItem")]')
    CLOSE_BUTTON = (By.XPATH, '//button[@aria-label="Close"]')

    # CommonError_closeButton__ - tUR1

    CLOSE_ERR_BUTTON = (By.XPATH, '//button[starts-with(@class, "CommonError_closeButton__-tUR1")]')

    ADD_BUTTON = (By.XPATH, '//span[contains(text(), "Добавить")]')
    AD_LOAD_MEDIAFILES = (By.XPATH, '//div[contains(@class, "Loading_loading")]')
    FILE_INPUT = (By.XPATH, '//input[@type="file"]')
    ADD_MEDIA_FILE_INPUT = (By.XPATH, '//label[starts-with(@class, "LocalFileSelector_file")]//input[@type="file"]')
    LOADED_MEDIA_PREVIEW = (
    By.XPATH, '//*[contains(@class, "MediaContainer_image") or contains(@class, "VideoContainer_video")]')
    AD_LOGO_PREVIEW = (By.XPATH, '//img[@alt="media preview" and contains(@class, "AdMediaPreview_img")]')
    ADD_MEDIA_AI = (By.XPATH, '//span[contains(text(), "Созданное нейросетью")]')
    MEDIA_PLACEHOLDER = (By.XPATH, '//*[contains(@class, "MediaPlaceholder")]')
    DESCRIPTION = (By.XPATH, '//*[@data-testid="Описание 2000 знаков"]')
    ADD_MEDIA_AI_ELEMENT = (By.XPATH, '//div[contains(@class, "ImageItem_imageItem")]')
    ADD_MEDIA_AI_BUTTON = (By.XPATH, '//span[contains(text(), "Добавить (")]')
    PUBLISH_BUTTON = (By.XPATH, '//span[contains(text(), "Опубликовать")]')
    GROUP_SELECTOR = (By.XPATH, '//div[starts-with(@class, "VkOwnerSelector_select")]')
    ENTER_OTHER_GROUP = (By.XPATH, '//*[text()="Другое сообщество"]')
    ADD_GROUP_BUTTON = (By.XPATH, '//*[text()="Добавить"]')
    CONFIRM_CAMPAIGN = (By.XPATH, '//span[text()="Отправить"]')
    SHOT_IN_VIDEO = (By.XPATH, '//span[text()="Ролик в видео"]')

    SELECT_LOGO_BUTTON = (By.XPATH, '//span[contains(text(), "Выбрать логотип")]')
    LOGO_FILE_INPUT_IN_MODAL = (By.XPATH, '//div[contains(@class, "MediaLibrary_container")]//input[@type="file"]')

    LOADED_LOGO_PREVIEW = (By.XPATH, '//div[contains(@class, "UploadMediaButton_image")]//img')

    ACTIONS_ICON = (By.XPATH, '//*[@data-testid="actions"]')
    DELETE_BUTTON = (By.XPATH, '//*[contains(text(), "Удалить")]')
    CAMPAIGNS_MENU_TAB = (By.XPATH, '//*[@id="dashboardV2.plans"]')

    SEARCH_INPUT = (By.XPATH, '//*[@data-testid="filter-search-input"]')
    FILTER_BUTTON = (By.XPATH, '//*[@data-testid="filter-button"]')
    FILTERS_RESET_BUTTON = (By.XPATH, '//*[@data-testid="filters-reset-all-button"]')
    FILTERS_APPLY_BUTTON = (By.XPATH, '//*[@data-testid="filters-apply-button"]')

    TAGS_SELECTOR = (By.XPATH, '//*[@data-testid="tags-selector"]')
    CREATE_TAG = (By.XPATH, '//*[@data-testid="create_tag"]')
    FOLDER_NAME_INPUT = (By.XPATH, '//input[@value="Новая папка"]')
    CLOSE_CREATE_FOLDER_POPUP = (By.XPATH, '//div[contains(@class, "TagAdPlanModal_actions")]//span[text()="Отмена"]')
    DELETE_FOLDER_BUTTON = (By.XPATH, '//span[text()="Удалить папку"]')
    CONFIRM_DELETE_FOLDER_BUTTON = (By.XPATH, '//div[contains(@class,"ModalConfirm_buttons")]//span[text()="Удалить"]')

    ADD_CAMPAIGNS_TO_FOLDER = (By.XPATH, '//span[text()="Добавить кампании в папку"]')
    SAVE = (By.XPATH, '//span[text()="Сохранить"]')

    EDIT_BUTTON = (By.XPATH, '//*[@data-testid="edit"]')

    ADS_MENU_ITEM = (By.XPATH, '//*[@id="dashboardV2.ads"]')
    EDIT_HEADER = (By.XPATH, '//*[text()="Редактирование"]')

    def get_campaign_name_locator(self, name):
        return (By.XPATH, f'//div[starts-with(@class, "nameCellContent_content")]//button[text()="{name}"]')

    def get_folder_name_locator(self, name):
        return (By.XPATH, f'//div[starts-with(@data-testid, "tag") and text()="{name}"]')

    def get_folder_edit_icon_locator(self, name):
        name_loc = self.get_folder_name_locator(name=name)[1]
        loc = name_loc + '/../../../../div[contains(@class, "vkuiSimpleCell__after")]'
        return (By.XPATH, loc)

    def get_select_campaign_element(self, name):
        return (By.XPATH, f'//span[contains(@class, "vkuiCheckbox__titleBefore") and text()="{name}"]')

    def get_ad_name_locator(self, name):
        return (By.XPATH, f'//button[text()="{name}"]')

    def get_editable_campaign_header(self, name):
        return (By.XPATH, f'//div[starts-with(@class, "EditableTitle") and *[contains(text(), {name})]]')

    def get_editable_ad_header(self, name):
        return (By.XPATH,
                f'//div[starts-with(@class, "EditableTitle") and *[contains(@class, "EditableTitle_title") and contains(text(), {name})]]')
