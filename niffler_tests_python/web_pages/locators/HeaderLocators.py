from dataclasses import dataclass
from selenium.webdriver.common.by import By

@dataclass
class HeaderLocators:
    MENU_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Menu"]')
    PROFILE_BUTTON = (By.CSS_SELECTOR, 'a[href = "/profile"]')
    SPENDING_BUTTON = (By.CSS_SELECTOR, 'a[href="/spending"]')
    ACCOUNT_MENU= (By.ID, 'account-menu')
