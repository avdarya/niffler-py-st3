from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from niffler_tests.configuration.ConfigProvider import ConfigProvider


class SpendingPage:

    __driver: WebDriver
    __timeout: float

    def __init__(self, driver: WebDriver, config: ConfigProvider):
        self.__driver = driver
        self.__timeout = config.get_timeout()

    def clear_amount_input(self) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'input[name="amount"]').clear()

    def enter_amount_input(self, amount: str) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'input[name="amount"]').send_keys(amount)

    def get_amount_input(self) -> str:
        amount_input = self.__driver.find_element(By.CSS_SELECTOR, 'input[name="amount"]')
        return amount_input.get_attribute('value')

    def helper_text_amount_input(self) -> str:
        amount_div = self.__driver.find_element(By.XPATH, './/input[@id="amount"]/parent::div')
        helper_text = amount_div.find_element(By.CSS_SELECTOR, '.input__helper-text')
        return helper_text.text

    def enter_description_input(self, description: str) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'input[name="description"]').send_keys(description)

    def get_description_input(self) -> str:
        description_input = self.__driver.find_element(By.CSS_SELECTOR, 'input[name="description"]')
        return description_input.get_attribute('value')

    def clear_description_input(self) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'input[name="description"]').clear()

    def enter_date_input(self, spend_date: str) -> None:
        date_input = self.__driver.find_element(By.CSS_SELECTOR, 'input[name="date"]')
        ActionChains(self.__driver).click(date_input).send_keys(spend_date).perform()

    def get_date_input(self) -> str:
        date_input = self.__driver.find_element(By.CSS_SELECTOR, 'input[name="date"]')
        date_value = date_input.get_attribute('value')
        return date_value

    def clear_date_input(self) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'input[name="date"]').clear()

    def get_selected_currency_input(self) -> str:
        currency_text = self.__driver.find_element(By.CSS_SELECTOR, 'div[aria-labelledby="currency"]').text
        currency_value = currency_text.split(' ')[-1]
        return currency_value

    def click_currency_input(self) -> None:
        self.__driver.find_element(By.ID, 'currency').click()
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'ul[role="listbox"]'))

    def click_currency_value(self, currency_value: str) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, f'li[data-value="{currency_value}"]').click()

    def get_category_input(self) -> str:
        return self.__driver.find_element(By.ID, "category").get_attribute("value")

    def enter_category_input(self, category_name: str) -> None:
        self.__driver.find_element(By.ID, "category").send_keys(category_name)

    def click_category(self, category_name: str) -> None:
        self.__driver.find_element(
            By.XPATH,
            f'//span[contains(@class, "MuiChip-label") and text()="{category_name}"]'
        ).click()
        WebDriverWait(self.__driver, self.__timeout).until(
            lambda d: d.find_element(By.ID, "category").get_attribute("value") != ""
        )

    def clear_category_input(self) -> None:
        self.__driver.find_element(By.ID, "category").clear()

    def helper_text_category_input(self) -> str:
        category_div = self.__driver.find_element(By.XPATH, './/input[@id="category"]/parent::div')
        helper_text = category_div.find_element(By.CSS_SELECTOR, '.input__helper-text')
        return helper_text.text

    def click_save_spend(self) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'button[id="save"]').click()