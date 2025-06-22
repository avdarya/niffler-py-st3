import dotenv
import os
from faker import Faker
from selenium.webdriver.ie.webdriver import WebDriver
from clients.categories_client import CategoriesApiClient
from configuration.ConfigProvider import ConfigProvider
from tests.conftest import update_category
from utils.helpers import login
from web_pages.HeaderPage import HeaderPage
from web_pages.ProfilePage import ProfilePage

dotenv.load_dotenv()
user_login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")

fake = Faker()

def test_add_category(
        browser: WebDriver,
        config: ConfigProvider,
        categories_client: CategoriesApiClient,
        update_category: dict
):
   auth_browser = login(driver=browser, login_url=config.get_ui_auth_url(), username=user_login, password=password)

   header_page = HeaderPage(driver=auth_browser)
   header_page.click_menu_button()
   header_page.click_profile()

   profile_page = ProfilePage(driver=auth_browser)

   category_name = fake.text(max_nb_chars=20).replace("\n", " ")

   profile_page.enter_add_category(category_name=category_name)
   profile_page.submit_add_category()

   alert_text = profile_page.alert_on_action()

   api_get_all_categories = categories_client.get_all_categories()
   assert api_get_all_categories.status_code == 200
   body = api_get_all_categories.json()
   api_category_name = None
   api_category_id = None
   api_category_archived = None
   for category in body:
      if category["name"] == category_name:
         api_category_name = category["name"]
         api_category_id = category["id"]
         api_category_archived = category["archived"]

   update_category["name"] = category_name
   update_category["id"] = api_category_id
   update_category["archived"] = True

   assert category_name == api_category_name
   assert api_category_archived is False
   assert f"You've added new category: {category_name}" in alert_text
   assert profile_page.is_input_cleared()
   assert profile_page.invisible_category_chip(category_name=category_name) is False