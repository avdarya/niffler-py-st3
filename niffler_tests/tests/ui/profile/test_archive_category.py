import dotenv
import os
from faker import Faker
from selenium.webdriver.ie.webdriver import WebDriver
from clients.categories_client import CategoriesApiClient
from configuration.ConfigProvider import ConfigProvider
from utils.helpers import login, wait_for_category_update_archive
from web_pages.HeaderPage import HeaderPage
from web_pages.ProfilePage import ProfilePage

dotenv.load_dotenv()
user_login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")

fake = Faker()

def test_archive_category(
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
   profile_page.click_archive_category_icon(category_name=category_name)

   text_alert_archive = profile_page.text_alert_archive()

   profile_page.click_archive_category_button()

   alert_text = profile_page.alert_on_action()

   wait_for_category_update_archive(
      categories_client=categories_client,
      category_id=category_id,
      expected_archive=True
   )

   assert category_name in text_alert_archive
   assert category_name in alert_text
   assert profile_page.invisible_category_chip(category_name=category_name) is True

