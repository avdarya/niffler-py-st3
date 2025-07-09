from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.tests.conftest import TestData, Pages
from niffler_tests_python.web_pages.MainPage import MainPage


@Pages.go_to_main_page_after_fill_spends
@TestData.fill_spends
def test_next_page(main_page: MainPage, spend_client: SpendApiClient):
    main_page.click_next_page()

    api_next_page = spend_client.get_all_spends_v2(page=1)
    api_spend_ids = [spend_item["id"] for spend_item in api_next_page["content"]]

    ui_spend_ids = main_page.get_spend_ids_row()

    assert len(api_next_page["content"]) == len(ui_spend_ids)
    assert api_spend_ids == ui_spend_ids

@Pages.go_to_main_page_after_fill_spends
@TestData.fill_spends
def test_previous_page(main_page: MainPage, spend_client: SpendApiClient):
    main_page.click_next_page()

    main_page.click_previous_page()

    api_previous_page = spend_client.get_all_spends_v2()
    api_spend_ids = [spend_item["id"] for spend_item in api_previous_page["content"]]

    ui_spend_ids = main_page.get_spend_ids_row()

    assert len(api_previous_page["content"]) == len(ui_spend_ids)
    assert api_spend_ids == ui_spend_ids
