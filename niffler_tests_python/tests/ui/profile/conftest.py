import pytest
from typing import Any
from collections.abc import Generator
from pytest import FixtureRequest
from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.databases.spend_db import SpendModelDB
from niffler_tests_python.model.category import CategoryModel
from niffler_tests_python.web_pages.components.Header import Header
from niffler_tests_python.web_pages.MainPage import MainPage
from niffler_tests_python.web_pages.ProfilePage import ProfilePage

@pytest.fixture
def archive_category(
        request: FixtureRequest,
        category_client: CategoryApiClient,
        spend_db: SpendModelDB
) -> Generator[CategoryModel, Any, None]:
    category_name = request.param
    api_current_categories = category_client.get_all_categories()
    current_categories = {category.name: category for category in api_current_categories}
    if category_name in current_categories:
        added_category = current_categories[category_name]
    else:
        added_category = category_client.add_category(category_name=category_name)
    added_category.archived = True
    archive_category = category_client.update_category(added_category)
    yield archive_category
    spend_db.delete_category(added_category.id)

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
    main_page.open()
    header.click_menu_button()
    header.click_profile()