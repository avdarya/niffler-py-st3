import allure
import pytest

from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.category import CategoryModel
from niffler_tests_python.utils.marks import Pages, TestData
from niffler_tests_python.utils.helpers import wait_for_category_update_name, wait_for_category_update_archive
from niffler_tests_python.web_pages.ProfilePage import ProfilePage


@allure.epic('Spending management')
@allure.feature('Category updating')
@allure.story('Edit category by icon')
@Pages.go_to_profile_after_category
@TestData.category("category for edit")
@pytest.mark.parametrize("new_category_name", ["updated category"])
def test_edit_category_name_by_icon(
        profile_page: ProfilePage,
        category: CategoryModel,
        category_client: CategoryApiClient,
        spend_db: SpendDB,
        new_category_name: str
):
   with allure.step('Click edit icon'):
      profile_page.click_edit_category_icon(category.name)

   with allure.step('Verify edited category input contains expected category name'):
       profile_page.expected_text_edit_category_input(category.name)

   with allure.step('Enter and submit edited category'):
      profile_page.clear_edit_category_input()
      profile_page.enter_edit_category(new_category_name)

   with allure.step('Verify alert text'):
       profile_page.notification.is_success_notification()
       assert "Category name is changed" == profile_page.notification.get_notification_text()

   with allure.step('Retrieve edited category form API and verify category name, archived'):
      wait_for_category_update_name(
         category_client=category_client,
         category_id=category.id,
         expected_name=new_category_name
      )

   with allure.step('Retrieve edited category in DB'):
      db_category = spend_db.get_category_by_name(new_category_name)

   with allure.step('Assert edit category'):
      with allure.step('Verify edited category is visible in active categories'):
         profile_page.expected_active_category_chip(new_category_name)
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
      profile_page.click_category_chip(category.name)

   with allure.step('Click close icon'):
      profile_page.click_close_edit_category_button()

   with allure.step('Verify category chip in UI'):
      profile_page.expected_active_category_chip(category.name)

   with allure.step('Save edited category from API'):
      api_category = wait_for_category_update_name(
         category_client=category_client,
         category_id=category.id,
         expected_name=category.name
      )

   with allure.step('Retrieve edited category in DB'):
      db_category = spend_db.get_category_by_name(category.name)
   with allure.step('Assert edit category'):
      with allure.step('Verify category archived in API'):
         assert api_category.archived is False
      with allure.step('Verify category name in DB'):
         assert db_category.name == category.name
      with allure.step('Verify category archived in DB'):
         assert db_category.archived == category.archived

@allure.epic('Spending management')
@allure.feature('Category archiving')
@allure.story('Archive category')
@Pages.go_to_profile_after_category
@TestData.category("category for archive")
def test_archive_category(
        category: CategoryModel,
        profile_page: ProfilePage,
        category_client: CategoryApiClient,
        spend_db: SpendDB
):
   category_name = category.name
   category_id = category.id

   with allure.step('Click archive icon'):
      profile_page.click_archive_category_icon(category_name)

   with allure.step('Verify submit dialog title and description'):
      profile_page.expect_archive_popup(category_name)

   with allure.step('Submit archived category'):
      profile_page.click_archive_category_button()

   with allure.step('Verify category name in alert text'):
      profile_page.notification.is_success_notification()
      assert category_name in profile_page.notification.get_notification_text()

   with allure.step('Click show archived toggle button'):
      profile_page.click_show_archived()

   with allure.step('Verify category chip is invisible in UI'):
      profile_page.expected_archive_category_chip(category_name)

   with allure.step('Retrieve archived category from API'):
      wait_for_category_update_archive(
         category_client=category_client,
         category_id=category_id,
         expected_archive=True
      )

   with allure.step('Retrieve archived category in DB'):
      db_category = spend_db.get_category_by_name(category_name)
   with allure.step('Assert archived category'):

      with allure.step('Verify category in DB is archived'):
         assert db_category.archived is True

@allure.epic('Spending management')
@allure.feature('Category archiving')
@allure.story('Unarchive category')
@TestData.archive_category("category for unarchive")
def test_unarchive_category(
        profile_page: ProfilePage,
        archive_category: CategoryModel,
        go_to_profile_page: None,
        category_client: CategoryApiClient,
        spend_db: SpendDB
):
   category_name = archive_category.name
   category_id = archive_category.id

   with allure.step('Click show archived toggle button'):
      profile_page.click_show_archived()

   with allure.step('Click unarchive icon'):
      profile_page.click_unarchive_category_icon(category_name)

   with allure.step('Verify submit dialog title and description'):
      profile_page.expect_unarchive_popup(category_name)

   with allure.step('Submit unarchived category'):
      profile_page.click_unarchive_category_button()

   with allure.step('Verify category name in alert text'):
      profile_page.notification.is_success_notification()
      assert category_name in profile_page.notification.get_notification_text()

   with allure.step('Verify category chip is active in UI'):
      profile_page.expected_active_category_chip(category_name)

   with allure.step('Retrieve unarchived category from API'):
      wait_for_category_update_archive(
         category_client=category_client,
         category_id=category_id,
         expected_archive=False
      )

   with allure.step('Retrieve unarchived category in DB'):
      db_category = spend_db.get_category_by_name(category_name)

   with allure.step('Verify category in DB is unarchived'):
      assert db_category.archived is False
