import pytest
from niffler_tests.clients.spend_client import SpendApiClient
from niffler_tests.tests.conftest import TestData
from niffler_tests.web_pages.MainPage import MainPage


@TestData.fill_test_spend
@TestData.add_custom_spend({
    "amount": 8989.05,
    "description": "test_search_spend_by_description",
    "currency": "RUB",
    "spendDate": "2025-06-27",
    "category": {"name": "category 1"}
})
def test_search_spend_by_description(add_custom_spend: dict, main_page: MainPage, spend_client: SpendApiClient):
    description = add_custom_spend["description"]
    main_page.open()
    main_page.enter_search_query(description)

    api_search_query = spend_client.get_all_spends_v2(search_query=description)
    assert api_search_query.status_code == 200
    body = api_search_query.json()
    api_spend_ids = [spend["id"] for spend in body["content"]]

    search_spend_ids = main_page.get_spend_ids_row()

    search_input_text = main_page.get_search_query_input()

    assert search_input_text == description
    assert len(api_spend_ids) == len(search_spend_ids)
    assert api_spend_ids == search_spend_ids

@TestData.fill_test_spend
@TestData.add_custom_spend({
    "amount": 8989.05,
    "description": "test_search_spend_by_category",
    "currency": "RUB",
    "spendDate": "2025-06-27",
    "category": {"name": "category 2"}
})
def test_search_spend_by_category(add_custom_spend: dict, main_page: MainPage, spend_client: SpendApiClient):
    category = add_custom_spend["category"]["name"]
    main_page.open()
    main_page.enter_search_query(category)

    api_search_query = spend_client.get_all_spends_v2(search_query=category)
    assert api_search_query.status_code == 200
    body = api_search_query.json()
    api_spend_ids = [spend["id"] for spend in body["content"]]

    search_spend_ids = main_page.get_spend_ids_row()

    search_input_text = main_page.get_search_query_input()

    assert search_input_text == category
    assert len(api_spend_ids) == len(search_spend_ids)
    assert api_spend_ids == search_spend_ids

@TestData.fill_test_spend
@pytest.mark.parametrize("add_custom_spend", [
    {
        "amount": 8989.05,
        "description": "test_search_spend_by_MONTH",
        "currency": "RUB",
        "spendDate": "MONTH",
        "category": {"name": "category 2"}
    },
    {
        "amount": 8989.05,
        "description": "test_search_spend_by_WEEK",
        "currency": "RUB",
        "spendDate": "WEEK",
        "category": {"name": "category 2"}
    },
    {
        "amount": 8989.05,
        "description": "test_search_spend_by_TODAY",
        "currency": "RUB",
        "spendDate": "TODAY",
        "category": {"name": "category 2"}
    },
    {
        "amount": 8989.05,
        "description": "test_search_spend_by_ALL",
        "currency": "RUB",
        "spendDate": "ALL",
        "category": {"name": "category 2"}
    }
], indirect=True)
def test_search_spend_by_period(
        add_custom_spend: dict,
        main_page: MainPage,
        spend_client: SpendApiClient
):
    period = add_custom_spend["period"]

    main_page.open()
    main_page.click_period_input()
    main_page.click_period_value(period)

    if period == "ALL":
        filter_period = None
    else:
        filter_period = period

    api_search = spend_client.get_all_spends_v2(filter_period=filter_period)
    assert api_search.status_code == 200
    body = api_search.json()
    api_spend_ids = [spend["id"] for spend in body["content"]]

    search_spend_ids = main_page.get_spend_ids_row()

    period_input_text = main_page.get_period_input()

    assert period_input_text == period
    assert len(api_spend_ids) == len(search_spend_ids)
    assert api_spend_ids == search_spend_ids

@TestData.fill_test_spend
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
    assert api_search.status_code == 200
    body = api_search.json()
    api_spend_ids = [spend["id"] for spend in body["content"]]

    search_spend_ids = main_page.get_spend_ids_row()

    currency_input_text = main_page.get_currency_input()

    assert currency_input_text == currency
    assert len(api_spend_ids) == len(search_spend_ids)
    assert api_spend_ids == search_spend_ids