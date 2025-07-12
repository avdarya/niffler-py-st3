from time import sleep

import pytest

from selenium.webdriver.remote.webdriver import WebDriver

from niffler_tests_python.model.category import CategoryModel
from niffler_tests_python.model.spend import SpendModel
from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.web_pages.LoginPage import LoginPage
from niffler_tests_python.web_pages.MainPage import MainPage
from niffler_tests_python.web_pages.ProfilePage import ProfilePage
from niffler_tests_python.web_pages.SpendingPage import SpendingPage
from niffler_tests_python.web_pages.components.Header import Header


@pytest.fixture(scope='session')
def login_page(browser: WebDriver, server_cfg: ServerConfig) -> LoginPage:
    return LoginPage(driver=browser, server_cfg=server_cfg)

@pytest.fixture(scope='session')
def main_page(auth_browser: WebDriver, server_cfg: ServerConfig) -> MainPage:
    return MainPage(driver=auth_browser, server_cfg=server_cfg)

@pytest.fixture(scope='session')
def spending_page(auth_browser: WebDriver, server_cfg: ServerConfig) -> SpendingPage:
    return SpendingPage(driver=auth_browser, server_cfg=server_cfg)

@pytest.fixture(scope='session')
def profile_page(auth_browser: WebDriver, server_cfg: ServerConfig) -> ProfilePage:
    return ProfilePage(driver=auth_browser, server_cfg=server_cfg)

@pytest.fixture(scope='session')
def header(auth_browser: WebDriver, server_cfg: ServerConfig) -> Header:
    return Header(driver=auth_browser, server_cfg=server_cfg)

@pytest.fixture(scope='function')
def go_to_main_page(main_page: MainPage) -> None:
    main_page.open()

@pytest.fixture(scope='function')
def go_to_main_page_after_spend(main_page: MainPage, spend: SpendModel) -> None:
    main_page.open()

@pytest.fixture(scope='function')
def go_to_main_page_after_fill_spends(main_page: MainPage, fill_spends: SpendModel) -> None:
    main_page.open()

@pytest.fixture(scope='function')
def go_to_profile_page(main_page: MainPage, profile_page: ProfilePage, header: Header) -> None:
    main_page.open()
    header.click_menu_button()
    header.click_profile()

@pytest.fixture(scope='function')
def go_to_profile_after_category(
        main_page: MainPage,
        profile_page: ProfilePage,
        header: Header,
        category: CategoryModel
) -> None:
    sleep(2)
    main_page.open()
    header.click_menu_button()
    header.click_profile()
