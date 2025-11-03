import pytest
import allure

from niffler_tests_python.clients.graphql_client import GraphQLClient
from niffler_tests_python.databases.user_db import UserDB
from niffler_tests_python.utils.graphql_loader import load_graphql_query
from niffler_tests_python.utils.waiters import wait_until_timeout


@pytest.mark.parametrize("query_file, mutation_file, new_fullname", [
    ('user_query', 'user_mutation', 'new_fullname'),
])
@allure.epic("Профиль пользователя")
@allure.feature("Обновление данных пользователя")
@allure.story("GraphQL")
@allure.tag("positive")
@allure.title("Пользователь может обновить свои данные через GraphQL и проверить изменения в БД")
def test_update_userdata_graphql(
        user: tuple[str, str],
        graphql_client: GraphQLClient,
        user_db: UserDB,
        query_file: str,
        mutation_file: str,
        new_fullname: str,
):
    username, _ = user
    with allure.step("Отправить GraphQL-мутATION для обновления данных пользователя"):
        response = graphql_client.mutation_user(
            query=load_graphql_query(mutation_file),
            variables={"input":{"fullname": new_fullname}},
        )

    with allure.step("Ожидать обновление данных пользователя в БД"):
        db_user = wait_until_timeout(user_db.get_userdata_by_username)(username)

    with allure.step("Выполнить GraphQL-запрос для получения актуальных данных"):
        queried_user = graphql_client.query_user(
            query=load_graphql_query(query_file),
            variables={},
        )

    with allure.step("Проверить корректность данных пользователя в ответе и БД"):
        assert response.data.user.id == str(db_user.id)
        assert response.data.user.username == username
        assert queried_user.data.user.fullname == new_fullname
        assert response.data.user.fullname == new_fullname
