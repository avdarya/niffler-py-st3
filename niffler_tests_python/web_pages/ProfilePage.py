import allure
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver

from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.web_pages.BasePage import BasePage
from niffler_tests_python.web_pages.locators.ProfilePageLocators import ProfilePageLocators


class ProfilePage(BasePage):

    def __init__(self, driver: WebDriver,  server_cfg: ServerConfig):
        super().__init__(driver, server_cfg)
        self.locator = ProfilePageLocators()

    @allure.step('[UI /profile] Fill add category input: category_name={category_name}')
    def enter_add_category(self, category_name: str) -> None:
        self._driver.find_element(*self.locator.ADD_CATEGORY_INPUT).send_keys(category_name)

    @allure.step('[UI /profile] Fill edit category input: category_name={category_name}')
    def enter_edit_category(self, category_name: str) -> None:
        self._driver.find_element(*self.locator.EDIT_CATEGORY_INPUT).send_keys(category_name)

    @allure.step('[UI /profile] Fill fullname input: name={name}')
    def enter_name(self, name: str) -> None:
        name_input = self._driver.find_element(*self.locator.FULLNAME_INTPUT)
        name_input.send_keys(name)

    @allure.step('[UI /profile] Submit add category input')
    def submit_add_category(self) -> None:
        self._driver.find_element(*self.locator.ADD_CATEGORY_INPUT).send_keys(Keys.ENTER)

    @allure.step('[UI /profile] Submit edit category input')
    def submit_edit_category(self) -> None:
        self._driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Edit category"]').send_keys(Keys.ENTER)

    @allure.step('[UI /profile] Get count invisible category chips: category_name={category_name}')
    def invisible_category_chip(self, category_name: str) -> bool:
        chips = self._driver.find_elements(
            self.locator.CATEGORY_CHIP_BY_NAME[0],
            self.locator.CATEGORY_CHIP_BY_NAME[1].format(category_name),
        )
        return len(chips) == 0

    @allure.step('[UI /profile] Check cleared add category input')
    def is_add_input_cleared(self) -> bool:
        category_input = self._driver.find_element(*self.locator.ADD_CATEGORY_INPUT)
        value = category_input.get_attribute("value")
        return value == ""

    @allure.step('[UI /profile] Click edit category icon: category_name={category_name}')
    def click_edit_category_icon(self, category_name: str) -> None:
        category_box = self.wait_for(
            (self.locator.CATEGORY_BOX[0],
            self.locator.CATEGORY_BOX[1].format(category_name)),
            EC.visibility_of_element_located
        )
        edit_icon = category_box.find_element(*self.locator.EDIT_ICON)
        edit_icon.click()

    @allure.step('[UI /profile] Click category chip: category_name={category_name}')
    def click_category_chip(self, category_name: str) -> None:
        self.wait_for(self.locator.CATEGORY_CHIP,  EC.visibility_of_any_elements_located)
        chips = self._driver.find_elements(*self.locator.CATEGORY_CHIP)
        for chip in chips:
            if chip.text == category_name:
                chip.click()

    @allure.step('[UI /profile] Click close edit category')
    def click_close_edit_category(self) -> None:

        self.wait_for(self.locator.CLOSE_ICON, EC.visibility_of_element_located)
        self._driver.find_element(*self.locator.CLOSE_ICON).click()

    @allure.step('[UI /profile] Click archive category icon: category_name={category_name}')
    def click_archive_category_icon(self, category_name: str) -> None:
        category_box = self.wait_for(
            (self.locator.CATEGORY_BOX[0],
            self.locator.CATEGORY_BOX[1].format(category_name)),
            EC.visibility_of_element_located
        )
        archive_icon = category_box.find_element(*self.locator.ARCHIVE_ICON)
        archive_icon.click()

    @allure.step('[UI /profile] Click unarchive category icon: category_name={category_name}')
    def click_unarchive_category_icon(self, category_name: str) -> None:
        category_box = self.wait_for(
            (self.locator.CATEGORY_BOX[0],
            self.locator.CATEGORY_BOX[1].format(category_name)),
            EC.visibility_of_element_located
        )
        unarchive_icon = category_box.find_element(*self.locator.UNARCHIVE_ICON)
        unarchive_icon.click()

    @allure.step('[UI /profile] Click submit archive category button')
    def click_archive_category_button(self) -> None:
        self._driver.find_element(*self.locator.SUBMIT_ARCHIVE_BUTTON).click()

    @allure.step('[UI /profile] Click submit unarchive category button')
    def click_unarchive_category_button(self) -> None:
        self.wait_for(self.locator.SUBMIT_UNARCHIVE_BUTTON, EC.visibility_of_element_located)
        self._driver.find_element(*self.locator.SUBMIT_UNARCHIVE_BUTTON).click()

    @allure.step('[UI /profile] Click save changes button')
    def click_save_changes(self) -> None:
        self._driver.find_element(*self.locator.SAVE_CHANGES_BUTTON).click()

    @allure.step('[UI /profile] Click show archived toggle button')
    def click_show_archived(self) -> None:
        self._driver.find_element(*self.locator.SHOW_ARCHIVED_BUTTON).click()

    @allure.step('[UI /profile] Get text edit category input')
    def get_text_edit_category_input(self) -> str:
        category_input =  self._driver.find_element(*self.locator.EDIT_CATEGORY_INPUT)
        return category_input.get_attribute("value")

    @allure.step('[UI /profile] Get description from submit popup')
    def submit_dialog_description(self) -> str:
        submit_dialog = self.wait_for(self.locator.SUBMIT_POPUP, EC.visibility_of_element_located)
        submit_dialog_description = submit_dialog.find_element(*self.locator.POPUP_DESCRIPTION)
        return submit_dialog_description.text

    @allure.step('[UI /profile] Get title from submit popup')
    def submit_dialog_title(self) -> str:
        submit_dialog = self.wait_for(self.locator.SUBMIT_POPUP, EC.visibility_of_element_located)
        submit_dialog_title = submit_dialog.find_element(*self.locator.POPUP_TITLE)
        return submit_dialog_title.text

    @allure.step('[UI /profile] Clear edit category input')
    def clear_edit_category_input(self) -> None:
        self._driver.find_element(*self.locator.EDIT_CATEGORY_INPUT).clear()

    @allure.step('[UI /profile] Clear fullname input')
    def clear_name_input(self) -> None:
        self._driver.find_element(*self.locator.FULLNAME_INTPUT).clear()

    @allure.step('[UI /profile] Get helper text for add category input')
    def helper_text_empty_add_category(self) -> str:
        element = self._driver.find_element(*self.locator.ADD_CATEGORY_HELPER_TEXT)
        return element.text

    @allure.step('[UI /profile] Check archiving category chip')
    def is_active_category_chip(self, category_name: str) -> bool:
        category_box = self.wait_for(
            (self.locator.CATEGORY_BOX[0],
            self.locator.CATEGORY_BOX[1].format(category_name)),
            EC.visibility_of_element_located
        )
        category_chip = category_box.find_element(*self.locator.CATEGORY_CHIP)
        classes = set(category_chip.get_attribute('class').split(' '))
        required_classes = {'MuiChip-colorPrimary'}
        return required_classes.issubset(classes)

    @allure.step('[UI /profile] Check display edit icon: category_name={category_name}')
    def is_display_edit_icon(self, category_name: str) -> bool:
        category_box = self.wait_for(
            (self.locator.CATEGORY_BOX[0],
            self.locator.CATEGORY_BOX[1].format(category_name)),
            EC.visibility_of_element_located
        )
        try:
            edit_icon = category_box.find_element(*self.locator.EDIT_ICON)
            return edit_icon.is_displayed()
        except NoSuchElementException:
            return False

    @allure.step('[UI /profile] Check display archive icon: category_name={category_name}')
    def is_display_archive_icon(self, category_name: str) -> bool:
        category_box = self.wait_for(
            (self.locator.CATEGORY_BOX[0],
            self.locator.CATEGORY_BOX[1].format(category_name)),
            EC.visibility_of_element_located
        )
        try:
            archive_icon = category_box.find_element(*self.locator.ARCHIVE_ICON)
            return archive_icon.is_displayed()
        except NoSuchElementException:
            return False

    @allure.step('[UI /profile] Get alert text')
    def alert_on_action(self) -> str:
        alert = self.wait_for(self.locator.ALERT_DIALOG)
        return alert.text
