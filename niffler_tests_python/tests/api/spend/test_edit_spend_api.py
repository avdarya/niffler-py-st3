import allure
import pytest
from datetime import datetime
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.enums.currency_title import CurrencyTitle
from niffler_tests_python.model.rest_model.spend import SpendModelAdd, SpendModel, SpendModelEdit
from niffler_tests_python.utils.marks import TestData


@allure.epic('Траты')
@allure.feature('Редактирование трат')
@allure.story('API')
@allure.tag('positive')
@allure.title('Пользователь может отредактировать трату и убедиться, что изменения корректно сохранены в API и БД')
@TestData.spend(SpendModelAdd(
    amount=203.01,
    description="test edit spend",
    currency=CurrencyTitle.USD,
    spendDate="2025-06-26",
    category={"name": "edit spend"}
))
@pytest.mark.parametrize("amount, currency, spend_date, description", [
    ("456", CurrencyTitle.EUR, "2025-07-09", "spending for update")
])
def test_edit_spend(
        spend: SpendModel,
        spend_client: SpendApiClient,
        spend_db: SpendDB,
        amount: str,
        currency: str,
        spend_date: str,
        description: str,
        user: tuple[str, str]
):
    username, _ = user
    expected_date = datetime.strptime(spend_date, "%Y-%m-%d").date()

    with allure.step('Отправить запрос на редактирование траты'):
        data_for_edit = SpendModelEdit(
            id=spend.id,
            amount=float(amount),
            category={"name": spend.category.name},
            description=description,
            currency=currency,
            spendDate=spend_date
        )
        edited_spend = spend_client.edit_spend(data_for_edit)

    with allure.step('Получить обновлённую информацию о трате из API'):
        api_spend = spend_client.get_spend_by_id(spend.id)

    with allure.step('Получить обновлённую запись о трате из базы данных'):
        db_spend = spend_db.get_spend(spend.id)

    with allure.step('Проверить корректность данных отредактированной траты в ответе'):
        assert edited_spend.amount == float(amount)
        assert edited_spend.category.name == spend.category.name
        assert edited_spend.category.username == username
        assert edited_spend.description == description
        assert edited_spend.currency == currency
        assert edited_spend.username == username
        assert edited_spend.spendDate.date() == expected_date

    with allure.step('Проверить корректность данных отредактированной траты в API'):
        assert api_spend.amount ==  float(amount)
        assert api_spend.category.name == spend.category.name
        assert api_spend.category.username == username
        assert api_spend.description == description
        assert api_spend.currency == currency
        assert api_spend.username == username
        assert api_spend.spendDate.date() == expected_date

    with allure.step('Проверить корректность данных отредактированной траты в базе данных'):
        assert db_spend.amount == float(amount)
        assert str(db_spend.category_id) == spend.category.id
        assert db_spend.description == description
        assert db_spend.currency == currency
        assert db_spend.username == username
        assert db_spend.spend_date == expected_date
