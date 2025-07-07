import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from niffler_tests_python.configuration.ConfigProvider import ConfigProvider
from niffler_tests_python.web_pages.BasePage import BasePage
from niffler_tests_python.web_pages.locators.SpendingPageLocators import SpendingPageLocators


class SpendingPage(BasePage):

    def __init__(self, driver: WebDriver, config: ConfigProvider):
        super().__init__(driver, config)
        self.locator = SpendingPageLocators

    @allure.step('[UI /spending] Clear amount input')
    def clear_amount_input(self) -> None:
        self._driver.find_element(*self.locator.AMOUNT_INPUT).clear()

    @allure.step('[UI /spending] Fill amount input: amount={amount}')
    def enter_amount_input(self, amount: str) -> None:
        self._driver.find_element(*self.locator.AMOUNT_INPUT).send_keys(amount)

    @allure.step('[UI /spending] Get amount input text')
    def get_amount_input(self) -> str:
        amount_input = self._driver.find_element(*self.locator.AMOUNT_INPUT)
        return amount_input.get_attribute('value')

    @allure.step('[UI /spending] Get helper text for amount input')
    def helper_text_amount_input(self) -> str:
        amount_div = self._driver.find_element(*self.locator.AMOUNT_FIELD)
        helper_text = amount_div.find_element(*self.locator.HELPER_TEXT)
        return helper_text.text

    @allure.step('[UI /spending] Fill description input: description={description}')
    def enter_description_input(self, description: str) -> None:
        self._driver.find_element(*self.locator.DESCRIPTION_INPUT).send_keys(description)

    @allure.step('[UI /spending] Get description input text')
    def get_description_input(self) -> str:
        return self._driver.find_element(*self.locator.DESCRIPTION_INPUT).get_attribute('value')

    @allure.step('[UI /spending] Clear description input')
    def clear_description_input(self) -> None:
        self._driver.find_element(*self.locator.DESCRIPTION_INPUT).clear()

    @allure.step('[UI /spending] Fill date input: date={spend_date}')
    def enter_date_input(self, spend_date: str) -> None:
        date_input = self._driver.find_element(*self.locator.DATE_INPUT)
        ActionChains(self._driver).click(date_input).send_keys(spend_date).perform()

    @allure.step('[UI /spending] Get date input text')
    def get_date_input(self) -> str:
        date_input = self._driver.find_element(*self.locator.DATE_INPUT)
        date_value = date_input.get_attribute('value')
        return date_value

    @allure.step('[UI /spending] Clear date input')
    def clear_date_input(self) -> None:
        self._driver.find_element(*self.locator.DATE_INPUT).clear()

    @allure.step('[UI /spending] Get selected currency input')
    def get_selected_currency_input(self) -> str:
        currency_text = self._driver.find_element(*self.locator.CURRENCY_FIELD).text
        currency_value = currency_text.split(' ')[-1]
        return currency_value

    @allure.step('[UI /spending] Click currency input')
    def click_currency_input(self) -> None:
        self._driver.find_element(*self.locator.CURRENCY_INPUT).click()
        self.wait_for_visibility_element(self.locator.CURRENCY_DIALOG)

    @allure.step('[UI /spending] Click currency value: currency_value={currency_value}')
    def click_currency_value(self, currency_value: str) -> None:
        self._driver.find_element(
            self.locator.CURRENCY_VALUE[0],
            self.locator.CURRENCY_VALUE[1].format(currency_value)
        ).click()

    @allure.step('[UI /spending] Get category input text')
    def get_category_input(self) -> str:
        return self._driver.find_element(*self.locator.CATEGORY_INPUT).get_attribute("value")

    @allure.step('[UI /spending] Fill category input: category={category_name}')
    def enter_category_input(self, category_name: str) -> None:
        self._driver.find_element(*self.locator.CATEGORY_INPUT).send_keys(category_name)

    @allure.step('[UI /spending] Click category: category_name={category_name}')
    def click_category(self, category_name: str) -> None:
        self._driver.find_element(
            self.locator.CATEGORY_CHIP[0],
            self.locator.CATEGORY_CHIP[1].format(category_name)
        ).click()
        WebDriverWait(self._driver, self._timeout).until(
            lambda d: d.find_element(*self.locator.CATEGORY_INPUT).get_attribute("value") != ""
        )

    @allure.step('[UI /spending] Clear category input')
    def clear_category_input(self) -> None:
        self._driver.find_element(*self.locator.CATEGORY_INPUT).clear()

    @allure.step('[UI /spending] Get helper text for category input')
    def helper_text_category_input(self) -> str:
        category_div = self._driver.find_element(*self.locator.CATEGORY_FIELD)
        helper_text = category_div.find_element(*self.locator.HELPER_TEXT)
        return helper_text.text

    @allure.step('[UI /spending] Click add button')
    def click_save_spend(self) -> None:
        self._driver.find_element(*self.locator.ADD_BUTTON).click()
