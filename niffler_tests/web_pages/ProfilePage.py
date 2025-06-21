from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


class ProfilePage:

    __driver: WebDriver

    def __init__(self, driver: WebDriver):
        self.__driver = driver

    def enter_add_category(self, category_name: str) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Add new category"]').send_keys(category_name)

    def enter_edit_category(self, category_name: str) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Edit category"]').send_keys(category_name)

    def submit_add_category(self) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Add new category"]').send_keys(Keys.ENTER)

    def submit_edit_category(self) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Edit category"]').send_keys(Keys.ENTER)

    def submit_add_empty_category(self) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Add new category"]').send_keys(Keys.ENTER)

    def invisible_category_chip(self, category_name: str) -> bool:
        chips = self.__driver.find_elements(
            By.XPATH,
            f'//div[contains(@class, "MuiChip-clickable") and .//span[text()="{category_name}"]]'
        )
        return len(chips) == 0

    def is_input_cleared(self) -> bool:
        category_input = self.__driver.find_element(By.ID, "category")
        value = category_input.get_attribute("value")

        return value == ""

    def click_edit_category_icon(self) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Edit category"]').click()

    def click_category_chip(self, category_name: str) -> None:
        chips = self.__driver.find_elements(By.CSS_SELECTOR, 'span.MuiChip-label')
        for chip in chips:
            if chip.text == category_name:
                chip.click()

    def click_close_edit_category(self) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'button[aria-label="close"]').click()

    def click_archive_category_icon(self, category_name: str) -> None:
        chip = self.__driver.find_element(
            By.XPATH,
            f'//div[contains(@class, "MuiGrid-item") and .//span[text()="{category_name}"]]'

        )
        chip.find_element(By.CSS_SELECTOR, 'button[aria-label="Archive category"]').click()

    def click_archive_category_button(self) -> None:
        self.__driver.find_element(By.XPATH, '//button[.//text()[normalize-space()="Archive"]]').click()

    def text_edit_category_input(self) -> str:
        category_input =  self.__driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Edit category"]')
        return category_input.get_attribute("value")

    def text_alert_archive(self) -> str:
        alert_dialog_description = WebDriverWait(self.__driver, 5).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, 'div[aria-describedby="alert-dialog-slide-description"]'
            ))
        )
        return alert_dialog_description.text

    def clear_edit_category_input(self) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Edit category"]').clear()

    def helper_text_empty_add_category(self) -> str:
        element = self.__driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Add new category"] + span.input__helper-text')
        return element.text

    def alert_on_action(self) -> str:
        alert = WebDriverWait(self.__driver, 2).until(
            EC.visibility_of_element_located((
                By.XPATH, '//div[@role="alert"]'
            ))
        )
        return alert.text

