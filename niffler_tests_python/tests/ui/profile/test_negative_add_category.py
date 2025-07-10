import allure
import pytest
from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.tests.conftest import Pages
from niffler_tests_python.web_pages.components.Header import Header
from niffler_tests_python.web_pages.MainPage import MainPage
from niffler_tests_python.web_pages.ProfilePage import ProfilePage


@allure.epic('Spending management')
@allure.feature('Category creation')
@allure.story('Add empty category')
@Pages.go_to_profile_page
def test_add_empty_category(profile_page: ProfilePage, category_client: CategoryApiClient):
   with allure.step('Retrieve category count before'):
      before_get_all_categories = category_client.get_all_categories()
      before_category_count = len(before_get_all_categories)

   profile_page.submit_add_category()

   with allure.step('Retrieve category count after'):
      after_get_all_categories = category_client.get_all_categories()
      after_category_count = len(after_get_all_categories)

   with allure.step('Assert add empty category'):
      with allure.step('Category count after = category count before'):
         assert before_category_count == after_category_count
      with allure.step('Verify helper text for category input'):
         assert "Allowed category length is from 2 to 50 symbols" in profile_page.helper_text_empty_add_category()

@allure.epic('Spending management')
@allure.feature('Category creation')
@allure.story('Add category with invalid value')
@Pages.go_to_profile_page
@pytest.mark.parametrize("category_name", ["1"])
def test_add_category_invalid_value(
        category_name: str,
        category_client: CategoryApiClient,
        main_page: MainPage,
        header: Header,
        profile_page: ProfilePage,
):
   with allure.step('Retrieve category count before'):
      before_get_all_categories = category_client.get_all_categories()
      before_category_count = len(before_get_all_categories)

   with allure.step('Enter and submit new category with invalid value'):
      profile_page.enter_add_category(category_name=category_name)
      profile_page.submit_add_category()

   with allure.step('Save helper text'):
      helper_text = profile_page.helper_text_empty_add_category()

   with allure.step('Retrieve category count after'):
      after_get_all_categories = category_client.get_all_categories()
      after_category_count = len(after_get_all_categories)

   with allure.step('Assert add category with invalid value'):
      with allure.step('Category count after = category count before'):
         assert before_category_count == after_category_count
      with allure.step('Verify helper text for category input'):
         assert "Allowed category length is from 2 to 50 symbols" in helper_text
