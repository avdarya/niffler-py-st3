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
from niffler_tests_python.model.spend import SpendModel, SpendModelAdd
from niffler_tests_python.web_pages.MainPage import MainPage


@pytest.fixture(scope='function')
def go_to_main_page_after_fill_spends(main_page: MainPage, fill_spends: SpendModel) -> None:
    main_page.open()

@pytest.fixture
def custom_date_spend(request: FixtureRequest, spend_client: SpendApiClient, spend_db: SpendModelDB) -> Generator[tuple[SpendModel, dict[str, str]], dict, None]:
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

@pytest.fixture
def fill_spends(
        spend_client: SpendApiClient,
        category_client: CategoryApiClient,
        spend_db: SpendModelDB
) -> Generator[None, Any, None]:
    spends_path = Path(__file__).resolve().parent.parent.parent.parent / 'spend_data.json'
    with open(spends_path, 'r') as f:
        spends = json.load(f)
    created_spend_ids = []
    created_category_ids = []
    for spend_item in spends:
        spend_model = SpendModelAdd(**spend_item)
        added_spend = spend_client.add_spend(spend_model)
        created_spend_ids.append(added_spend.id)
        created_category_ids.append(added_spend.category.id)
    yield
    spend_client.delete_spend(created_spend_ids)
    for category_id in created_category_ids:
        spend_db.delete_category(category_id)