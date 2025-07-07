import allure
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.spend import SpendModelAdd, SpendModel
from niffler_tests_python.tests.conftest import TestData, Pages
from niffler_tests_python.web_pages.MainPage import MainPage


@allure.epic('Spending management')
@allure.feature('Spending delete')
@allure.story('Delete single spend')
@Pages.go_to_main_page_after_spend
@TestData.spend(SpendModelAdd(
    amount=9.01,
    description="test delete spending by one",
    currency="EUR",
    spendDate="2025-06-23T21:00:00.000+00:00",
    category={"name": "spend delete by one"}
))
def test_delete_spending_by_one(
        main_page: MainPage,
        spend: SpendModel,
        spend_client: SpendApiClient,
        spend_db: SpendDB
):
    with allure.step('Retrieve spending count before'):
        before_spending = spend_client.get_all_spends()
        before_spending_count = len(before_spending)

    with allure.step('Save spend row for delete'):
        spend_row = main_page.get_spend_row(spend_id=spend.id)
        assert spend_row is not None

    with allure.step('Select spend row'):
        main_page.click_checkbox(spend_row)
        checked = main_page.get_checkbox_state(spend_row)

    with allure.step('Delete spend'):
        main_page.click_delete_spend()
        main_page.click_submit_delete_spend()

    with allure.step('Save alert dialog'):
        alert_on_deleted = main_page.alert_on_action()

    with allure.step('Try to find deleted spend row'):
        spend_row_after_deleted = main_page.get_spend_row(spend_id=spend.id)

    with allure.step('Retrieve spending count after'):
        after_spending = spend_client.get_all_spends()
        after_spending_count = len(after_spending)

    with allure.step('Retrieve deleted spend'):
        db_spend = spend_db.get_spend(spend.id)

    with allure.step('Assert spend row deleted'):
        with allure.step('Verify checkbox state after select'):
            assert checked is True
        with allure.step('Spending count after = spending count before + 1'):
            assert before_spending_count - 1 == after_spending_count
        with allure.step('Verify alert text'):
            assert "Spendings succesfully deleted" in alert_on_deleted
        with allure.step('Deleted spend row does not exist in UI'):
            assert spend_row_after_deleted is None
        with allure.step('Deleted spend record does not exist in DB'):
            assert db_spend is None

@allure.epic('Spending management')
@allure.feature('Spending delete')
@allure.story('Delete spend list')
@Pages.go_to_main_page_after_fill_spends
@TestData.fill_spends
def test_delete_spending_by_list(main_page: MainPage, spend_client: SpendApiClient, spend_db: SpendDB):
    with allure.step('Retrieve spending count before'):
        before_spending = spend_client.get_all_spends()
        before_spending_count = len(before_spending)

    with allure.step('Select all spend rows by checkbox in table header'):
        main_page.click_select_all_rows()
        selected_spend_ids = main_page.get_selected_spend_ids_row()

    with allure.step('Delete spend'):
        main_page.click_delete_spend()
        main_page.click_submit_delete_spend()

    with allure.step('Save alert dialog'):
        alert_on_deleted = main_page.alert_on_action()

    with allure.step('Save display spend ids after delete'):
        ui_spend_ids_after_deleted = main_page.get_spend_ids_row()

    with allure.step('Retrieve spending count and ids after'):
        after_spending = spend_client.get_all_spends()
        after_spending_count = len(after_spending)
        after_spend_ids = [spend.id for spend in after_spending]

    with allure.step('Verify deleted spends are absent in DB'):
        for spend_id in selected_spend_ids:
            assert spend_db.get_spend(spend_id) is None

    with allure.step('Assert spend rows deleted after multi select'):
        with allure.step('Spending count after = spending count before + selected spend row count'):
            assert before_spending_count - len(selected_spend_ids) == after_spending_count
        with allure.step('Verify alert text'):
            assert "Spendings succesfully deleted" in alert_on_deleted
        with allure.step('Verify deleted spends are absent in API response'):
            assert set(after_spend_ids).isdisjoint(selected_spend_ids)
        with allure.step('Verify deleted spends are absent in UI spend table'):
            assert set(ui_spend_ids_after_deleted).isdisjoint(selected_spend_ids)

@allure.epic('Spending management')
@allure.feature('Spending delete')
@allure.story('Cancel delete spend')
@Pages.go_to_main_page_after_spend
@TestData.spend(SpendModelAdd(
    amount=12.01,
    description="test cancel delete spend",
    currency="USD",
    spendDate="2025-06-26T21:00:00.000+00:00",
    category={"name": "cancel delete spend"}
))
def test_cancel_delete_spend(
        main_page: MainPage,
        spend: SpendModel,
        spend_client: SpendApiClient,
        spend_db: SpendDB
):
    with allure.step('Retrieve spending count before'):
        before_spending = spend_client.get_all_spends()
        before_spending_count = len(before_spending)

    with allure.step('Save spend row for delete'):
        spend_row = main_page.get_spend_row(spend_id=spend.id)
        assert spend_row is not None

    with allure.step('Select spend row for delete'):
        main_page.click_checkbox(spend_row)

    with allure.step('Click delete button and cancel deletion'):
        main_page.click_delete_spend()
        main_page.click_cancel_delete_spend()

    with allure.step('Check spend row checkbox state after cancel'):
        main_page.click_checkbox(spend_row)
        checked = main_page.get_checkbox_state(spend_row)

    with allure.step('Find selected spend row'):
        spend_row_after_deleted = main_page.get_spend_row(spend_id=spend.id)

    with allure.step('Retrieve spending count and ids after'):
        after_spending = spend_client.get_all_spends()
        after_spending_count = len(after_spending)

    with allure.step('Retrieve selected spend from DB'):
        db_spend = spend_db.get_spend(spend_id=spend.id)

    with allure.step('Assert spend row exists after cancel delete'):
        with allure.step('Spending count after = spending count before'):
            assert before_spending_count == after_spending_count
        with allure.step('Verify checkbox state after deselect'):
            assert checked is False
        with allure.step('Verify selected row exists in UI'):
            assert spend_row_after_deleted is not None
        with allure.step('Verify selected spend exists in DB'):
            assert db_spend is not None