import allure
import pytest
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.model.spend import SpendModelAdd, SpendModel
from niffler_tests_python.tests.conftest import TestData
from niffler_tests_python.web_pages.MainPage import MainPage


@allure.epic('Spending management')
@allure.feature('Spending search')
@allure.story('Search spend by description')
@TestData.fill_spends
@TestData.spend(SpendModelAdd(
    amount = 8989.05,
    description = "test search spend by description",
    currency = "RUB",
    spendDate = "2025-06-27",
    category = {"name": "category for search desc"}
))
def test_search_spend_by_description(spend: SpendModel, main_page: MainPage, spend_client: SpendApiClient):
    description = spend.description

    with allure.step('Go to main page'):
        main_page.open()

    with allure.step('Enter search query by description'):
        main_page.enter_search_query(description)

    with allure.step('Retrieve search query by description from API'):
        api_search_query = spend_client.get_all_spends_v2(search_query=description)
        api_spend_ids = [spend_item["id"] for spend_item in api_search_query["content"]]

    with allure.step('Save in UI spend ids after searching'):
        search_spend_ids = main_page.get_spend_ids_row()

    with allure.step('Save search input text after searching'):
        search_input_text = main_page.get_search_query_input()

    with allure.step('Assert search spend by description'):
        with allure.step('Verify search input text contains search query'):
            assert search_input_text == description
        with allure.step('After searching spend count from API = spend count from UI'):
            assert len(api_spend_ids) == len(search_spend_ids)
        with allure.step('After searching spend ids from API = spend ids from UI'):
            assert api_spend_ids == search_spend_ids

@allure.epic('Spending management')
@allure.feature('Spending search')
@allure.story('Search spend by category')
@TestData.fill_spends
@TestData.spend(SpendModelAdd(
    amount = 8989.05,
    description = "test search spend by category",
    currency = "RUB",
    spendDate = "2025-06-27",
    category = {"name": "category for search category"}
))
def test_search_spend_by_category(spend: SpendModel, main_page: MainPage, spend_client: SpendApiClient):
    category_name = spend.category.name

    with allure.step('Go to main page'):
        main_page.open()

    with allure.step('Enter search query by category name'):
        main_page.enter_search_query(category_name)

    with allure.step('Retrieve search query by category name  from API'):
        api_search_query = spend_client.get_all_spends_v2(search_query=category_name)
        api_spend_ids = [spend_item["id"] for spend_item in api_search_query["content"]]

    with allure.step('Save in UI spend ids after searching'):
        search_spend_ids = main_page.get_spend_ids_row()

    with allure.step('Save search input text after searching'):
        search_input_text = main_page.get_search_query_input()

    with allure.step('Assert search spend by category name'):
        with allure.step('Verify search input text contains search query'):
            assert search_input_text == category_name
        with allure.step('After searching spend count from API = spend count from UI'):
            assert len(api_spend_ids) == len(search_spend_ids)
        with allure.step('After searching spend ids from API = spend ids from UI'):
            assert api_spend_ids == search_spend_ids

@allure.epic('Spending management')
@allure.feature('Spending search')
@allure.story('Search spend by period')
@TestData.fill_spends
@pytest.mark.parametrize("custom_date_spend", [
    {
        "amount": 8989.05,
        "description": "test search spend by MONTH",
        "currency": "RUB",
        "spendDate": "MONTH",
        "category": {"name": "category for search period"}
    },
    {
        "amount": 8989.05,
        "description": "test search spend by WEEK",
        "currency": "RUB",
        "spendDate": "WEEK",
        "category": {"name": "category for search period"}
    },
    {
        "amount": 8989.05,
        "description": "test search spend by TODAY",
        "currency": "RUB",
        "spendDate": "TODAY",
        "category": {"name": "category for search period"}
    }
], indirect=True)
def test_search_spend_by_period(
        custom_date_spend: tuple[SpendModel, dict[str, str]],
        main_page: MainPage,
        spend_client: SpendApiClient
):
    added_spend, period_dict = custom_date_spend
    period = period_dict["period"]

    with allure.step('Go to main page'):
        main_page.open()

    with allure.step('Select date period'):
        main_page.click_period_field()
        main_page.click_period_value(period)

    with allure.step('Retrieve search query by period from API'):
        api_search = spend_client.get_all_spends_v2(filter_period=period)
        api_spend_ids = [spend_item["id"] for spend_item in api_search["content"]]

    with allure.step('Save in UI spend ids after searching'):
        search_spend_ids = main_page.get_spend_ids_row()

    with allure.step('Save period input value after searching'):
        period_input_text = main_page.get_period_input()

    with allure.step('Assert search spend by period'):
        with allure.step('Verify date input value contains selected period'):
            assert period_input_text == period
        with allure.step('After searching spend count from API = spend count from UI'):
            assert len(api_spend_ids) == len(search_spend_ids)
        with allure.step('After searching spend ids from API = spend ids from UI'):
            assert api_spend_ids == search_spend_ids

@allure.epic('Spending management')
@allure.feature('Spending search')
@allure.story('Search spend by currency')
@TestData.fill_spends
@pytest.mark.parametrize("currency", ["RUB", "KZT", "EUR", "USD"])
def test_search_spend_by_currency(
        main_page: MainPage,
        spend_client: SpendApiClient,
        currency: str
):
    with allure.step('Go to main page'):
        main_page.open()

    with allure.step('Select currency'):
        main_page.click_currency_field()
        main_page.click_currency_value(currency)

    with allure.step('Retrieve search query by currency from API'):
        api_search = spend_client.get_all_spends_v2(filter_currency=currency)
        api_spend_ids = [spend_item["id"] for spend_item in api_search["content"]]

    with allure.step('Save in UI spend ids after searching'):
        search_spend_ids = main_page.get_spend_ids_row()

    with allure.step('Save currency input value after searching'):
        currency_input_text = main_page.get_currency_input()

    with allure.step('Assert search spend by currency'):
        with allure.step('Verify currency input value contains selected currency'):
            assert currency_input_text == currency
        with allure.step('After searching spend count from API = spend count from UI'):
            assert len(api_spend_ids) == len(search_spend_ids)
        with allure.step('After searching spend ids from API = spend ids from UI'):
            assert api_spend_ids == search_spend_ids