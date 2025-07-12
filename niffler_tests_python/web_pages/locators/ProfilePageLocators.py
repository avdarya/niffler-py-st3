from dataclasses import dataclass
from selenium.webdriver.common.by import By


@dataclass
class ProfilePageLocators:
    FULLNAME_INTPUT = (By.ID, 'name')
    ADD_CATEGORY_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Add new category"]')
    EDIT_CATEGORY_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Edit category"]')
    CATEGORY_CHIP_BY_NAME = (By.XPATH, '//div[contains(@class, "MuiChip-clickable") and .//span[text()="{}"]]')
    CATEGORY_CHIP = (By.CSS_SELECTOR, 'div.MuiChip-root[role="button"]')
    CATEGORY_BOX = (By.XPATH, '//span[text()="{}"]/ancestor::div[contains(@class, "MuiBox-root")]')
    EDIT_ICON = (By.CSS_SELECTOR, 'button[aria-label="Edit category"]')
    CLOSE_ICON = (By.CSS_SELECTOR, 'button[aria-label="close"]')
    ARCHIVE_ICON = (By.CSS_SELECTOR, 'button[aria-label="Archive category"]')
    UNARCHIVE_ICON = (By.CSS_SELECTOR, 'button[aria-label="Unarchive category"]')
    SUBMIT_ARCHIVE_BUTTON = (By.XPATH, '//button[normalize-space()="Archive"]')
    SUBMIT_UNARCHIVE_BUTTON = (By.XPATH, '//button[normalize-space()="Unarchive"]')
    SAVE_CHANGES_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')
    SHOW_ARCHIVED_BUTTON = (By.CSS_SELECTOR, 'input[type="checkbox"]')
    SUBMIT_POPUP = (By.CSS_SELECTOR, 'div[aria-describedby="alert-dialog-slide-description"]')
    POPUP_DESCRIPTION = (By.CSS_SELECTOR, 'p[id="alert-dialog-slide-description"]')
    POPUP_TITLE = (By.CSS_SELECTOR, 'h2')
    ALERT_DIALOG = (By.CSS_SELECTOR, 'div[role="alert"]')
    ADD_CATEGORY_HELPER_TEXT = (By.CSS_SELECTOR, 'input[placeholder="Add new category"] + span.input__helper-text')
