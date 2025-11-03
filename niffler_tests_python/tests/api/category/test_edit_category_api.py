import allure

from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.rest_model.category import CategoryModel
from niffler_tests_python.utils.marks import TestData
from niffler_tests_python.utils.helpers import get_category_by_name


@allure.epic("Траты")
@allure.feature("Редактирование категории")
@allure.story("API")
@allure.tag("positive")
@allure.title("Пользователь может редактировать категорию")
@TestData.category("category")
def test_edit_category(
        category: CategoryModel,
        category_client: CategoryApiClient,
        spend_db: SpendDB,
        new_category_name: str,
        user: tuple[str, str],
):
    username, _  = user

    with allure.step('Отправка запроса на изменение категории'):
        data_for_edit = CategoryModel(
            id=category.id,
            name=new_category_name,
            username=username,
            archived=not category.archived
        )
        edited_category = category_client.update_category(data_for_edit)

    with allure.step('Получение категории из API по новому имени'):
        api_category = get_category_by_name(new_category_name, category_client)

    with allure.step('Получение категории из БД по id'):
        db_category = spend_db.get_category_by_id(category.id)

    with allure.step('Проверка данных изменённой категории'):
        assert edited_category.name == new_category_name, f"Имя категории в ответе не соответствует ожидаемому: {edited_category.name} != {new_category_name}"
        assert edited_category.archived != category.archived, f"Статус archived в ответе не изменился: {edited_category.archived}"
        assert edited_category.username == username, f"Имя пользователя в ответе не соответствует ожидаемому: {edited_category.username} != {username}"

    with allure.step('Проверка данных категории в API'):
        assert api_category is not None, "Категория с новым именем не найдена в API"
        assert api_category.name == new_category_name, f"Имя категории в API не соответствует ожидаемому: {api_category.name} != {new_category_name}"
        assert api_category.archived != category.archived, f"Статус archived в API не изменился: {api_category.archived}"
        assert api_category.username == username, f"Имя пользователя в API не соответствует ожидаемому: {api_category.username} != {username}"

    with allure.step('Проверка данных категории в БД'):
        assert db_category is not None, "Категория не найдена в БД по id"
        assert db_category.name == new_category_name, f"Имя категории в БД не соответствует ожидаемому: {db_category.name} != {new_category_name}"
        assert db_category.archived != category.archived, f"Статус archived в БД не изменился: {db_category.archived}"
        assert db_category.username == username, f"Имя пользователя в БД не соответствует ожидаемому: {db_category.username} != {username}"