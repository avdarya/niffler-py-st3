from selenium.webdriver.common.by import By

class HeaderLocators:
    MENU_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Menu"]')
    PROFILE_BUTTON = (By.CSS_SELECTOR, 'a[href = "/profile"]')
    SPENDING_BUTTON = (By.CSS_SELECTOR, 'a[href="/spending"]')
