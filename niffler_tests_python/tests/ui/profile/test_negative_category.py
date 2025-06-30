import pytest
from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.tests.conftest import Pages
from niffler_tests_python.web_pages.HeaderPage import HeaderPage
from niffler_tests_python.web_pages.MainPage import MainPage
from niffler_tests_python.web_pages.ProfilePage import ProfilePage


@Pages.go_to_profile_page
def test_add_empty_category(profile_page: ProfilePage, category_client: CategoryApiClient):
   before_get_all_categories = category_client.get_all_categories()
   before_category_count = len(before_get_all_categories)

   profile_page.submit_add_empty_category()

   after_get_all_categories = category_client.get_all_categories()
   after_category_count = len(after_get_all_categories)

   assert before_category_count == after_category_count
   assert "Allowed category length is from 2 to 50 symbols" in profile_page.helper_text_empty_add_category()

@Pages.go_to_profile_page
@pytest.mark.parametrize("category_name", ["1"])
def test_add_category_invalid_value(
        category_name: str,
        category_client: CategoryApiClient,
        main_page: MainPage,
        header_page: HeaderPage,
        profile_page: ProfilePage,
):
   before_get_all_categories = category_client.get_all_categories()
   before_category_count = len(before_get_all_categories)

   profile_page.enter_add_category(category_name=category_name)
   profile_page.submit_add_category()

   helper_text = profile_page.helper_text_empty_add_category()

   after_get_all_categories = category_client.get_all_categories()
   after_category_count = len(after_get_all_categories)

   assert before_category_count == after_category_count
   assert "Allowed category length is from 2 to 50 symbols" in helper_text
