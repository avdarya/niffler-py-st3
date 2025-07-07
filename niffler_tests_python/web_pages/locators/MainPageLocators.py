from selenium.webdriver.common.by import By


class MainPageLocators:
    LOGO_IMG = (By.CSS_SELECTOR, 'img[alt="Niffler logo"]')
    LONELY_NIFFLER_IMG = (By.CSS_SELECTOR, 'img[alt="Lonely niffler"')
    CHECKBOX = (By.CSS_SELECTOR, f'input[type="checkbox"]')
    MULTI_SELECT_CHECKBOX = (By.CSS_SELECTOR, 'input[aria-label="select all rows"]')
    EDIT_ICON = (By.CSS_SELECTOR,'button[aria-label="Edit spending"]')
    AMOUNT_INPUT = ( By.ID, 'amount')
    DELETE_BUTTON = (By.ID, 'delete')
    SUBMIT_POPUP = (By.CSS_SELECTOR, 'div[aria-describedby="alert-dialog-slide-description"]')
    SUBMIT_DELETE_BUTTON = (By.XPATH, './/button[normalize-space(text())="Delete"]')
    CANCEL_DELETE_BUTTON = (By.XPATH, './/button[normalize-space(text())="Cancel"]')
    NEXT_PAGE_BUTTON = (By.ID, 'page-next')
    PREVIOUS_PAGE_BUTTON = (By.ID, 'page-prev')
    # ALERT_DIALOG = (By.XPATH, '//div[@role="alert"]')
    ALERT_DIALOG = (By.CSS_SELECTOR, 'div[role="alert"]')
    PERIOD_FIELD = (By.ID, 'period')
    PERIOD_VALUE = (By.CSS_SELECTOR, 'li[data-value="{}"]')
    PERIOD_INPUT = (By.CSS_SELECTOR, 'input[name="period"]')
    CURRENCY_FIELD = (By.ID, 'currency')
    CURRENCY_VALUE = (By.CSS_SELECTOR, 'li[data-value="{}"]')
    CURRENCY_INPUT = (By.CSS_SELECTOR, 'input[name="currency"]')
    SEARCH_INPUT = (By.CSS_SELECTOR, 'input[aria-label="search"]')
    CATEGORY_CELL = (By.CSS_SELECTOR, 'td[id^="enhanced-table-checkbox-"]')
    CATEGORY_CELL_FROM_CATEGORY = (By.XPATH, '//td[contains(@id, "enhanced-table-checkbox")]')
    CATEGORY_CELL_BY_ID = (By.CSS_SELECTOR, 'td[id="enhanced-table-checkbox-{}"]')
    SPEND_ROW = (By.CSS_SELECTOR, "tr.MuiTableRow-root")
    SPEND_ROW_FROM_CATEGORY = (By.XPATH, './ancestor::tr')
    SELECTED_SPEND_ROW = (By.CSS_SELECTOR, 'tr[aria-checked="true"]')


