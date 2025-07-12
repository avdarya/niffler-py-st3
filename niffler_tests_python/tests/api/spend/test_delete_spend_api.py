import allure

from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.utils.marks import TestData


@allure.epic('Spending management')
@allure.feature('[API-test] Spending delete - Positive')
@allure.story('Delete spends by list')
@TestData.fill_spends
def test_delete_spending_by_list(
        fill_spends: list[str],
        spend_client: SpendApiClient,
        spend_db: SpendDB
):
    with allure.step('Retrieve spending count before'):
        before_spends = spend_client.get_all_spends()
        before_spending_count = len(before_spends)

    with allure.step('Send request for delete spend list'):
        spend_client.delete_spend(fill_spends)

    with allure.step('Retrieve spending count and ids after'):
        after_spending = spend_client.get_all_spends()
        after_spending_count = len(after_spending)
        after_spend_ids = [spend.id for spend in after_spending]

    with (allure.step('Retrieve deleted spend rows from DB')):
        db_spends = spend_db.get_spend_list(fill_spends)

    with allure.step('Assert spendings deleted by provided ID list'):
        with allure.step('Spending count before - selected ids count = spending count after'):
            assert before_spending_count - len(fill_spends) == after_spending_count
        with allure.step('Verify deleted spends are absent in API response'):
            assert set(after_spend_ids).isdisjoint(fill_spends)
        with allure.step('Verify deleted spends are absent in DB'):
            assert len(db_spends) == 0