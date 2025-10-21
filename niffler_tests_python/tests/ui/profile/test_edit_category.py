import allure
import pytest

from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.category import CategoryModel
from niffler_tests_python.utils.marks import Pages, TestData
from niffler_tests_python.utils.helpers import wait_for_category_update_name, wait_for_category_update_archive
from niffler_tests_python.web_pages.ProfilePage import ProfilePage


@allure.epic("Траты")
@allure.feature("Редактирование категории")
@allure.story("UI")
@allure.tag("positive")
@allure.title("Редактирование названия категории через иконку")
@Pages.go_to_profile_after_category
@TestData.category("category for edit")
@pytest.mark.parametrize("new_category_name", ["updated category"])
def test_edit_category_name_by_icon(
        user: tuple[str, str],
        profile_page: ProfilePage,
        category: CategoryModel,
        category_client: CategoryApiClient,
        spend_db: SpendDB,
        new_category_name: str
):
   with allure.step("Нажимаем на иконку редактирования категории"):
      profile_page.click_edit_category_icon(category.name)

   with allure.step("Проверяем, что поле редактирования заполнено текущим именем категории"):
       profile_page.expected_text_edit_category_input(category.name)

   with allure.step("Очищаем поле и вводим новое название категории"):
      profile_page.clear_edit_category_input()
      profile_page.enter_edit_category(new_category_name)

   with allure.step("Проверяем уведомление об успешном изменении"):
       profile_page.notification.is_success_notification()
       assert "Category name is changed" == profile_page.notification.get_notification_text()

   with allure.step("Проверяем обновлённые данные категории через API и базу данных"):
      wait_for_category_update_name(
         category_client=category_client,
         category_id=category.id,
         expected_name=new_category_name
      )
      db_category = spend_db.get_user_category_by_name(user[0], new_category_name)
      profile_page.expected_active_category_chip(new_category_name)
      assert db_category.name == new_category_name
      assert db_category.archived is False

@allure.epic("Траты")
@allure.feature("Редактирование категории")
@allure.story("UI")
@allure.tag("negative")
@allure.title("Отмена редактирования категории")
@Pages.go_to_profile_after_category
@TestData.category("category for cancel edit")
def test_cancel_edit_category(
        user: tuple[str, str],
        profile_page: ProfilePage,
        category: CategoryModel,
        category_client: CategoryApiClient,
        spend_db: SpendDB
):
   with allure.step("Нажимаем на категорию для редактирования"):
      profile_page.click_category_chip(category.name)

   with allure.step("Отмена редактирования категории (крестик)"):
      profile_page.click_close_edit_category_button()

   with allure.step("Проверяем, что категория осталась без изменений в UI"):
      profile_page.expected_active_category_chip(category.name)

   with allure.step("Проверяем, что категория не изменилась через API и БД"):
      api_category = wait_for_category_update_name(
         category_client=category_client,
         category_id=category.id,
         expected_name=category.name
      )
      db_category = spend_db.get_user_category_by_name(user[0], category.name)
      assert api_category.archived is False
      assert db_category.name == category.name
      assert db_category.archived == category.archived

@allure.epic("Траты")
@allure.feature("Архивация категории")
@allure.story("UI")
@allure.tag("positive")
@allure.title("Архивация категории через интерфейс")
@Pages.go_to_profile_after_category
@TestData.category("category for archive")
def test_archive_category(
        user: tuple[str, str],
        category: CategoryModel,
        profile_page: ProfilePage,
        category_client: CategoryApiClient,
        spend_db: SpendDB
):
   category_name = category.name
   category_id = category.id
   with allure.step("Открываем диалог подтверждения архивации"):
      profile_page.click_archive_category_icon(category_name)
      profile_page.expect_archive_popup(category_name)

   with allure.step("Подтверждаем архивацию"):
      profile_page.click_archive_category_button()
      profile_page.notification.is_success_notification()
      assert category_name in profile_page.notification.get_notification_text()

   with allure.step("Проверяем, что категория скрыта в активных и отображается в архивных"):
      profile_page.click_show_archived()
      profile_page.expected_archive_category_chip(category_name)

   with allure.step("Проверяем, что категория заархивирована через API и БД"):
      wait_for_category_update_archive(
         category_client=category_client,
         category_id=category_id,
         expected_archive=True
      )
      db_category = spend_db.get_user_category_by_name(user[0], category_name)
      assert db_category.archived is True

@allure.epic("Траты")
@allure.feature("Архивация категории")
@allure.story("UI")
@allure.tag("positive")
@allure.title("Разархивация категории через интерфейс")
@TestData.archive_category("category for unarchive")
def test_unarchive_category(
        user: tuple[str, str],
        profile_page: ProfilePage,
        archive_category: CategoryModel,
        go_to_profile_page: None,
        category_client: CategoryApiClient,
        spend_db: SpendDB
):
   category_name = archive_category.name
   category_id = archive_category.id
   with allure.step("Открываем список архивных категорий"):
      profile_page.click_show_archived()

   with allure.step("Разархивируем категорию"):
      profile_page.click_unarchive_category_icon(category_name)
      profile_page.expect_unarchive_popup(category_name)
      profile_page.click_unarchive_category_button()

   with allure.step("Проверяем уведомление и отображение категории в активных"):
      profile_page.notification.is_success_notification()
      assert category_name in profile_page.notification.get_notification_text()
      profile_page.expected_active_category_chip(category_name)

   with allure.step("Проверяем, что категория не архивная через API и БД"):
      wait_for_category_update_archive(
         category_client=category_client,
         category_id=category_id,
         expected_archive=False
      )
      db_category = spend_db.get_user_category_by_name(user[0], category_name)
      assert db_category.archived is False
