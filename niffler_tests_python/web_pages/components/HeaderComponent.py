import allure
from playwright.sync_api import Page, expect
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.web_pages.BasePage import BasePage
from niffler_tests_python.web_pages.components.BaseComponent import BaseComponent
from niffler_tests_python.web_pages.locators.HeaderLocators import HeaderLocators


# class Header(BasePage):
#
#     def __init__(self, driver: WebDriver,  server_cfg: ServerConfig):
#         super().__init__(driver, server_cfg)
#         self.locator = HeaderLocators()
#
#     @allure.step('[UI header]')
#     def click_menu_button(self) -> None:
#         self._driver.find_element(*self.locator.MENU_BUTTON).click()
#
#     @allure.step('[UI header] Click profile button')
#     def click_profile(self) -> None:
#         self._driver.find_element(*self.locator.PROFILE_BUTTON).click()
#         self.wait_for(
#             self.locator.ACCOUNT_MENU,
#             EC.invisibility_of_element_located
#         )
#
#     @allure.step('[UI header] Click new spending button')
#     def click_new_spending(self) -> None:
#         self._driver.find_element(*self.locator.SPENDING_BUTTON).click()

class HeaderComponent(BaseComponent):

    def __init__(self, page: Page,  server_cfg: ServerConfig):
        super().__init__(page, server_cfg)
        self.locators = HeaderLocators



    # @allure.step('[UI header]')
    # def click_menu_button(self) -> None:
    #     self._driver.find_element(*self.locator.MENU_BUTTON).click()
    #
    # @allure.step('[UI header] Click profile button')
    # def click_profile(self) -> None:
    #     self._driver.find_element(*self.locator.PROFILE_BUTTON).click()
    #     self.wait_for(
    #         self.locator.ACCOUNT_MENU,
    #         EC.invisibility_of_element_located
    #     )
    #
    @allure.step('[UI header] Click new spending button')
    def click_new_spending(self) -> None:
        self.locators.spending_button(self._page).click()

    @allure.step('[UI header] Проверка видимости кнопки профиля')
    def is_visible_person_icon(self):
        expect(self.locators.person_icon(self._page)).to_be_visible()

    def click_person_icon(self) -> None:
        self.locators.person_icon(self._page).click()

    def click_profile_button(self) -> None:
        self.locators.profile_button(self._page).click()

    def click_friends_button(self) -> None:
        self.locators.friends_button(self._page).click()

    def click_all_people(self) -> None:
        self.locators.all_people_button(self._page).click()

