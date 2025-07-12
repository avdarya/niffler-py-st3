import allure
import pytest
from datetime import datetime
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.category import CategoryModel
from niffler_tests_python.utils.marks import Pages, TestData
from niffler_tests_python.utils.api_checkers import assert_spend_record_exists
from niffler_tests_python.utils.helpers import wait_for_spend_row, is_text_match_spend_row
from niffler_tests_python.web_pages.components.Header import Header
from niffler_tests_python.web_pages.MainPage import MainPage
from niffler_tests_python.web_pages.SpendingPage import SpendingPage


@allure.epic('Spending management')
@allure.feature('Spending creation')
@allure.story('Add spend')
@Pages.go_to_main_page
@TestData.category("add spend")
@pytest.mark.parametrize("amount, currency, spend_date, description", [
    ("10.01", "RUB", "12/09/2024", "test add spending"),
    ("501", "KZT", "01/15/2025", "test add spending"),
    ("0.01", "EUR", "04/09/2025", "test add spending"),
    ("3", "USD", "06/21/2025", "test add spending")
])
def test_add_spending(
        main_page: MainPage,
        header: Header,
        spending_page: SpendingPage,
        spend_client: SpendApiClient,
        category: CategoryModel,
        spend_db: SpendDB,
        amount: str,
        currency: str,
        spend_date: str,
        description: str,
):
    with allure.step('Click new spending button'):
        header.click_new_spending()

    with allure.step('Retrieve spending count before'):
        before_spending = spend_client.get_all_spends()
        before_spending_count = len(before_spending)

    with allure.step('Enter amount'):
        spending_page.clear_amount_input()
        spending_page.enter_amount_input(amount)

    with allure.step('Enter currency'):
        spending_page.click_currency_input()
        spending_page.click_currency_value(currency)

    with allure.step('Select category'):
        category_name = category.name
        spending_page.click_category(category_name=category_name)

    with allure.step('Enter date'):
        spending_page.enter_date_input(spend_date=spend_date)

    with allure.step('Enter description'):
        spending_page.enter_description_input(description=description)

    with allure.step('Click add button'):
        spending_page.click_save_spend()

    with allure.step('Save alert dialog'):
        alert_on_added = main_page.alert_on_action()

    with allure.step('Retrieve spending count after'):
        after_spending = spend_client.get_all_spends()
        after_spending_count = len(after_spending)
        with allure.step('Spending count after = spending count before + 1'):
            assert before_spending_count == after_spending_count - 1

    with allure.step('Retrieve added spend from API'):
        api_spend = assert_spend_record_exists(
            api_response=after_spending,
            currency=currency,
            amount=amount,
            spend_date=spend_date,
            description=description,
            category_name=category.name,
            spend_client=spend_client,
        )

    with allure.step('Save added spend row from UI'):
        spend_row = wait_for_spend_row(main_page=main_page, spend_id=api_spend.id)

    with allure.step('Retrieve added spend row from DB'):
        db_spend = spend_db.get_spend(api_spend.id)
        db_category = spend_db.get_category_by_name(category_name)

    with allure.step('Delete added spend'):
        spend_client.delete_spend([api_spend.id])

    with allure.step('Assert add spend'):
        with allure.step('Verify alert text'):
            assert "New spending is successfully created" in alert_on_added
        with allure.step('Verify added spend row data in UI'):
            assert spend_row is not None
            assert is_text_match_spend_row(
                spend_row_text=spend_row.text,
                category_name=category.name,
                amount=amount,
                currency=currency,
                description=description,
                spend_date=spend_date
            )
        with allure.step('Verify added spend amount in DB'):
            assert db_spend.amount == float(amount)
        with allure.step('Verify added spend currency in DB'):
            assert db_spend.currency == currency
        with allure.step('Verify added spend date in DB'):
            assert db_spend.spend_date == datetime.strptime(spend_date, "%m/%d/%Y").date()
        with allure.step('Verify added spend description in DB'):
            assert db_spend.description == description
        with allure.step('Verify added spend category in DB'):
            assert db_category.name == category_name