import allure
import pytest
from typing import Callable
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.spend import SpendModelAdd


@allure.epic("Траты")
@allure.feature("Создание траты")
@allure.story("API")
@allure.tag("negative")
@allure.title("Пользователь не может добавить трату с датой в будущем")
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

    with allure.step('Получить количество трат до добавления из API'):
        before_get_all_spends = spend_client.get_all_spends()
        before_spending_count = len(before_get_all_spends)

    with allure.step('Получить количество трат до добавления из базы данных'):
        before_db_spending_count = spend_db.get_spend_count()

    with allure.step('Отправить запрос на добавление траты с будущей датой'):
        future_spend = spend_client.add_spend_error(SpendModelAdd(
            amount=float(amount),
            category={"name": category},
            description=description,
            currency=currency,
            spendDate=future_date
        ).model_dump())

    with allure.step('Получить количество трат после добавления из API'):
        after_get_all_spends = spend_client.get_all_spends()
        after_spending_count = len(after_get_all_spends)

    with allure.step('Получить количество трат после добавления из базы данных'):
        after_db_spending_count = spend_db.get_spend_count()

    with allure.step('Проверить, что трата с будущей датой не была добавлена'):
        with allure.step('Проверить тело ответа: код ошибки, сообщение и детали'):
            assert future_spend.type == "niffler-gateway: Entity validation error"
            assert future_spend.title == "Bad Request"
            assert future_spend.status == 400
            assert future_spend.detail == "Spend date must not be future or less than 01.01.1970"
            assert future_spend.instance == "/api/spends/add"
        with allure.step('Проверить, что количество трат в API не изменилось'):
            assert before_spending_count == after_spending_count
        with allure.step('Проверить, что количество трат в базе данных не изменилось'):
            assert before_db_spending_count == after_db_spending_count

@allure.epic("Траты")
@allure.feature("Создание траты")
@allure.story("API")
@allure.tag("negative")
@allure.title("Пользователь не может добавить трату с некорректной минимальной суммой")
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
    with allure.step('Получить количество трат до добавления из API'):
        before_get_all_spends = spend_client.get_all_spends()
        before_spending_count = len(before_get_all_spends)

    with allure.step('Получить количество трат до добавления из базы данных'):
        before_db_spending_count = spend_db.get_spend_count()

    with allure.step(f'Когда пользователь отправляет запрос на добавление траты с суммой меньше минимально допустимой: amount={amount}'):
        future_spend = spend_client.add_spend_error(SpendModelAdd(
            amount=float(amount),
            category={"name": category},
            description=description,
            currency=currency,
            spendDate=spend_date
        ).model_dump())

    with allure.step('Получить количество трат после добавления из API'):
        after_get_all_spends = spend_client.get_all_spends()
        after_spending_count = len(after_get_all_spends)

    with allure.step('Получить количество трат после добавления из базы данных'):
        after_db_spending_count = spend_db.get_spend_count()

    with allure.step('Тогда трата с некорректной суммой не добавляется'):
        with allure.step('Проверить тело ответа: код ошибки, сообщение и детали'):
            assert future_spend.type == "niffler-gateway: Entity validation error"
            assert future_spend.title == "Bad Request"
            assert future_spend.status == 400
            assert future_spend.detail == "Amount should be greater than 0.01"
            assert future_spend.instance == "/api/spends/add"
        with allure.step('Проверить, что количество трат в API не изменилось'):
            assert before_spending_count == after_spending_count
        with allure.step('Проверить, что количество трат в базе данных не изменилось'):
            assert before_db_spending_count == after_db_spending_count