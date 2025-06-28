from time import sleep

from niffler_tests.clients.spend_client import SpendApiClient
from niffler_tests.tests.conftest import TestData
from niffler_tests.web_pages.MainPage import MainPage


@TestData.fill_test_spend
def test_next_page(main_page: MainPage, spend_client: SpendApiClient):
    main_page.open()
    main_page.click_next_page()

    api_next_page = spend_client.get_all_spends_v2(page=1)
    assert api_next_page.status_code == 200
    body = api_next_page.json()
    api_spend_ids = [spend["id"] for spend in body["content"]]

    ui_spend_ids = main_page.get_spend_ids_row()

    assert len(body["content"]) == len(ui_spend_ids)
    assert api_spend_ids == ui_spend_ids

@TestData.fill_test_spend
def test_previous_page(main_page: MainPage, spend_client: SpendApiClient):
    main_page.open()
    main_page.click_next_page()

    main_page.click_previous_page()

    api_previous_page = spend_client.get_all_spends_v2()
    assert api_previous_page.status_code == 200
    body = api_previous_page.json()
    api_spend_ids = [spend["id"] for spend in body["content"]]

    ui_spend_ids = main_page.get_spend_ids_row()

    assert len(body["content"]) == len(ui_spend_ids)
    assert api_spend_ids == ui_spend_ids
