from niffler_tests.clients.spend_client import SpendApiClient
from niffler_tests.tests.conftest import TestData
from niffler_tests.web_pages.MainPage import MainPage


def test_delete_spending_by_one(
        main_page: MainPage,
        add_spend: dict,
        spend_client: SpendApiClient,
):
    main_page.open()

    before_spending_resp = spend_client.get_all_spends()
    assert before_spending_resp.status_code == 200
    before_spending_count = len(before_spending_resp.json())

    spend_row = main_page.get_spend_row(spend_id=add_spend["id"])
    assert spend_row is not None

    main_page.click_checkbox(spend_row)

    checked = main_page.get_checkbox_state(spend_row)
    main_page.click_delete_spend()
    main_page.click_submit_delete_spend()

    alert_on_deleted = main_page.alert_on_action()

    spend_row_after_deleted = main_page.get_spend_row(spend_id=add_spend["id"])

    after_spending_resp = spend_client.get_all_spends()
    assert after_spending_resp.status_code == 200
    after_spending_count = len(after_spending_resp.json())

    assert checked is True
    assert before_spending_count - 1 == after_spending_count
    assert "Spendings succesfully deleted" in alert_on_deleted
    assert spend_row_after_deleted is None

@TestData.fill_test_spend
def test_delete_spending_by_list(
        main_page: MainPage,
        spend_client: SpendApiClient,
):
    main_page.open()

    before_spending_resp = spend_client.get_all_spends()
    assert before_spending_resp.status_code == 200
    before_spending_count = len(before_spending_resp.json())

    main_page.click_select_all_rows()
    selected_spend_ids = main_page.get_selected_spend_ids_row()

    main_page.click_delete_spend()
    main_page.click_submit_delete_spend()

    alert_on_deleted = main_page.alert_on_action()

    spend_ids_after_deleted = main_page.get_spend_ids_row()

    after_spending_resp = spend_client.get_all_spends()
    assert after_spending_resp.status_code == 200
    after_body = after_spending_resp.json()
    after_spending_count = len(after_body)
    api_spend_ids = [spend["id"] for spend in after_body]

    assert before_spending_count - len(selected_spend_ids) == after_spending_count
    assert "Spendings succesfully deleted" in alert_on_deleted
    assert set(api_spend_ids).isdisjoint(selected_spend_ids)
    assert set(spend_ids_after_deleted).isdisjoint(selected_spend_ids)

def test_cancel_delete_spend(
        main_page: MainPage,
        add_spend: dict,
        spend_client: SpendApiClient,
):
    main_page.open()

    before_spending_resp = spend_client.get_all_spends()
    assert before_spending_resp.status_code == 200
    before_spending_count = len(before_spending_resp.json())

    spend_row = main_page.get_spend_row(spend_id=add_spend["id"])
    assert spend_row is not None

    main_page.click_checkbox(spend_row)
    main_page.click_delete_spend()
    main_page.click_cancel_delete_spend()
    main_page.click_checkbox(spend_row)
    checked = main_page.get_checkbox_state(spend_row)

    spend_row_after_deleted = main_page.get_spend_row(spend_id=add_spend["id"])

    after_spending_resp = spend_client.get_all_spends()
    assert after_spending_resp.status_code == 200
    after_spending_count = len(after_spending_resp.json())

    assert before_spending_count == after_spending_count
    assert checked is False
    assert spend_row_after_deleted is not None