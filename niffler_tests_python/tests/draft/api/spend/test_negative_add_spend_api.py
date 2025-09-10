import allure
import pytest
from typing import Callable
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.spend import SpendModelAdd


@allure.epic('Spending management')
@allure.feature('[API-test] Spending creation - Negative')
@allure.story('Attempt add future spend')
@pytest.mark.parametrize("amount, category, currency, description", [
    ("10.01", "future spend", "RUB", "test add future spending")
])
def test_add_future_spend(
        spend_client: SpendApiClient,
        make_future_date: Callable,
        spend_db: SpendDB,
        amount: str,
        category: str,
        currency: str,
        description: str,
):
    future_date = make_future_date(1)

    with allure.step('Retrieve before spending count before from API'):
        before_get_all_spends = spend_client.get_all_spends()
        before_spending_count = len(before_get_all_spends)

    with (allure.step('Retrieve before spending count from DB')):
        before_db_spending_count = spend_db.get_spend_count()

    with (allure.step('Send request for added future spending')):
        future_spend = spend_client.add_spend_error(SpendModelAdd(
            amount=float(amount),
            category={"name": category},
            description=description,
            currency=currency,
            spendDate=future_date
        ).model_dump())

    with allure.step('Retrieve after spending count from API'):
        after_get_all_spends = spend_client.get_all_spends()
        after_spending_count = len(after_get_all_spends)

    with (allure.step('Retrieve after spending count from DB')):
        after_db_spending_count = spend_db.get_spend_count()

    with allure.step('Assert future spending does not added'):
        with allure.step('Verify response for added future spending'):
            assert future_spend.type == "niffler-gateway: Entity validation error"
            assert future_spend.title == "Bad Request"
            assert future_spend.status == 400
            assert future_spend.detail == "Spend date must not be future or less than 01.01.1970"
            assert future_spend.instance == "/api/spends/add"
        with allure.step('Verify before spending count = after spending count from API'):
            assert before_spending_count == after_spending_count
        with allure.step('Verify before spending count = after spending count in DB'):
            assert before_db_spending_count == after_db_spending_count

@allure.epic('Spending management')
@allure.feature('[API-test] Spending creation - Negative')
@allure.story('Attempt add spending with amount less then allowed')
@pytest.mark.parametrize("amount, category, spend_date, currency, description", [
    ("0.009", "less min amount", "2025-07-09T21:00:00.000+00:00", "RUB", "test add spending with amount less then allowed")
])
def test_add_spend_with_invalid_min_amount(
        spend_client: SpendApiClient,
        spend_db: SpendDB,
        amount: str,
        category: str,
        spend_date: str,
        currency: str,
        description: str,
):
    with allure.step('Retrieve before spending count before from API'):
        before_get_all_spends = spend_client.get_all_spends()
        before_spending_count = len(before_get_all_spends)

    with (allure.step('Retrieve before spending count from DB')):
        before_db_spending_count = spend_db.get_spend_count()

    with (allure.step(f'Send request for added spending with amount less then allowed: amount={amount}')):
        future_spend = spend_client.add_spend_error(SpendModelAdd(
            amount=float(amount),
            category={"name": category},
            description=description,
            currency=currency,
            spendDate=spend_date
        ).model_dump())

    with allure.step('Retrieve after spending count from API'):
        after_get_all_spends = spend_client.get_all_spends()
        after_spending_count = len(after_get_all_spends)

    with (allure.step('Retrieve after spending count from DB')):
        after_db_spending_count = spend_db.get_spend_count()

    with allure.step('Assert future spending does not added'):
        with allure.step('Verify response for added future spending'):
            assert future_spend.type == "niffler-gateway: Entity validation error"
            assert future_spend.title == "Bad Request"
            assert future_spend.status == 400
            assert future_spend.detail == "Amount should be greater than 0.01"
            assert future_spend.instance == "/api/spends/add"
        with allure.step('Verify before spending count = after spending count from API'):
            assert before_spending_count == after_spending_count
        with allure.step('Verify before spending count = after spending count in DB'):
            assert before_db_spending_count == after_db_spending_count