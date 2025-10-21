import allure
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.spend import SpendModelAdd, SpendModel
from niffler_tests_python.utils.marks import  TestData


@allure.epic('Траты')
@allure.feature('Получение трат')
@allure.story('API')
@allure.tag('positive')
@allure.title('Пользователь может получить данные траты по ID и убедиться в корректности информации в API и БД')
@TestData.spend(SpendModelAdd(
    amount=203.01,
    description="test get spend by id",
    currency="USD",
    spendDate="2025-06-26T21:00:00.000+00:00",
    category={"name": "get spend by id"}
))
def test_get_spend_by_id(
        spend: SpendModel,
        spend_client: SpendApiClient,
        spend_db: SpendDB,
        user: tuple[str, str]
):
    username, _ = user
    with allure.step('Отправить запрос на получение траты по ID'):
        get_spend = spend_client.get_spend_by_id(spend.id)

    with allure.step('Получить данные траты из базы данных'):
        db_spend = spend_db.get_spend(spend.id)
        db_category = spend_db.get_category_by_id(db_spend.category_id)

    with allure.step('Проверить корректность данных траты, полученной по ID'):
        with allure.step('Проверить корректность данных в ответе API'):
            assert get_spend.id == spend.id
            assert get_spend.spendDate.date() == spend.spendDate.date()
            assert get_spend.category.name == spend.category.name
            assert get_spend.category.username == username
            assert get_spend.currency == spend.currency
            assert get_spend.amount == spend.amount
            assert get_spend.description == spend.description
            assert get_spend.username == username
        with allure.step('Проверить соответствие данных в базе данных'):
            assert get_spend.id == str(db_spend.id)
            assert get_spend.spendDate.astimezone().date() == db_spend.spend_date
            assert get_spend.category.name == db_category.name
            assert get_spend.category.username == db_category.username
            assert get_spend.category.archived == db_category.archived
            assert get_spend.category.id == str(db_spend.category_id)
            assert get_spend.currency == db_spend.currency
            assert get_spend.amount == db_spend.amount
            assert get_spend.description == db_spend.description
            assert get_spend.username == db_spend.username