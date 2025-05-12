from selenium.webdriver.common.by import By

class LoginPageLocators:
    REGISTRATION_BUTTON = (By.CLASS_NAME, "ButtonCabinet_primary__LCfol")
    REGISTRATION_MODAL = (By.CLASS_NAME, "vkc__AuthRoot__contentIn")
    NAME = (By.CLASS_NAME, "vkc__LoginConnectOrPhone__caption")
    PROFILE_CREATION = (By.CLASS_NAME, "vkuiImageBase__children")
    WELCOME_WORDS = (By.CLASS_NAME, "registration_panelTitle__jHdpM")
    DROPDOWN_BUTTON = (By.CLASS_NAME, "AccountSwitch_changeAccountName__pzp40")
    CURRENT_LK = (By.CLASS_NAME, "vkuiSimpleCell__after.vkuiInternalSimpleCell__after")
    COPY_ID = (By.CLASS_NAME, "AccountSwitchListItem_userIdInner__k3sqA.AccountSwitchListItem_visible__vP0GR")
    COPY_TEXT = (By.CLASS_NAME, "AccountSwitchListItem_userIdInner__k3sqA.AccountSwitchListItem_userIdCopy__XZtkF.AccountSwitchListItem_visible__vP0GR")
    # COPY_ID = (By.CLASS_NAME, "AccountSwitchListItem_userIdInner__k3sqA AccountSwitchListItem_userIdCopy__XZtkF")