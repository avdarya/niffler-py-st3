from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.spend import SpendModelAdd, SpendModel
from niffler_tests_python.tests.conftest import TestData, Pages
from niffler_tests_python.web_pages.MainPage import MainPage


@Pages.go_to_main_page_after_spend
@TestData.spend(SpendModelAdd(
    amount=9.01,
    description="test_delete_spending_by_one",
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
    before_spending = spend_client.get_all_spends()
    before_spending_count = len(before_spending)

    spend_row = main_page.get_spend_row(spend_id=spend.id)
    assert spend_row is not None

    main_page.click_checkbox(spend_row)

    checked = main_page.get_checkbox_state(spend_row)
    main_page.click_delete_spend()
    main_page.click_submit_delete_spend()

    alert_on_deleted = main_page.alert_on_action()

    spend_row_after_deleted = main_page.get_spend_row(spend_id=spend.id)

    after_spending = spend_client.get_all_spends()
    after_spending_count = len(after_spending)

    db_spend = spend_db.get_spend(spend.id)

    assert checked is True
    assert before_spending_count - 1 == after_spending_count
    assert "Spendings succesfully deleted" in alert_on_deleted
    assert spend_row_after_deleted is None
    assert db_spend is None

@Pages.go_to_main_page_after_fill_spends
@TestData.fill_spends
def test_delete_spending_by_list(main_page: MainPage, spend_client: SpendApiClient, spend_db: SpendDB):
    before_spending = spend_client.get_all_spends()
    before_spending_count = len(before_spending)

    main_page.click_select_all_rows()
    selected_spend_ids = main_page.get_selected_spend_ids_row()

    main_page.click_delete_spend()
    main_page.click_submit_delete_spend()

    alert_on_deleted = main_page.alert_on_action()

    ui_spend_ids_after_deleted = main_page.get_spend_ids_row()

    after_spending = spend_client.get_all_spends()
    after_spending_count = len(after_spending)
    after_spend_ids = [spend.id for spend in after_spending]

    for spend_id in selected_spend_ids:
        assert spend_db.get_spend(spend_id) is None

    assert before_spending_count - len(selected_spend_ids) == after_spending_count
    assert "Spendings succesfully deleted" in alert_on_deleted
    assert set(after_spend_ids).isdisjoint(selected_spend_ids)
    assert set(ui_spend_ids_after_deleted).isdisjoint(selected_spend_ids)

@Pages.go_to_main_page_after_spend
@TestData.spend(SpendModelAdd(
    amount=12.01,
    description="test_cancel_delete_spend",
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
    before_spending = spend_client.get_all_spends()
    before_spending_count = len(before_spending)

    spend_row = main_page.get_spend_row(spend_id=spend.id)
    assert spend_row is not None

    main_page.click_checkbox(spend_row)
    main_page.click_delete_spend()
    main_page.click_cancel_delete_spend()
    main_page.click_checkbox(spend_row)
    checked = main_page.get_checkbox_state(spend_row)

    spend_row_after_deleted = main_page.get_spend_row(spend_id=spend.id)

    after_spending = spend_client.get_all_spends()
    after_spending_count = len(after_spending)

    db_spend = spend_db.get_spend(spend_id=spend.id)

    assert before_spending_count == after_spending_count
    assert checked is False
    assert spend_row_after_deleted is not None
    assert db_spend is not None