import os
import dotenv
from faker import Faker
from selenium.webdriver.ie.webdriver import WebDriver
from configuration.ConfigProvider import ConfigProvider
from utils.helpers import login
from web_pages.HeaderPage import HeaderPage
from web_pages.SpendingPage import SpendingPage

dotenv.load_dotenv()
user_login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")

fake = Faker()

def test_add_empty_spend(browser: WebDriver, config: ConfigProvider, add_spending: dict):
    auth_browser = login(driver=browser, login_url=config.get_ui_auth_url(), username=user_login, password=password)

    spending_page = SpendingPage(driver=auth_browser)
    header_page = HeaderPage(driver=auth_browser)

    header_page.click_new_spending()

    spending_page.click_save_spend()

    helper_text_amount = spending_page.helper_text_amount_input()
    helper_text_category = spending_page.helper_text_category_input()

    assert "Amount has to be not less then 0.01" in helper_text_amount
    assert "Please choose category" in helper_text_category