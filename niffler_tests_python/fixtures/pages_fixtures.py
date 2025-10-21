from time import sleep

import pytest
from playwright.sync_api import Page
from typing import Callable, Any, Generator

from selenium.webdriver.remote.webdriver import WebDriver
from playwright.sync_api import Page, Browser, sync_playwright
from niffler_tests_python.model.category import CategoryModel
from niffler_tests_python.model.spend import SpendModel
from niffler_tests_python.model.userdata import UserFriendshipModel, UserModelDB
from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.web_pages.LoginPage import LoginPage
from niffler_tests_python.web_pages.MainPage import MainPage
from niffler_tests_python.web_pages.PeopleAllPage import PeopleAllPage
from niffler_tests_python.web_pages.PeopleFriendsPage import PeopleFriendsPage
from niffler_tests_python.web_pages.ProfilePage import ProfilePage
from niffler_tests_python.web_pages.RegisterPage import RegisterPage
from niffler_tests_python.web_pages.SpendingPage import SpendingPage
from niffler_tests_python.web_pages.components.HeaderComponent import HeaderComponent


@pytest.fixture
def register_page(page_not_authed: Page, server_cfg: ServerConfig) -> RegisterPage:
    return RegisterPage(page_not_authed, server_cfg)

@pytest.fixture
def login_page(page_not_authed: Page, server_cfg: ServerConfig) -> LoginPage:
    return LoginPage(page_not_authed, server_cfg)

@pytest.fixture
def main_page_guest(page_not_authed: Page, server_cfg: ServerConfig) -> MainPage:
    return MainPage(page_not_authed, server_cfg)

@pytest.fixture
def main_page(page_authed: Page, server_cfg: ServerConfig) -> MainPage:
    return MainPage(page_authed, server_cfg)

@pytest.fixture
def spending_page(page_authed: Page, server_cfg: ServerConfig) -> SpendingPage:
    return SpendingPage(page_authed, server_cfg)

@pytest.fixture
def profile_page(page_authed: Page, server_cfg: ServerConfig) -> ProfilePage:
    return ProfilePage(page_authed, server_cfg)

@pytest.fixture
def people_all_page(page_authed: Page, server_cfg: ServerConfig) -> PeopleAllPage:
    return PeopleAllPage(page_authed, server_cfg)

@pytest.fixture
def people_friends_page(page_authed: Page, server_cfg: ServerConfig) -> PeopleFriendsPage:
    return PeopleFriendsPage(page_authed, server_cfg)

@pytest.fixture
def header_page_guest(page_not_authed: Page, server_cfg: ServerConfig) -> HeaderComponent:
    return HeaderComponent(page_not_authed, server_cfg)

@pytest.fixture
def header(page_authed: Page, server_cfg: ServerConfig) -> HeaderComponent:
    return HeaderComponent(page_authed, server_cfg)

@pytest.fixture
def go_to_main_page(main_page: MainPage) -> None:
    main_page.navigate()

@pytest.fixture
def go_to_main_page_after_spend(main_page: MainPage, spend: SpendModel) -> None:
    main_page.navigate()

@pytest.fixture
def go_to_main_page_after_fill_spends(main_page: MainPage, fill_spends: SpendModel) -> None:
    main_page.navigate()

@pytest.fixture
def go_to_profile_page(main_page: MainPage, profile_page: ProfilePage, header: HeaderComponent) -> None:
    main_page.navigate()
    header.click_person_icon()
    header.click_profile_button()

@pytest.fixture
def go_to_people_all_after_people(
        main_page: MainPage,
        header: HeaderComponent,
        register_new_user: tuple[str, str]
) -> None:
    main_page.navigate()
    header.click_person_icon()
    header.click_all_people()

@pytest.fixture
def go_to_people_friends_after_send(
        main_page: MainPage,
        header: HeaderComponent,
        sending_invitation: None
) -> None:
    main_page.navigate()
    header.click_person_icon()
    header.click_friends_button()

@pytest.fixture
def go_to_people_friends_after_accept(
        main_page: MainPage,
        profile_page: ProfilePage,
        header: HeaderComponent,
        accept_invitation: None
) -> None:
    main_page.navigate()
    header.click_person_icon()
    header.click_friends_button()

@pytest.fixture
def go_to_people_all_after_list_people(
        main_page: MainPage,
        profile_page: ProfilePage,
        header: HeaderComponent,
        people_list: list[UserModelDB]
) -> None:
    main_page.navigate()
    header.click_person_icon()
    header.click_all_people()

@pytest.fixture
def go_to_people_friends_after_list_friend(
        main_page: MainPage,
        profile_page: ProfilePage,
        header: HeaderComponent,
        friend_list: list[UserModelDB]
) -> None:
    main_page.navigate()
    header.click_person_icon()
    header.click_friends_button()

@pytest.fixture
def go_to_profile_after_category(
        main_page: MainPage,
        profile_page: ProfilePage,
        header: HeaderComponent,
        category: CategoryModel
) -> None:
    main_page.navigate()
    header.click_person_icon()
    header.click_profile_button()

