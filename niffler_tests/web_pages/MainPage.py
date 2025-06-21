from datetime import datetime
from dateutil import tz  # pip install python-dateutil

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from configuration.ConfigProvider import ConfigProvider


class MainPage:

    __driver: WebDriver
    __url: str
    __timeout: int

    def __init__(self, driver: WebDriver, config: ConfigProvider) -> None:
        self.__driver = driver
        self.__url = config.get_ui_base_url() + "/main"
        self.__timeout = config.get('ui', 'timeout')

    def open(self) -> None:
        self.__driver.get(self.__url)
        self.__driver.refresh()

        WebDriverWait(self.__driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'img[alt="Niffler logo"]'))
        )

    def get_checkbox_state(self, spend_id: str) -> bool:
        row = self.__driver.find_element(
            By.XPATH,
            f'//td[@id="enhanced-table-checkbox-{spend_id}"]/ancestor::tr'
        )
        checked = row.get_attribute('aria-checked')
        return checked == "true"

    def click_checkbox(self, spend_id: str) -> None:
        checkbox_wrapper = WebDriverWait(self.__driver, 5).until(
            EC.element_to_be_clickable((
                By.XPATH,
                f'//td[@id="enhanced-table-checkbox-{spend_id}"]/preceding-sibling::td//span[contains(@class, "MuiButtonBase-root")]'
            ))
        )
        checkbox_wrapper.click()

    def click_edit_spend(self, spend_id: str) -> None:
        edit_button = self.__driver.find_element(
            By.XPATH,
            f'//td[@id="enhanced-table-checkbox-{spend_id}"]/ancestor::tr//button[@aria-label="Edit spending"]'
        )
        edit_button.click()

    def click_delete_spend(self) -> None:
        self.__driver.find_element(By.ID, 'delete').click()

    def click_submit_delete_spend(self) -> None:
        submit_popup = WebDriverWait(self.__driver, 2).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, 'div[aria-describedby="alert-dialog-slide-description"]'
            ))
        )
        submit_popup.find_element(By.XPATH, './/button[normalize-space(text())="Delete"]').click()

    def click_cancel_delete_spend(self) -> None:
        submit_popup = WebDriverWait(self.__driver, 2).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, 'div[aria-describedby="alert-dialog-slide-description"]'
            ))
        )
        submit_popup.find_element(By.XPATH, './/button[normalize-space(text())="Cancel"]').click()

    def is_found_spend_row(
            self,
            category_name: str,
            amount: str,
            currency: str,
            description: str | None,
            spend_date: str
    ) -> bool:
        date_obj = datetime.strptime(spend_date,  "%m/%d/%Y")
        formatted_date = date_obj.strftime("%b %d, %Y")

        # local_dt = datetime.fromisoformat(str(date_obj)).astimezone(tz.tzlocal())
        # formatted_date = local_dt.strftime("%b %d, %Y")

        currency_symbols = {
            "RUB": "₽",
            "USD": "$",
            "EUR": "€",
            "KZT": "₸",
        }
        amount_with_symbol = f"{amount} {currency_symbols.get(currency, '')}"

        while True:
            spend_rows = self.__driver.find_elements(By.CSS_SELECTOR, 'tr.MuiTableRow-root')
            first_row_category_id = spend_rows[0].find_element(By.XPATH, '//td[contains(@id, "enhanced-table-checkbox")]').get_attribute(
                'id'
            )
            first_row_category = self.__driver.find_element(By.ID, first_row_category_id)

            for row in spend_rows:
                row_text = row.text

                if (
                    category_name in row_text and
                   amount_with_symbol in row_text and
                    (description in row_text or not description)
                    # formatted_date in row_text
                ):
                    return True

            try:
                next_page_button = self.__driver.find_element(By.ID, "page-next")

                if next_page_button.get_attribute("disabled") is not None or "disabled" in next_page_button.get_attribute("class"):
                    break

                next_page_button.click()
                WebDriverWait(self.__driver, 10).until(
                    EC.staleness_of(first_row_category)
                )


            except Exception:
                break

        return False

    def alert_on_action(self) -> str:
        alert = WebDriverWait(self.__driver, 2).until(
            EC.visibility_of_element_located((
                By.XPATH, '//div[@role="alert"]'
            ))
        )
        return alert.text

    def click_next_page(self) -> None:
        self.__driver.find_element(By.ID, "page-next").click()