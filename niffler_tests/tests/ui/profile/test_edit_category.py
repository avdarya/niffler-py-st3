import dotenv
import os
from faker import Faker
from selenium.webdriver.ie.webdriver import WebDriver
from clients.categories_client import CategoriesApiClient
from configuration.ConfigProvider import ConfigProvider
from utils.helpers import login, wait_for_category_update_name
from web_pages.HeaderPage import HeaderPage
from web_pages.ProfilePage import ProfilePage

dotenv.load_dotenv()
user_login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")

fake = Faker()

def test_edit_category_by_icon(
        browser: WebDriver,
        config: ConfigProvider,
        add_category: dict,
        categories_client: CategoriesApiClient,
):
   auth_browser = login(driver=browser, login_url=config.get_ui_auth_url(), username=user_login, password=password)

   header_page = HeaderPage(driver=auth_browser)
   header_page.click_menu_button()
   header_page.click_profile()

   profile_page = ProfilePage(driver=auth_browser)

   category_name = add_category["name"]
   category_id = add_category["id"]
   new_category_name = fake.text(max_nb_chars=10).replace("\n", " ")

   profile_page.click_edit_category_icon()
   expected_text_input = profile_page.text_edit_category_input()

   profile_page.clear_edit_category_input()
   profile_page.enter_edit_category(category_name=new_category_name)
   profile_page.submit_edit_category()

   alert_text = profile_page.alert_on_action()

   updated_category = wait_for_category_update_name(categories_client=categories_client, category_id=category_id, expected_name=new_category_name)

   api_get_all_categories = categories_client.get_all_categories()
   assert api_get_all_categories.status_code == 200
   body = api_get_all_categories.json()
   for category in body:
      if category["id"] == category_id:
         assert category["name"] == new_category_name
         assert category["archived"] is False

   assert expected_text_input == category_name
   assert "Category name is changed" in alert_text
   assert profile_page.invisible_category_chip(category_name=new_category_name) is False
   assert updated_category["archived"] is False

def test_cancel_edit_category(
        browser: WebDriver,
        config: ConfigProvider,
        add_category: dict,
        categories_client: CategoriesApiClient,
):
   auth_browser = login(driver=browser, login_url=config.get_ui_auth_url(), username=user_login, password=password)

   header_page = HeaderPage(driver=auth_browser)
   header_page.click_menu_button()
   header_page.click_profile()

   profile_page = ProfilePage(driver=auth_browser)

   category_name = add_category["name"]
   category_id = add_category["id"]

   profile_page.click_category_chip(category_name=category_name)
   profile_page.click_close_edit_category()

   is_category_chip_present = profile_page.invisible_category_chip(category_name=category_name)

   api_category = wait_for_category_update_name(categories_client=categories_client, category_id=category_id, expected_name=category_name)

   assert is_category_chip_present is False
   assert api_category["archived"] is False
