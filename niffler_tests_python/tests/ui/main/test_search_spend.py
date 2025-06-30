import pytest
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.model.spend import SpendModelAdd, SpendModel
from niffler_tests_python.tests.conftest import TestData, Pages
from niffler_tests_python.web_pages.MainPage import MainPage


@TestData.fill_spends
@TestData.spend(SpendModelAdd(
    amount = 8989.05,
    description = "test_search_spend_by_description",
    currency = "RUB",
    spendDate = "2025-06-27",
    category = {"name": "category for search desc"}
))
def test_search_spend_by_description(spend: SpendModel, main_page: MainPage, spend_client: SpendApiClient):
    description = spend.description

    main_page.open()
    main_page.enter_search_query(description)

    api_search_query = spend_client.get_all_spends_v2(search_query=description)
    api_spend_ids = [spend_item["id"] for spend_item in api_search_query["content"]]

    search_spend_ids = main_page.get_spend_ids_row()
    search_input_text = main_page.get_search_query_input()

    assert search_input_text == description
    assert len(api_spend_ids) == len(search_spend_ids)
    assert api_spend_ids == search_spend_ids

@TestData.fill_spends
@TestData.spend(SpendModelAdd(
    amount = 8989.05,
    description = "test_search_spend_by_category",
    currency = "RUB",
    spendDate = "2025-06-27",
    category = {"name": "category for search category"}
))
def test_search_spend_by_category(spend: SpendModel, main_page: MainPage, spend_client: SpendApiClient):
    category_name = spend.category.name

    main_page.open()
    main_page.enter_search_query(category_name)

    api_search_query = spend_client.get_all_spends_v2(search_query=category_name)
    api_spend_ids = [spend_item["id"] for spend_item in api_search_query["content"]]

    search_spend_ids = main_page.get_spend_ids_row()
    search_input_text = main_page.get_search_query_input()

    assert search_input_text == category_name
    assert len(api_spend_ids) == len(search_spend_ids)
    assert api_spend_ids == search_spend_ids

@TestData.fill_spends
@pytest.mark.parametrize("custom_date_spend", [
    {
        "amount": 8989.05,
        "description": "test_search_spend_by_MONTH",
        "currency": "RUB",
        "spendDate": "MONTH",
        "category": {"name": "category for search period"}
    },
    {
        "amount": 8989.05,
        "description": "test_search_spend_by_WEEK",
        "currency": "RUB",
        "spendDate": "WEEK",
        "category": {"name": "category for search period"}
    },
    {
        "amount": 8989.05,
        "description": "test_search_spend_by_TODAY",
        "currency": "RUB",
        "spendDate": "TODAY",
        "category": {"name": "category for search period"}
    },
    {
        "amount": 8989.05,
        "description": "test_search_spend_by_ALL",
        "currency": "RUB",
        "spendDate": "ALL",
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

    main_page.open()
    main_page.click_period_input()
    main_page.click_period_value(period)

    if period == "ALL":
        filter_period = None
    else:
        filter_period = period

    api_search = spend_client.get_all_spends_v2(filter_period=filter_period)
    api_spend_ids = [spend_item["id"] for spend_item in api_search["content"]]

    search_spend_ids = main_page.get_spend_ids_row()
    period_input_text = main_page.get_period_input()

    assert period_input_text == period
    assert len(api_spend_ids) == len(search_spend_ids)
    assert api_spend_ids == search_spend_ids

@TestData.fill_spends
@pytest.mark.parametrize("currency", ["RUB", "KZT", "EUR", "USD", "ALL"])
def test_search_spend_by_currency(
        main_page: MainPage,
        spend_client: SpendApiClient,
        currency: str
):
    main_page.open()
    main_page.click_currency_input()
    main_page.click_currency_value(currency)

    if currency == "ALL":
        filter_currency = None
    else:
        filter_currency = currency
    api_search = spend_client.get_all_spends_v2(filter_currency=filter_currency)
    api_spend_ids = [spend_item["id"] for spend_item in api_search["content"]]

    search_spend_ids = main_page.get_spend_ids_row()
    currency_input_text = main_page.get_currency_input()

    assert currency_input_text == currency
    assert len(api_spend_ids) == len(search_spend_ids)
    assert api_spend_ids == search_spend_ids