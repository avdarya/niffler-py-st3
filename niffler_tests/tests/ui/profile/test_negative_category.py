import pytest
from niffler_tests.clients.category_client import CategoryApiClient
from niffler_tests.web_pages.HeaderPage import HeaderPage
from niffler_tests.web_pages.MainPage import MainPage
from niffler_tests.web_pages.ProfilePage import ProfilePage


def test_add_empty_category(
        profile_page: ProfilePage,
        go_to_profile_page: None,
        category_client: CategoryApiClient,
):
   before_get_all_categories = category_client.get_all_categories()
   assert before_get_all_categories.status_code == 200
   before_category_count = len(before_get_all_categories.json())

   profile_page.submit_add_empty_category()

   after_get_all_categories = category_client.get_all_categories()
   assert after_get_all_categories.status_code == 200
   after_category_count = len(after_get_all_categories.json())

   assert before_category_count == after_category_count
   assert "Allowed category length is from 2 to 50 symbols" in profile_page.helper_text_empty_add_category()

# @pytest.mark.skip("Check requirements")
@pytest.mark.parametrize("category_name", [
   "1",
   # "Example string that contains exact fifty-one chars."
])
def test_add_spend_invalid_value(
        category_name: str,
        category_client: CategoryApiClient,
        main_page: MainPage,
        header_page: HeaderPage,
        profile_page: ProfilePage,
):
   main_page.open()
   header_page.click_menu_button()
   header_page.click_profile()

   before_get_all_categories = category_client.get_all_categories()
   assert before_get_all_categories.status_code == 200
   before_category_count = len(before_get_all_categories.json())

   profile_page.enter_add_category(category_name=category_name)
   profile_page.submit_add_category()

   after_get_all_categories = category_client.get_all_categories()
   assert after_get_all_categories.status_code == 200
   after_category_count = len(after_get_all_categories.json())

   helper_text = profile_page.helper_text_empty_add_category()

   assert before_category_count == after_category_count
   assert "Allowed category length is from 2 to 50 symbols" in helper_text
