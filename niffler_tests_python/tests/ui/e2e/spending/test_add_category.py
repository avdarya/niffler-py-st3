import allure
import pytest

from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.utils.marks import Pages
from niffler_tests_python.utils.helpers import get_category_by_name
from niffler_tests_python.web_pages.ProfilePage import ProfilePage


@allure.epic('Spending management')
@allure.feature('Category creation')
@allure.story('Add category')
@Pages.go_to_profile_page
@pytest.mark.parametrize("category_name", ["added category"])
def test_add_category(
        profile_page: ProfilePage,
        category_client: CategoryApiClient,
        spend_db: SpendDB,
        category_name: str
):
   with allure.step('Fill and submit new category'):
      profile_page.enter_add_category(category_name)

   with allure.step('Verify alert text'):
      profile_page.notification.is_success_notification()
      assert f"You've added new category: {category_name}" == profile_page.notification.get_notification_text()

   with allure.step('Retrieve all categories from API and search added category'):
      api_category = get_category_by_name(category_name, category_client)

   with allure.step('Retrieve added category in DB'):
      db_category = spend_db.get_category_by_name(name=category_name)
      with allure.step('Delete added category'):
         spend_db.delete_category(db_category.id)

   with allure.step('Assert add category'):
      with allure.step('Added category from API is not archived'):
         assert api_category.archived is False
      with allure.step('Verify cleared input after adding category'):
         profile_page.expected_add_input_empty()
      with allure.step('Verify added category is visible in UI'):
         profile_page.expected_active_category_chip(category_name)
      with allure.step('Verify added category name in DB matches input'):
         assert db_category.name == category_name
      with allure.step('Verify added category in DB is not archived'):
         assert db_category.archived is False