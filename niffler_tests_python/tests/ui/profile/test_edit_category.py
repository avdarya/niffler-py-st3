import allure
import pytest

from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.category import CategoryModel
from niffler_tests_python.tests.conftest import Pages, TestData
from niffler_tests_python.utils.helpers import wait_for_category_update_name
from niffler_tests_python.web_pages.ProfilePage import ProfilePage


@allure.epic('Spending management')
@allure.feature('Category updating')
@allure.story('Edit category by icon')
@Pages.go_to_profile_after_category
@TestData.category("category for edit")
@pytest.mark.parametrize("new_category_name", ["updated category"])
def test_edit_category_by_icon(
        profile_page: ProfilePage,
        category: CategoryModel,
        category_client: CategoryApiClient,
        spend_db: SpendDB,
        new_category_name: str
):
   with allure.step('Click edit icon'):
      profile_page.click_edit_category_icon(category_name=category.name)

   with allure.step('Save edit category input text'):
      expected_text_input = profile_page.get_text_edit_category_input()

   with allure.step('Enter and submit edited category'):
      profile_page.clear_edit_category_input()
      profile_page.enter_edit_category(category_name=new_category_name)
      profile_page.submit_edit_category()

   with allure.step('Save alert dialog'):
      alert_text = profile_page.alert_on_action()

   with allure.step('Retrieve edited category form API and verify category name, archived'):
      wait_for_category_update_name(
         categories_client=category_client,
         category_id=category.id,
         expected_name=new_category_name
      )

   with allure.step('Retrieve edited category in DB'):
      db_category = spend_db.get_category_by_name(new_category_name)

   with allure.step('Assert edit category'):
      with allure.step('Verify edited category input contains expected category name'):
         assert expected_text_input == category.name
      with allure.step('Verify alert text'):
         assert "Category name is changed" in alert_text
      with allure.step('Edited category is visible in UI'):
         assert profile_page.invisible_category_chip(category_name=new_category_name) is False
      with allure.step('Verify edited category name in DB'):
         assert db_category.name == new_category_name
      with allure.step('Verify edited category archived in DB'):
         assert db_category.archived is False

@allure.epic('Spending management')
@allure.feature('Category updating')
@allure.story('Cancel edit category')
@Pages.go_to_profile_after_category
@TestData.category("category for cancel edit")
def test_cancel_edit_category(
        profile_page: ProfilePage,
        category: CategoryModel,
        category_client: CategoryApiClient,
        spend_db: SpendDB
):
   with allure.step('Click category chip'):
      profile_page.click_category_chip(category_name=category.name)

   with allure.step('Click close icon'):
      profile_page.click_close_edit_category()

   with allure.step('Find category chip in UI'):
      is_category_chip_present = profile_page.invisible_category_chip(category_name=category.name)

   with allure.step('Save edited category from API'):
      api_category = wait_for_category_update_name(
         categories_client=category_client,
         category_id=category.id,
         expected_name=category.name
      )

   with allure.step('Retrieve edited category in DB'):
      db_category = spend_db.get_category_by_name(category.name)

   with allure.step('Assert edit category'):
      with allure.step('Verify category chip in UI'):
         assert is_category_chip_present is False
      with allure.step('Verify category archived in API'):
         assert api_category.archived is False
      with allure.step('Verify category name in DB'):
         assert db_category.name == category.name
      with allure.step('Verify category archived in DB'):
         assert db_category.archived == category.archived
