from unittest.mock import Mock

import pytest
import allure

from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.model.category import CategoryModel


@pytest.fixture
def client():
    client = CategoryApiClient(Mock())
    return client

@allure.epic("Категории")
@allure.feature("Получение списка категорий")
@allure.story("Unit")
@allure.tag("positive")
@allure.title("Проверка корректного парсинга категории в клиенте CategoryApiClient")
def test_category(client):
    with allure.step('Создаём мок-ответ API с одной категорией'):
        response = Mock()
        response.json.return_value = [{
                'id': '1',
                'name': 'Category1',
                'username': 'user1',
                'archived': False,
        }]
        client.session.get.return_value = response
    with allure.step('Вызываем метод get_all_categories() клиента'):
        categories = client.get_all_categories()
    with allure.step('Проверяем, что длина списка категорий равна 1'):
        assert len(categories) == 1
    with allure.step('Проверяем корректность данных категории'):
        assert categories == [CategoryModel(id='1', name='Category1', username='user1', archived=False)]