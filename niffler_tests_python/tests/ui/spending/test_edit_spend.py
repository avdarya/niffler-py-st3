import allure
import pytest
from datetime import datetime
from dateutil.tz import tz
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.spend import SpendModelAdd, SpendModel
from niffler_tests_python.tests.conftest import Pages, TestData
from niffler_tests_python.utils.helpers import wait_for_spend_row, is_text_match_spend_row
from niffler_tests_python.web_pages.MainPage import MainPage
from niffler_tests_python.web_pages.SpendingPage import SpendingPage


@allure.epic('Spending management')
@allure.feature('Spending updating')
@allure.story('Edit spend')
@Pages.go_to_main_page_after_spend
@TestData.spend(SpendModelAdd(
    amount=203.01,
    description="test edit spend",
    currency="USD",
    spendDate="2025-06-26T21:00:00.000+00:00",
    category={"name": "edit spend"}
))
@pytest.mark.parametrize("amount, currency, new_category, spend_date, description", [
    ("456", "EUR", "after edit spend", "02/09/2025", "spending for update")
])
def test_edit_spend(
        main_page: MainPage,
        spending_page: SpendingPage,
        spend: SpendModel,
        spend_client: SpendApiClient,
        spend_db: SpendDB,
        amount: str,
        currency: str,
        new_category: str,
        spend_date: str,
        description: str,
):
    with allure.step('Open spend for editing'):
        added_spend_row = main_page.get_spend_row(spend_id=spend.id)
        main_page.click_edit_spend(added_spend_row)

    with allure.step('Enter amount'):
        spending_page.clear_amount_input()
        spending_page.enter_amount_input(amount=amount)

    with allure.step('Enter currency'):
        spending_page.click_currency_input()
        spending_page.click_currency_value(currency_value=currency)

    with allure.step('Enter category'):
        spending_page.clear_category_input()
        spending_page.enter_category_input(category_name=new_category)

    with allure.step('Enter date'):
        spending_page.enter_date_input(spend_date=spend_date)

    with allure.step('Enter description'):
        spending_page.clear_description_input()
        spending_page.enter_description_input(description=description)

    with allure.step('Click save button'):
        spending_page.click_save_spend()

    with allure.step('Save alert dialog'):
        alert_on_updated = main_page.alert_on_action()

    with allure.step('Save edited spend row from UI'):
        edited_spend_row = wait_for_spend_row(main_page=main_page, spend_id=spend.id)

    with allure.step('Retrieve edited spend from API'):
        api_spend = spend_client.get_spend_by_id(spend.id)
        local_dt = api_spend.spendDate.astimezone(tz.tzlocal())
        date_str = local_dt.strftime("%m/%d/%Y")

    with allure.step('Retrieve edited spend in DB'):
        db_spend = spend_db.get_spend(spend_id=spend.id)
        db_category = spend_db.get_category_by_name(name=new_category)

    with allure.step('Assert edit spend'):
        with allure.step('Verify alert text'):
            assert "Spending is edited successfully" in alert_on_updated
        with allure.step('Verify edited spend row data in UI'):
            assert is_text_match_spend_row(
                spend_row_text=edited_spend_row.text,
                category_name=new_category,
                amount=amount,
                currency=currency,
                description=description,
                spend_date=spend_date
            )
        with allure.step('Verify edited spend date in API'):
            assert date_str == spend_date
        with allure.step('Verify edited spend category in API'):
            assert api_spend.category.name == new_category
        with allure.step('Verify edited spend currency in API'):
            assert api_spend.currency == currency
        with allure.step('Verify edited spend amount in API'):
            assert api_spend.amount == float(amount)
        with allure.step('Verify edited spend description in API'):
            assert api_spend.description == description

        with allure.step('Verify edited spend amount in DB'):
            assert db_spend.amount == float(amount)
        with allure.step('Verify edited spend currency in DB'):
            assert db_spend.currency == currency
        with allure.step('Verify edited spend date in DB'):
            assert db_spend.spend_date == datetime.strptime(spend_date, "%m/%d/%Y").date()
        with allure.step('Verify edited spend description in DB'):
            assert db_spend.description == description
        with allure.step('Verify edited spend category in DB'):
            assert db_category.name == new_category
