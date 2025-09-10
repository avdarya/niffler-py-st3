import allure
import pytest
from datetime import datetime
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.spend import SpendModelAdd, SpendModel, SpendModelEdit
from niffler_tests_python.utils.marks import TestData


@allure.epic('Spending management')
@allure.feature('[API-test] Spending updating - Positive')
@allure.story('Edit spend')
@TestData.spend(SpendModelAdd(
    amount=203.01,
    description="test edit spend",
    currency="USD",
    spendDate="2025-06-26T21:00:00.000+00:00",
    category={"name": "edit spend"}
))
@pytest.mark.parametrize("amount, currency, spend_date, description", [
    ("456", "EUR", "2025-07-09T21:00:00.000+00:00", "spending for update")
])
def test_edit_spend(
        spend: SpendModel,
        spend_client: SpendApiClient,
        spend_db: SpendDB,
        amount: str,
        currency: str,
        spend_date: str,
        description: str,
        username: str
):
    expected_date = datetime.fromisoformat(spend_date.replace("Z", "+00:00")).date()
    expected_date_db = datetime.fromisoformat(spend_date.replace("Z", "+00:00")).astimezone().date()

    with allure.step('Send request for edit spending'):
        data_for_edit = SpendModelEdit(
            id=spend.id,
            amount=float(amount),
            category={"name": spend.category.name},
            description=description,
            currency=currency,
            spendDate=spend_date
        )
        edited_spend = spend_client.edit_spend(data_for_edit)

    with allure.step('Retrieve edited spend from API'):
        api_spend = spend_client.get_spend_by_id(spend.id)

    with (allure.step('Retrieve edited spend row from DB')):
        db_spend = spend_db.get_spend(spend.id)
        db_spend_date = datetime.combine(db_spend.spend_date, datetime.min.time()).date()

    with allure.step('Assert edit spend'):
        with allure.step('Verify response data for edite spend'):
            assert edited_spend.amount == float(amount)
            assert edited_spend.category.name == spend.category.name
            assert edited_spend.category.username == username
            assert edited_spend.description == description
            assert edited_spend.currency == currency
            assert edited_spend.username == username
            assert edited_spend.spendDate.date() == expected_date
        with allure.step('Verify edited spend data in API'):
            assert api_spend.amount ==  float(amount)
            assert api_spend.category.name == spend.category.name
            assert api_spend.category.username == username
            assert api_spend.description == description
            assert api_spend.currency == currency
            assert api_spend.username == username
            assert api_spend.spendDate.date() == expected_date
        with allure.step('Verify edited spend data in DB'):
            assert db_spend.amount == float(amount)
            assert str(db_spend.category_id) == spend.category.id
            assert db_spend.description == description
            assert db_spend.currency == currency
            assert db_spend.username == username
            assert db_spend_date == expected_date_db
