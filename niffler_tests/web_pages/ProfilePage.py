from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from niffler_tests.configuration.ConfigProvider import ConfigProvider


class ProfilePage:

    __driver: WebDriver
    __timeout: float

    def __init__(self, driver: WebDriver, config: ConfigProvider):
        self.__driver = driver
        self.__timeout = config.get_timeout()

    def enter_add_category(self, category_name: str) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Add new category"]').send_keys(category_name)

    def enter_edit_category(self, category_name: str) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Edit category"]').send_keys(category_name)

    def enter_name(self, name: str) -> None:
        name_input = self.__driver.find_element(By.ID, 'name')
        name_input.clear()
        name_input.send_keys(name)

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

    def click_edit_category_icon(self, category_name: str) -> None:
        category_box = WebDriverWait(self.__driver, self.__timeout).until(
            EC.visibility_of_element_located((
                By.XPATH,
                f'//span[text()="{category_name}"]/ancestor::div[contains(@class, "MuiBox-root")]'
            ))
        )
        edit_icon = category_box.find_element(By.CSS_SELECTOR, 'button[aria-label="Edit category"]')
        edit_icon.click()

    def click_category_chip(self, category_name: str) -> None:
        chips = self.__driver.find_elements(By.CSS_SELECTOR, 'span.MuiChip-label')
        for chip in chips:
            if chip.text == category_name:
                chip.click()

    def click_close_edit_category(self) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'button[aria-label="close"]').click()

    def click_archive_category_icon(self, category_name: str) -> None:
        category_box = WebDriverWait(self.__driver, self.__timeout).until(
            EC.visibility_of_element_located((
                By.XPATH,
                f'//span[text()="{category_name}"]/ancestor::div[contains(@class, "MuiBox-root")]'
            ))
        )
        archive_icon = category_box.find_element(By.CSS_SELECTOR, 'button[aria-label="Archive category"]')
        archive_icon.click()

    def click_unarchive_category_icon(self, category_name: str) -> None:
        category_box = WebDriverWait(self.__driver, self.__timeout).until(
            EC.visibility_of_element_located((
                By.XPATH,
                f'//span[text()="{category_name}"]/ancestor::div[contains(@class, "MuiBox-root")]'
            ))
        )
        unarchive_icon = category_box.find_element(By.CSS_SELECTOR, 'button[aria-label="Unarchive category"]')
        unarchive_icon.click()

    def click_archive_category_button(self) -> None:
        self.__driver.find_element(By.XPATH, '//button[normalize-space()="Archive"]').click()

    def click_unarchive_category_button(self) -> None:
        self.__driver.find_element(By.XPATH, '//button[normalize-space()="Unarchive"]').click()

    def click_save_changes(self) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    def click_show_archived(self) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]').click()

    def text_edit_category_input(self) -> str:
        category_input =  self.__driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Edit category"]')
        return category_input.get_attribute("value")

    def alert_dialog_description(self) -> str:
        alert_dialog = WebDriverWait(self.__driver, self.__timeout).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, 'div[aria-describedby="alert-dialog-slide-description"]'
            ))
        )
        alert_dialog_description = alert_dialog.find_element(By.CSS_SELECTOR, 'p[id="alert-dialog-slide-description"]')
        return alert_dialog_description.text

    def alert_dialog_title(self) -> str:
        alert_dialog = WebDriverWait(self.__driver, self.__timeout).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, 'div[aria-describedby="alert-dialog-slide-description"]'
            ))
        )
        alert_dialog_title = alert_dialog.find_element(By.CSS_SELECTOR, 'h2')
        return alert_dialog_title.text

    def clear_edit_category_input(self) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Edit category"]').clear()

    def helper_text_empty_add_category(self) -> str:
        element = self.__driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Add new category"] + span.input__helper-text')
        return element.text

    def is_active_category_chip(self, category_name: str) -> bool:
        category_box = WebDriverWait(self.__driver, self.__timeout).until(
            EC.visibility_of_element_located((
                By.XPATH,
                f'//span[text()="{category_name}"]/ancestor::div[contains(@class, "MuiBox-root")]'
            ))
        )
        category_chip = category_box.find_element(By.CSS_SELECTOR, 'div[role="button"]')
        classes = set(category_chip.get_attribute('class').split(' '))
        required_classes = {'MuiChip-colorPrimary'}
        return required_classes.issubset(classes)

    def is_display_edit_icon(self, category_name: str) -> bool:
        category_box = WebDriverWait(self.__driver, self.__timeout).until(
            EC.visibility_of_element_located((
                By.XPATH,
                f'//span[text()="{category_name}"]/ancestor::div[contains(@class, "MuiBox-root")]'
            ))
        )
        try:
            edit_icon = category_box.find_element(By.CSS_SELECTOR, 'button[aria-label="Edit category"]')
            return edit_icon.is_displayed()
        except NoSuchElementException:
            return False

    def is_display_archive_icon(self, category_name: str) -> bool:
        category_box = WebDriverWait(self.__driver, self.__timeout).until(
            EC.visibility_of_element_located((
                By.XPATH,
                f'//span[text()="{category_name}"]/ancestor::div[contains(@class, "MuiBox-root")]'
            ))
        )
        try:
            archive_icon = category_box.find_element(By.CSS_SELECTOR, 'button[aria-label="Archive category"]')
            return archive_icon.is_displayed()
        except NoSuchElementException:
            return False

    def alert_on_action(self) -> str:
        alert = WebDriverWait(self.__driver, self.__timeout).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, 'div[role="alert"]'
            ))
        )
        return alert.text

