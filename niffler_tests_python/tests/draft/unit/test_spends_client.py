from unittest.mock import Mock

import pytest

from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.model.category import CategoryModel


@pytest.fixture
def client():
    client = CategoryApiClient(Mock())
    return client

def test_category(client):
    response = Mock()
    response.json.return_value = [{
            'id': '1',
            'name': 'Category1',
            'username': 'user1',
            'archived': False,
    }]
    client.session.get.return_value = response
    categories = client.get_all_categories()
    assert len(categories) == 1
    assert categories == [CategoryModel(id='1', name='Category1', username='user1', archived=False)]