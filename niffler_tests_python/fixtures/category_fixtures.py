import json
import pytest
from typing import Any
from collections.abc import Generator
from pathlib import Path
from pytest import FixtureRequest
from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.databases.spend_db import SpendModelDB
from niffler_tests_python.model.category import CategoryModel


@pytest.fixture
def category(
        request: FixtureRequest,
        category_client: CategoryApiClient,
        spend_db: SpendModelDB
) -> Generator[CategoryModel, Any, None]:
    category_name = request.param
    api_current_categories = category_client.get_all_categories()
    current_categories = {category.name: category for category in api_current_categories}
    if category_name in current_categories:
        added_category = current_categories[category_name]
    else:
        added_category = category_client.add_category(category_name=category_name)
    yield added_category
    spend_db.delete_category(added_category.id)

@pytest.fixture
def archive_category(
        request: FixtureRequest,
        category_client: CategoryApiClient,
        spend_db: SpendModelDB
) -> Generator[CategoryModel, Any, None]:
    category_name = request.param
    api_current_categories = category_client.get_all_categories()
    current_categories = {category.name: category for category in api_current_categories}
    if category_name in current_categories:
        added_category = current_categories[category_name]
    else:
        added_category = category_client.add_category(category_name=category_name)
    added_category.archived = True
    archive_category = category_client.update_category(added_category)
    yield archive_category
    spend_db.delete_category(added_category.id)

@pytest.fixture
def fill_categories(
        category_client: CategoryApiClient,
        spend_db: SpendModelDB
) -> Generator[None, Any, None]:
    categories_path = Path(__file__).resolve().parents[1] / 'test_data' / 'category_data.json'
    with open(categories_path, 'r') as f:
        categories = json.load(f)
    created_category_ids = []
    for category_item in categories:
        added_category = category_client.add_category(category_item.get('name', None))
        created_category_ids.append(added_category.id)
    yield

    for category_id in created_category_ids:
        spend_db.delete_category(category_id)

@pytest.fixture
def two_categories(
        request: FixtureRequest,
        category_client: CategoryApiClient,
        spend_db: SpendModelDB
) -> Generator[tuple[CategoryModel, CategoryModel], Any, None]:
    name_1, name_2 = request.param

    api_current_categories = category_client.get_all_categories()
    existed_categories = {category.name: category for category in api_current_categories}

    if name_1 not in existed_categories:
        category_1 = category_client.add_category(name_1)
    else:
        category_1 = existed_categories[name_1]

    if name_2 not in existed_categories:
        category_2 = category_client.add_category(name_2)
    else:
        category_2 = existed_categories[name_2]

    yield category_1, category_2

    spend_db.delete_category(category_1.id)
    spend_db.delete_category(category_2.id)
