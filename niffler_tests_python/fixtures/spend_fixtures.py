import json
import pytest
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any
from collections.abc import Generator
from pytest import FixtureRequest

from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.databases.spend_db import SpendModelDB
from niffler_tests_python.model.category import CategoryModel
from niffler_tests_python.model.spend import SpendModel, SpendModelAdd
from niffler_tests_python.databases.spend_db import  SpendDB
from niffler_tests_python.utils.jinja_renderer import render_spend_jinja_template


@pytest.fixture
def fill_spends(
        spend_client: SpendApiClient,
        spend_db: SpendDB
) -> Generator[list[SpendModel], Any, None]:
    # spends_path = Path(__file__).resolve().parents[1] / 'test_data' / 'spend_data.json'
    # with open(spends_path, 'r') as f:
    #     spends = json.load(f)
    # created_spend_ids = []
    # created_category_ids = []
    # for spend_item in spends:
    #     spend_model = SpendModelAdd(**spend_item)
    #     added_spend = spend_client.add_spend(spend_model)
    #     created_spend_ids.append(added_spend.id)
    #     created_category_ids.append(added_spend.category.id)
    # yield created_spend_ids
    # spend_client.delete_spend(created_spend_ids)
    # for category_id in created_category_ids:
    #     spend_db.delete_category(category_id)



    # spends_path = Path(__file__).resolve().parents[1] / 'test_data' / 'spend_data.json'
    # with open(spends_path, 'r') as f:
    #     spends = json.load(f)
    rendered = render_spend_jinja_template('spend_data.json.j2')
    spends = json.loads(rendered)

    created_spends = []
    created_spend_ids = []
    created_category_ids = []
    for spend_item in spends:
        spend_model = SpendModelAdd(**spend_item)
        added_spend = spend_client.add_spend(spend_model)
        created_spends.append(added_spend)
        created_spend_ids.append(added_spend.id)
        created_category_ids.append(added_spend.category.id)
    yield created_spends
    spend_client.delete_spend(created_spend_ids)
    for category_id in created_category_ids:
        spend_db.delete_category(category_id)

@pytest.fixture
def filled_spends_contains_archived_category(fill_spends: list[SpendModel], category_client: CategoryApiClient) -> None:
    spend = fill_spends[0]
    category_client.update_category(CategoryModel(
        id=str(spend.category.id),
        name=spend.category.name,
        username=spend.username,
        archived=True
    ))

@pytest.fixture
def spend(request: FixtureRequest, spend_client: SpendApiClient, spend_db: SpendDB) -> Generator[SpendModel, Any, None]:
    added_spend = spend_client.add_spend(request.param)
    yield added_spend
    all_spends = spend_client.get_all_spends()
    spend_dict = {spend_item.id:spend_item for spend_item in all_spends}
    if added_spend.id in spend_dict:
        spend_client.delete_spend([added_spend.id])
        spend_db.delete_category(spend_dict[added_spend.id].category.id)
    spend_db.delete_category(added_spend.category.id)

@pytest.fixture
def custom_date_spend(request: FixtureRequest, spend_client: SpendApiClient, spend_db: SpendDB) -> Generator[tuple[SpendModel, dict[str, str]], dict, None]:
    spend_param = request.param
    period = spend_param["spendDate"]
    if period == "MONTH":
        actual_date = datetime.now().replace(day=1).date().isoformat()
        spend_param["spendDate"] = actual_date
    if period == 'WEEK':
        actual_date = (datetime.now() - timedelta(days=datetime.now().weekday())).date().isoformat()
        spend_param["spendDate"] = actual_date
    if period == 'TODAY':
        actual_date = datetime.now().date().isoformat()
        spend_param["spendDate"] = actual_date
    if period == 'ALL':
        actual_date = (datetime.now().replace(day=1) - timedelta(days=1)).date().isoformat()
        spend_param["spendDate"] = actual_date
    added_spend = spend_client.add_spend(SpendModelAdd(**spend_param))
    yield added_spend, {"period": period}
    spend_client.delete_spend([added_spend.id])
    spend_db.delete_category(added_spend.category.id)