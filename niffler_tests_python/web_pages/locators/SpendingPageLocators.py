from selenium.webdriver.common.by import By


class SpendingPageLocators:
    AMOUNT_INPUT = (By.ID, 'amount')
    AMOUNT_FIELD = (By.XPATH, './/input[@id="amount"]/parent::div')
    AMOUNT_INPUT_HELPER_TEXT = (By.CSS_SELECTOR, '.input__helper-text')
    DESCRIPTION_INPUT = (By.ID, 'description')
    DATE_INPUT = (By.CSS_SELECTOR, 'input[name="date"]')
    CURRENCY_FIELD = (By.CSS_SELECTOR, 'div[aria-labelledby="currency"]')
    CURRENCY_INPUT = (By.ID, 'currency')
    CURRENCY_DIALOG = (By.CSS_SELECTOR, 'ul[role="listbox"]')
    CURRENCY_VALUE = (By.CSS_SELECTOR, 'li[data-value="{}"]')
    CATEGORY_INPUT = (By.ID, 'category')
    CATEGORY_FIELD = (By.XPATH, './/input[@id="category"]/parent::div')
    CATEGORY_CHIP = (By.XPATH, '//span[contains(@class, "MuiChip-label") and text()="{}"]')
    HELPER_TEXT = (By.CSS_SELECTOR, '.input__helper-text')
    ADD_BUTTON = (By.CSS_SELECTOR, 'button[id="save"]')
