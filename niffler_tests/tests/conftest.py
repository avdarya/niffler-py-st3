from datetime import datetime, timezone
from typing import Any

import dotenv
import pytest

from faker import Faker
from collections.abc import Generator

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options
from clients.categories_client import CategoriesApiClient
from clients.spend_client import SpendApiClient
from clients.user_client import UserApiClient
from config import Server
from configuration.ConfigProvider import ConfigProvider
from utils.base_session import BaseSession

fake = Faker()

@pytest.fixture(scope="session", autouse=True)
def envs() -> None:
    dotenv.load_dotenv()

def pytest_addoption(parser) -> None:
    parser.addoption("--env", default="dev")

@pytest.fixture(scope="session")
def env(request) -> str:
    return request.config.getoption("--env")

@pytest.fixture(scope="session")
def browser() -> Generator[WebDriver]:
    config = ConfigProvider()
    timeout = config.get_int("ui", "timeout")
    browser_name = config.get("ui", "browser_name")

    if browser_name == 'chrome':
        service = ChromeService(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service)
    else:
        options = Options()
        options.page_load_strategy = 'normal'
        browser = webdriver.Firefox(options=options)

    browser.implicitly_wait(timeout)
    browser.maximize_window()

    yield browser

    browser.quit()

@pytest.fixture(scope="session")
def config() -> ConfigProvider:
    return ConfigProvider()

@pytest.fixture(scope="session")
def base_session(env: str) -> BaseSession:
    return BaseSession(base_url=Server(env).base_api_url)

@pytest.fixture(scope="session")
def user_client(base_session: BaseSession) -> UserApiClient:
    return UserApiClient(session=base_session)

@pytest.fixture(scope="session")
def categories_client(base_session: BaseSession) -> CategoriesApiClient:
    return CategoriesApiClient(session=base_session)

@pytest.fixture(scope="session")
def spend_client(base_session: BaseSession) -> SpendApiClient:
    return SpendApiClient(session=base_session)

@pytest.fixture
def get_all_categories(categories_client: CategoriesApiClient, excludeArchived: bool | None) -> dict:
    response = categories_client.get_all_categories(excludeArchived=excludeArchived)
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def add_category(categories_client: CategoriesApiClient) -> Generator[dict, Any, None]:
    response = categories_client.add_category(category_name=fake.text(max_nb_chars=25).replace("\n", " "))
    assert response.status_code == 200
    body = response.json()

    yield body

    categories_client.update_category(
        category_id=body["id"],
        category_name=fake.text().replace("\n", " "),
        archived=True,
    )

@pytest.fixture
def update_category(categories_client: CategoriesApiClient) -> Generator[dict, Any, None]:
    update_category = {
        "id": None,
        "name": "",
        "archived": True
    }

    yield update_category

    if update_category["id"] is None:

        all_categories = categories_client.get_all_categories()
        assert all_categories.status_code == 200

        category_id = None
        for category in all_categories.json():
            if category["name"] == update_category["name"]:


                category_id = category["id"]
                break

        categories_client.update_category(
            category_name=update_category["name"],
            category_id=category_id,
            archived=update_category["archived"]
        )
    else:

        categories_client.update_category(
            category_name=update_category["name"],
            category_id=update_category["id"],
            archived=update_category["archived"]
        )

@pytest.fixture
def add_spending(spend_client: SpendApiClient, add_category: dict) -> Generator[dict, Any, None]:
    current_date = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    payload = {
        "amount": 1221.05,
        "currency": "RUB",
        "description": fake.text(max_nb_chars=10).replace("\n", " "),
        "spendDate": current_date,
        "category": {
            "name": add_category["name"]
            }
    }

    response = spend_client.add_spending(payload)
    assert response.status_code == 201
    body = response.json()

    yield body

    spend_client.delete_spending([body["id"]])