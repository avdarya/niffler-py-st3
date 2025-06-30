import pytest

from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.category import CategoryModel
from niffler_tests_python.tests.conftest import Pages, TestData
from niffler_tests_python.utils.helpers import wait_for_category_update_name
from niffler_tests_python.web_pages.ProfilePage import ProfilePage


@Pages.go_to_profile_after_category
@TestData.category("category for edit")
@pytest.mark.parametrize("new_category_name", ["updated_category"])
def test_edit_category_by_icon(
        profile_page: ProfilePage,
        category: CategoryModel,
        category_client: CategoryApiClient,
        spend_db: SpendDB,
        new_category_name: str
):
   profile_page.click_edit_category_icon(category_name=category.name)
   expected_text_input = profile_page.text_edit_category_input()
   profile_page.clear_edit_category_input()
   profile_page.enter_edit_category(category_name=new_category_name)
   profile_page.submit_edit_category()
   alert_text = profile_page.alert_on_action()

   updated_category = wait_for_category_update_name(
      categories_client=category_client,
      category_id=category.id,
      expected_name=new_category_name
   )

   api_get_all_categories = category_client.get_all_categories()
   for category_item in api_get_all_categories:
      if category_item.id == category.id:
         assert category_item.name == new_category_name
         assert category_item.archived is False

   db_category = spend_db.get_category_by_name(new_category_name)

   assert expected_text_input == category.name
   assert "Category name is changed" in alert_text
   assert profile_page.invisible_category_chip(category_name=new_category_name) is False
   assert updated_category.archived is False
   assert db_category.name == new_category_name
   assert db_category.archived is False

@Pages.go_to_profile_after_category
@TestData.category("category for cancel edit")
def test_cancel_edit_category(
        profile_page: ProfilePage,
        category: CategoryModel,
        category_client: CategoryApiClient,
        spend_db: SpendDB
):
   profile_page.click_category_chip(category_name=category.name)
   profile_page.click_close_edit_category()
   is_category_chip_present = profile_page.invisible_category_chip(category_name=category.name)

   api_category = wait_for_category_update_name(
      categories_client=category_client,
      category_id=category.id,
      expected_name=category.name
   )

   db_category = spend_db.get_category_by_name(category.name)

   assert is_category_chip_present is False
   assert api_category.archived is False
   assert db_category.name == category.name
   assert db_category.archived == category.archived
