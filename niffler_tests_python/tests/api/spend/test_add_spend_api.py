import allure
import pytest
from datetime import datetime
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.rest_model.category import CategoryModel
from niffler_tests_python.model.rest_model.spend import SpendModelAdd
from niffler_tests_python.utils.marks import TestData


@allure.epic("Траты")
@allure.feature("Создание траты")
@allure.story("API")
@allure.tag("positive")
@allure.title("Пользователь может создать новую трату")
@TestData.category("add spend")
@pytest.mark.parametrize("amount, currency, spend_date, description", [
    ("10.01", "RUB", "2024-12-09", "test add spending"),
    ("501", "KZT", "2025-01-15", "test add spending"),
    ("0.01", "EUR", "2025-04-09", "test add spending"),
    ("3", "USD", "2025-07-09", "test add spending")
])
def test_add_spending_and_verifydata(
        spend_client: SpendApiClient,
        category: CategoryModel,
        spend_db: SpendDB,
        amount: str,
        currency: str,
        spend_date: str,
        description: str,
        user: tuple[str, str]
):
    username, _ = user
    expected_date = datetime.strptime(spend_date, "%Y-%m-%d").date()

    with allure.step("Получить количество трат до добавления"):
        before_get_all_spends = spend_client.get_all_spends()
        before_spending_count = len(before_get_all_spends)

    with allure.step("Отправить запрос на добавление новой траты"):
        added_spend = spend_client.add_spend(SpendModelAdd(
            amount=float(amount),
            category={"id": category.id, "name": category.name, "username": category.username},
            description=description,
            currency=currency,
            spendDate=spend_date
        ))

    with allure.step("Получить количество трат после добавления"):
        after_get_all_spends = spend_client.get_all_spends()
        after_spending_count = len(after_get_all_spends)

    with allure.step("Проверить, что количество трат увеличилось на 1"):
        assert before_spending_count == after_spending_count - 1

    with allure.step("Получить данные добавленной траты из API"):
        api_spend = spend_client.get_spend_by_id(added_spend.id)

    with allure.step("Получить данные добавленной траты из базы данных"):
        db_spend = spend_db.get_spend(added_spend.id)
        db_spend_date = datetime.combine(db_spend.spend_date, datetime.min.time()).date()

    with allure.step("Удалить созданную трату и категорию из системы"):
        spend_client.delete_spend([api_spend.id])
        spend_db.delete_category(category.id)

    with allure.step("Проверить корректность данных созданной траты в ответе API"):
        assert added_spend.amount == float(amount)
        assert added_spend.category.name == category.name
        assert added_spend.category.username == username
        assert added_spend.description == description
        assert added_spend.currency == currency
        assert added_spend.username == username
        assert added_spend.spendDate.date() == expected_date

    with allure.step("Проверить корректность данных созданной траты при запросе через API"):
        assert api_spend.amount == float(amount)
        assert api_spend.category.name == category.name
        assert api_spend.category.username == username
        assert api_spend.description == description
        assert api_spend.currency == currency
        assert api_spend.username == username
        assert api_spend.spendDate.date() == expected_date

    with allure.step("Проверить корректность данных созданной траты в БД"):
        assert db_spend.amount == float(amount)
        assert str(db_spend.category_id) == category.id
        assert db_spend.description == description
        assert db_spend.currency == currency
        assert db_spend.username == username
        assert db_spend_date == expected_date