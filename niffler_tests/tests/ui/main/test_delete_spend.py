import os
import dotenv
from datetime import datetime
from faker import Faker
from selenium.webdriver.ie.webdriver import WebDriver
from clients.spend_client import SpendApiClient
from configuration.ConfigProvider import ConfigProvider
from utils.helpers import login
from web_pages.MainPage import MainPage

dotenv.load_dotenv()
user_login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")

fake = Faker()

def test_delete_spending_by_one(
        browser: WebDriver,
        config: ConfigProvider,
        add_spending: dict,
        spend_client: SpendApiClient,
):
    auth_browser = login(driver=browser, login_url=config.get_ui_auth_url(), username=user_login, password=password)

    main_page = MainPage(driver=auth_browser, config=config)

    before_spending_resp = spend_client.get_all_spends()
    assert before_spending_resp.status_code == 200
    before_spending_count = len(before_spending_resp.json())

    main_page.click_checkbox(spend_id=add_spending["id"])
    checked = main_page.get_checkbox_state(spend_id=add_spending["id"])
    main_page.click_delete_spend()
    main_page.click_submit_delete_spend()

    alert_on_deleted = main_page.alert_on_action()

    dt = datetime.fromisoformat(add_spending["spendDate"])
    date_str = dt.strftime("%m/%d/%Y")
    is_found_spend_row = main_page.is_found_spend_row(
        category_name=add_spending["category"]["name"],
        amount=add_spending["amount"],
        currency=add_spending["currency"],
        description=add_spending["description"],
        spend_date=date_str,
    )

    after_spending_resp = spend_client.get_all_spends()
    assert after_spending_resp.status_code == 200
    after_spending_count = len(after_spending_resp.json())

    assert checked is True
    assert before_spending_count - 1 == after_spending_count
    assert "Spendings succesfully deleted" in alert_on_deleted
    assert is_found_spend_row is False

def test_cancel_delete_spend(
        browser: WebDriver,
        config: ConfigProvider,
        add_spending: dict,
        spend_client: SpendApiClient,
):
    auth_browser = login(driver=browser, login_url=config.get_ui_auth_url(), username=user_login, password=password)

    main_page = MainPage(driver=auth_browser, config=config)

    before_spending_resp = spend_client.get_all_spends()
    assert before_spending_resp.status_code == 200
    before_spending_count = len(before_spending_resp.json())

    main_page.click_checkbox(spend_id=add_spending["id"])
    main_page.click_delete_spend()
    main_page.click_cancel_delete_spend()
    main_page.click_checkbox(spend_id=add_spending["id"])
    checked = main_page.get_checkbox_state(spend_id=add_spending["id"])

    dt = datetime.fromisoformat(add_spending["spendDate"])
    date_str = dt.strftime("%m/%d/%Y")
    is_found_spend_row = main_page.is_found_spend_row(
        category_name=add_spending["category"]["name"],
        amount=add_spending["amount"],
        currency=add_spending["currency"],
        description=add_spending["description"],
        spend_date=date_str,
    )

    after_spending_resp = spend_client.get_all_spends()
    assert after_spending_resp.status_code == 200
    after_spending_count = len(after_spending_resp.json())

    assert before_spending_count == after_spending_count
    assert checked is False
    assert is_found_spend_row is True