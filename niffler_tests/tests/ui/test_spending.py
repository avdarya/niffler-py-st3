import pytest
import os
from dateutil import tz
import dotenv
from datetime import datetime
from faker import Faker
from selenium.webdriver.ie.webdriver import WebDriver
from clients.spend_client import SpendApiClient
from configuration.ConfigProvider import ConfigProvider
from tests.conftest import update_category
from tests.ui.helpers.api_checkers import assert_spend_record_exists
from tests.ui.helpers.helpers import login, wait_for_category_update_name, wait_for_category_update_archive
from web_pages.HeaderPage import HeaderPage
from web_pages.MainPage import MainPage
from web_pages.SpendingPage import SpendingPage

dotenv.load_dotenv()
user_login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")

fake = Faker()

@pytest.mark.parametrize("amount, currency, spend_date", [
    ("10.01", "RUB", "12/09/2024"),
    ("501", "KZT", "01/15/2025"),
    ("0.01", "EUR", "04/09/2025"),
    ("3", "USD", "06/21/2025")
])
def test_add_spending(
        browser: WebDriver,
        config: ConfigProvider,
        add_category: dict,
        spend_client: SpendApiClient,
        amount: str,
        currency: str,
        spend_date: str,
):

    auth_browser = login(driver=browser, login_url=config.get_ui_auth_url(), username=user_login, password=password)

    before_spending_resp = spend_client.get_all_spends()
    assert before_spending_resp.status_code == 200
    before_spending_count = len(before_spending_resp.json())

    header_page = HeaderPage(driver=auth_browser)
    main_page = MainPage(driver=auth_browser, config=config)
    spending_page = SpendingPage(driver=auth_browser)

    header_page.click_new_spending()

    spending_page.clear_amount_input()
    spending_page.enter_amount_input(amount)

    spending_page.click_currency_input()
    spending_page.click_currency_value(currency)

    category_name = add_category["name"]
    spending_page.click_category(category_name=category_name)

    spending_page.enter_date_input(spend_date=spend_date)

    description = fake.sentence(nb_words=5)
    spending_page.enter_description_input(description=description)

    spending_page.click_save_spend()

    alert_on_added = main_page.alert_on_action()
    assert "New spending is successfully created" in alert_on_added

    is_spend_in_table = main_page.is_found_spend_row(
        category_name=add_category["name"],
        amount=amount,
        currency=currency,
        description=description,
        spend_date=spend_date
    )

    assert is_spend_in_table

    after_spending_resp = spend_client.get_all_spends()
    assert after_spending_resp.status_code == 200
    after_spending_count = len(after_spending_resp.json())
    assert before_spending_count == after_spending_count - 1

    spend_id = assert_spend_record_exists(
        api_response=after_spending_resp.json(),
        currency=currency,
        amount=amount,
        spend_date=spend_date,
        description=description,
        category_name=add_category["name"],
        spend_client=spend_client,
    )["id"]
    spend_client.delete_spending([spend_id])

@pytest.mark.parametrize("amount, currency, spend_date, description", [
    ("456", "EUR", "02/09/2025", "spending for update")
])
def test_edit_spend(
        browser: WebDriver,
        config: ConfigProvider,
        add_spending: dict,
        update_category: dict,
        spend_client: SpendApiClient,
        amount: str,
        currency: str,
        spend_date: str,
        description: str,
):

    auth_browser = login(driver=browser, login_url=config.get_ui_auth_url(), username=user_login, password=password)

    main_page = MainPage(driver=auth_browser, config=config)
    spending_page = SpendingPage(driver=auth_browser)

    main_page.click_edit_spend(spend_id=add_spending["id"])

    spending_page.clear_amount_input()
    spending_page.enter_amount_input(amount=amount)

    spending_page.click_currency_input()
    spending_page.click_currency_value(currency_value=currency)

    new_category = fake.text(max_nb_chars=25).replace("\n", " ")
    spending_page.clear_category_input()
    spending_page.enter_category_input(category_name=new_category)

    spending_page.enter_date_input(spend_date=spend_date)

    spending_page.clear_description_input()
    spending_page.enter_description_input(description=description)

    spending_page.click_save_spend()

    alert_on_updated = main_page.alert_on_action()

    is_found_updated_row = main_page.is_found_spend_row(
        category_name=new_category,
        amount=amount,
        currency=currency,
        description=description,
        spend_date=spend_date,
    )

    api_spend = spend_client.get_all_spends()
    assert api_spend.status_code == 200
    for spend in api_spend.json():
        if spend["id"] == add_spending["id"]:
            local_dt = datetime.fromisoformat(spend["spendDate"]).astimezone(tz.tzlocal())
            date_str = local_dt.strftime("%m/%d/%Y")

            update_category["name"] = spend["category"]["name"]
            update_category["archived"] = True
            update_category["id"] = spend["category"]["id"]

            assert date_str == spend_date
            assert spend["category"]["name"] == new_category
            assert spend["currency"] == currency
            assert spend["amount"] == float(amount)
            assert spend["description"] == description

    assert "Spending is edited successfully" in alert_on_updated
    assert is_found_updated_row

def test_delete_spending_by_one(
        browser: WebDriver,
        config: ConfigProvider,
        add_spending: dict,
        spend_client: SpendApiClient,
):
    auth_browser = login(driver=browser, login_url=config.get_ui_auth_url(), username=user_login, password=password)

    spending_page = SpendingPage(driver=auth_browser)
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

    spending_page = SpendingPage(driver=auth_browser)
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

