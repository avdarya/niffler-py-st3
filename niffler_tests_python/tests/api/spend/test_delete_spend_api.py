import allure

from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.rest_model.spend import SpendModel
from niffler_tests_python.utils.marks import TestData


@allure.epic("Траты")
@allure.feature("Удаление трат")
@allure.story("API")
@allure.tag("positive")
@allure.title("Пользователь может удалить траты по списку и убедиться, что они отсутствуют в API и БД")
@TestData.fill_spends
def test_delete_spending_by_list(
        fill_spends: list[SpendModel],
        spend_client: SpendApiClient,
        spend_db: SpendDB
):
    with allure.step("Получить количество трат до удаления"):
        before_spends = spend_client.get_all_spends()
        before_spending_count = len(before_spends)

    spend_ids = [spend.id for spend in fill_spends]
    with allure.step("Отправить запрос на удаление списка трат"):
        spend_client.delete_spend(spend_ids)

    with allure.step("Получить количество и идентификаторы трат после удаления"):
        after_spending = spend_client.get_all_spends()
        after_spending_count = len(after_spending)
        after_spend_ids = [spend.id for spend in after_spending]

    with allure.step("Получить удалённые записи трат из базы данных"):
        db_spends = spend_db.get_spend_list(spend_ids)

    with allure.step("Проверить корректность удаления трат"):
        with allure.step("Количество трат до удаления минус удалённые равно количеству после"):
            assert before_spending_count - len(fill_spends) == after_spending_count
        with allure.step("Удалённые траты отсутствуют в API"):
            assert set(after_spend_ids).isdisjoint(spend_ids)
        with allure.step("Удалённые траты отсутствуют в БД"):
            assert len(db_spends) == 0