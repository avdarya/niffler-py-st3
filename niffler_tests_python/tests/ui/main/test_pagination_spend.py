import allure
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.utils.marks import Pages, TestData
from niffler_tests_python.web_pages.MainPage import MainPage


@allure.epic('Spending management')
@allure.feature('Spending pagination')
@allure.story('Go to next page of spends')
@Pages.go_to_main_page_after_fill_spends
@TestData.fill_spends
def test_next_page(main_page: MainPage, spend_client: SpendApiClient):
    with allure.step('Go to next page'):
        main_page.click_next_page()

    with allure.step('Retrieve spends for next page from API'):
        api_next_page = spend_client.get_all_spends_v2(page=1)
        api_spend_ids = [spend_item["id"] for spend_item in api_next_page["content"]]

    with allure.step('Save spend ids from next page in UI'):
        ui_spend_ids = main_page.get_spend_ids_row()

    with allure.step('Assert for next page'):
        with allure.step('For next page spend cound from API == spend count from UI'):
            assert len(api_next_page["content"]) == len(ui_spend_ids)
    with allure.step('For next page spend ids from API == spend ids from UI'):
        assert api_spend_ids == ui_spend_ids

@allure.epic('Spending management')
@allure.feature('Spending pagination')
@allure.story('Go to previous page of spends')
@Pages.go_to_main_page_after_fill_spends
@TestData.fill_spends
def test_previous_page(main_page: MainPage, spend_client: SpendApiClient):
    with allure.step('Go to next page'):
        main_page.click_next_page()

    with allure.step('Go to previous page'):
        main_page.click_previous_page()

    with allure.step('Retrieve spends for previous page from API'):
        api_previous_page = spend_client.get_all_spends_v2()
        api_spend_ids = [spend_item["id"] for spend_item in api_previous_page["content"]]

    with allure.step('Save spend ids from previous page in UI'):
        ui_spend_ids = main_page.get_spend_ids_row()

    with allure.step('Assert for previous page'):
        with allure.step('For previous page spend cound from API == spend count from UI'):
            assert len(api_previous_page["content"]) == len(ui_spend_ids)
        with allure.step('For previous page spend ids from API == spend ids from UI'):
            assert api_spend_ids == ui_spend_ids
