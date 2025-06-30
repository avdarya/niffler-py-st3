from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from niffler_tests_python.configuration.ConfigProvider import ConfigProvider


class MainPage:

    __driver: WebDriver
    __url: str
    __timeout: float

    def __init__(self, driver: WebDriver, config: ConfigProvider) -> None:
        self.__driver = driver
        self.__url = config.get_frontend_url() + "/main"
        self.__timeout = config.get_timeout()

    def open(self) -> None:
        self.__driver.get(self.__url)
        self.__driver.refresh()

        WebDriverWait(self.__driver, self.__timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'img[alt="Niffler logo"]'))
        )

    def get_checkbox_state(self, spend_row: WebElement) -> bool:
        checked = spend_row.get_attribute('aria-checked')
        return checked == "true"


    def click_checkbox(self, spend_row: WebElement) -> None:
        spend_row.find_element(By.CSS_SELECTOR, f'input[type="checkbox"]').click()

    def click_select_all_rows(self) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'input[aria-label="select all rows"]').click()

    def click_edit_spend(self, spend_row: WebElement) -> None:
        spend_row.find_element(By.CSS_SELECTOR,'button[aria-label="Edit spending"]').click()
        WebDriverWait(self.__driver, self.__timeout).until(
            EC.visibility_of_element_located((
                By.ID, 'amount'
            ))
        )

    def click_delete_spend(self) -> None:
        self.__driver.find_element(By.ID, 'delete').click()

    def click_submit_delete_spend(self) -> None:
        submit_popup = WebDriverWait(self.__driver, self.__timeout).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, 'div[aria-describedby="alert-dialog-slide-description"]'
            ))
        )
        submit_popup.find_element(By.XPATH, './/button[normalize-space(text())="Delete"]').click()

    def click_cancel_delete_spend(self) -> None:
        submit_popup = WebDriverWait(self.__driver, self.__timeout).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, 'div[aria-describedby="alert-dialog-slide-description"]'
            ))
        )
        submit_popup.find_element(By.XPATH, './/button[normalize-space(text())="Cancel"]').click()

    def click_next_page(self) -> None:
        self.__driver.find_element(By.ID, 'page-next').click()

    def click_previous_page(self) -> None:
        self.__driver.find_element(By.ID, 'page-prev').click()

    def alert_on_action(self) -> str:
        alert = WebDriverWait(self.__driver, self.__timeout).until(
            EC.visibility_of_element_located((
                By.XPATH, '//div[@role="alert"]'
            ))
        )
        return alert.text

    def click_period_input(self) -> None:
        self.__driver.find_element(By.ID, 'period').click()

    def click_period_value(self, period: str) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, f'li[data-value="{period}"]').click()

    def click_currency_input(self) -> None:
        self.__driver.find_element(By.ID, 'currency' ).click()

    def click_currency_value(self, currency: str) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, f'li[data-value="{currency}"]').click()

    def enter_search_query(self, query: str) -> None:
        query_input = self.__driver.find_element(By.CSS_SELECTOR, 'input[aria-label="search"]')
        query_input.send_keys(query)
        query_input.send_keys(Keys.ENTER)

    def get_search_query_input(self) -> str:
        query_input = self.__driver.find_element(By.CSS_SELECTOR, 'input[aria-label="search"]')
        return query_input.get_attribute('value')

    def get_period_input(self) -> str:
        period_input = self.__driver.find_element(By.CSS_SELECTOR, 'input[name="period"]')
        return period_input.get_attribute('value')

    def get_currency_input(self) -> str:
        currency_input = self.__driver.find_element(By.CSS_SELECTOR, 'input[name="currency"]')
        return currency_input.get_attribute('value')

    def get_spend_ids_row(self) -> list[str]:
        spend_ids = []
        elements = WebDriverWait(self.__driver, self.__timeout).until(
            EC.visibility_of_any_elements_located((
                By.CSS_SELECTOR, 'td[id^="enhanced-table-checkbox-"]'
            ))
        )
            # self.__driver.find_elements(By.CSS_SELECTOR, 'td[id^="enhanced-table-checkbox-"]'))
        for e in elements:
            spend_id = e.get_attribute("id").replace("enhanced-table-checkbox-", "")
            spend_ids.append(spend_id)
        return spend_ids

    def get_selected_spend_ids_row(self) -> list[str]:
        spend_ids = []
        selected_rows = self.__driver.find_elements(By.CSS_SELECTOR, 'tr[aria-checked="true"]')
        for spend in selected_rows:
            spend_checkbox = spend.find_element(By.CSS_SELECTOR, 'td[id^="enhanced-table-checkbox-"]')
            spend_id = spend_checkbox.get_attribute("id").replace("enhanced-table-checkbox-", "")
            spend_ids.append(spend_id)
        return spend_ids

    def get_spend_row(self, spend_id: str) -> WebElement | None:
        try:
            img_lonely_niffler = self.__driver.find_element(By.CSS_SELECTOR, 'img[alt="Lonely niffler"')
            if img_lonely_niffler.is_displayed():
                return None
        except NoSuchElementException:
            pass
        while True:
            spend_rows = self.__driver.find_elements(By.CSS_SELECTOR, "tr.MuiTableRow-root")
            first_row_category_id = (spend_rows[0]
                .find_element(By.XPATH, '//td[contains(@id, "enhanced-table-checkbox")]')
                .get_attribute('id')
            )
            first_row_category = self.__driver.find_element(By.ID, first_row_category_id)
            try:
                td = self.__driver.find_element(By.CSS_SELECTOR, f'td[id="enhanced-table-checkbox-{spend_id}"]')
                row = td.find_element(By.XPATH, './ancestor::tr')
                return row
            except NoSuchElementException:
                pass

            try:
                next_page_button = self.__driver.find_element(By.ID, "page-next")
                if next_page_button.get_attribute("disabled") is not None or "disabled" in next_page_button.get_attribute("class"):
                    break
                next_page_button.click()
                WebDriverWait(self.__driver, self.__timeout).until(
                    EC.staleness_of(first_row_category)
                )
            except Exception:
                break

        return None