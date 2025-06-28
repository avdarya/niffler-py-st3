import json
import dotenv
import os
import pytest
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Any
from faker import Faker
from collections.abc import Generator
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options
from niffler_tests.clients.category_client import CategoryApiClient
from niffler_tests.clients.spend_client import SpendApiClient
from niffler_tests.clients.user_client import UserApiClient
from niffler_tests.config import Server
from niffler_tests.configuration.ConfigProvider import ConfigProvider
from niffler_tests.utils.base_session import BaseSession
from niffler_tests.web_pages.HeaderPage import HeaderPage
from niffler_tests.web_pages.LoginPage import LoginPage
from niffler_tests.web_pages.MainPage import MainPage
from niffler_tests.web_pages.ProfilePage import ProfilePage
from niffler_tests.web_pages.SpendingPage import SpendingPage

fake = Faker()

@pytest.fixture(scope="session")
def envs() -> None:
    dotenv.load_dotenv()

@pytest.fixture(scope="session")
def user_creds(envs) -> tuple[str, str]:
    return os.getenv("LOGIN"), os.getenv("PASSWORD")

def pytest_addoption(parser) -> None:
    parser.addoption("--env", default="dev")

@pytest.fixture(scope="session")
def env(request) -> str:
    return request.config.getoption("--env")

@pytest.fixture(scope="session")
def config() -> ConfigProvider:
    return ConfigProvider()

@pytest.fixture(scope="session")
def browser(config: ConfigProvider) -> Generator[WebDriver]:
    timeout = config.get_timeout()
    browser_name = config.get_prop("ui", "browser_name")

    if browser_name == 'chrome':
        service = ChromeService(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service)
    else:
        options = Options()
        options.page_load_strategy = 'normal'
        browser = webdriver.Firefox(options=options)

    browser.implicitly_wait(timeout)
    # browser.maximize_window()

    yield browser

    browser.quit()

@pytest.fixture(scope='session')
def login_page(browser: WebDriver, config: ConfigProvider) -> LoginPage:
    return LoginPage(browser, config)

@pytest.fixture(scope="session")
def auth_browser(browser: WebDriver, login_page: LoginPage, user_creds: tuple[str, str]) -> WebDriver:
    username, password = user_creds

    login_page.open()
    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_login_button()

    return browser

@pytest.fixture(scope="session")
def token(auth_browser: WebDriver) -> str:
    def token_present(driver: WebDriver) -> str:
        return auth_browser.execute_script('return window.localStorage.getItem("id_token")')

    token = WebDriverWait(auth_browser, 5).until(token_present)
    return token

@pytest.fixture(scope='session')
def main_page(auth_browser: WebDriver, config: ConfigProvider) -> MainPage:
    return MainPage(driver=auth_browser, config=config)

@pytest.fixture(scope='session')
def spending_page(auth_browser: WebDriver, config: ConfigProvider) -> SpendingPage:
    return SpendingPage(driver=auth_browser, config=config)

@pytest.fixture(scope='session')
def profile_page(auth_browser: WebDriver, config: ConfigProvider):
    return ProfilePage(driver=auth_browser, config=config)

@pytest.fixture(scope='session')
def header_page(auth_browser: WebDriver, config: ConfigProvider):
    return HeaderPage(driver=auth_browser, config=config)

@pytest.fixture(scope='function')
def go_to_main_page(main_page: MainPage):
    main_page.open()

@pytest.fixture(scope='function')
def go_to_profile_page(main_page: MainPage, profile_page: ProfilePage, header_page: HeaderPage):
    main_page.open()
    header_page.click_menu_button()
    header_page.click_profile()

@pytest.fixture(scope="session")
def base_session(env: str, token: str) -> BaseSession:
    base_url = Server(env).base_api_url
    return BaseSession(base_url=base_url, token=token)

@pytest.fixture(scope="session")
def user_client(base_session: BaseSession) -> UserApiClient:
    return UserApiClient(session=base_session)

@pytest.fixture(scope="session")
def category_client(base_session: BaseSession) -> CategoryApiClient:
    return CategoryApiClient(session=base_session)

@pytest.fixture(scope="session")
def spend_client(base_session: BaseSession) -> SpendApiClient:
    return SpendApiClient(session=base_session)

@pytest.fixture
def get_all_categories(category_client: CategoryApiClient, exclude_archived: bool | None) -> dict:
    response = category_client.get_all_categories(exclude_archived=exclude_archived)
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def add_category(category_client: CategoryApiClient) -> Generator[dict, Any, None]:
    category_name = fake.text(max_nb_chars=25).replace("\n", " ")
    response = category_client.add_category(category_name=category_name)
    assert response.status_code == 200
    body = response.json()
    yield body
    category_client.update_category(
        category_id=body["id"],
        category_name=fake.text().replace("\n", " "),
        archived=True,
    )

@pytest.fixture
def add_archive_category(add_category: dict, category_client: CategoryApiClient) -> Generator[dict, Any, None]:
    response = category_client.update_category(
        category_id=add_category["id"],
        category_name=add_category["name"],
        archived=True,
    )
    assert response.status_code == 200
    body = response.json()
    yield body
    category_client.update_category(
        category_id=body["id"],
        category_name=body["name"],
        archived=True,
    )

@pytest.fixture
def update_category(category_client: CategoryApiClient) -> Generator[dict, Any, None]:
    update_category = {
        "id": None,
        "name": "",
        "archived": True
    }

    yield update_category

    if update_category["id"] is None:

        all_categories = category_client.get_all_categories()
        assert all_categories.status_code == 200

        category_id = None
        for category in all_categories.json():
            if category["name"] == update_category["name"]:
                category_id = category["id"]
                break

        category_client.update_category(
            category_name=update_category["name"],
            category_id=category_id,
            archived=update_category["archived"]
        )
    else:

        category_client.update_category(
            category_name=update_category["name"],
            category_id=update_category["id"],
            archived=update_category["archived"]
        )

@pytest.fixture
def add_spend(spend_client: SpendApiClient, add_category: dict) -> Generator[dict, Any, None]:
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

@pytest.fixture
def add_custom_spend(
        request,
        spend_client: SpendApiClient,
        category_client: CategoryApiClient,
        update_category: dict,
):
    spend = request.param
    period = spend["spendDate"]
    if period == "MONTH":
        actual_date = datetime.now().replace(day=1).date().isoformat()
        spend["spendDate"] = actual_date
    if period == 'WEEK':
        actual_date = (datetime.now() - timedelta(days=datetime.now().weekday())).date().isoformat()
        spend["spendDate"] = actual_date
    if period == 'TODAY':
        actual_date = datetime.now().date().isoformat()
        spend["spendDate"] = actual_date
    if period == 'ALL':
        actual_date = (datetime.now().replace(day=1) - timedelta(days=1)).date().isoformat()
        spend["spendDate"] = actual_date
    response = spend_client.add_spending(spend)
    assert response.status_code == 201
    body = response.json()

    yield {**body, "period": period}

    spend_client.delete_spending([body["id"]])
    update_category["name"] = spend["category"]["name"]

@pytest.fixture
def fill_test_spend(
        spend_client: SpendApiClient,
        category_client: CategoryApiClient
) -> Generator[None, Any, None]:
    base_dir = Path(__file__).resolve().parent
    spends_path = base_dir.parent / 'spend_data.json'
    with open(spends_path, 'r') as f:
        spends = json.load(f)
    created_spend_id = []
    created_categories = {}
    for spend in spends:
        response = spend_client.add_spending(spend)
        assert response.status_code == 201
        body = response.json()
        created_spend_id.append(body["id"])
        created_categories[body["category"]["id"]] = body["category"]["name"]

    yield

    spend_client.delete_spending(created_spend_id)
    for category_id, name in created_categories.items():
        category_client.update_category(category_id=category_id, category_name=name, archived=True)

class Pages:
    go_to_profile_page = pytest.mark.usefixtures("go_to_profile_page")

class TestData:
    fill_test_spend = pytest.mark.usefixtures("fill_test_spend")
    add_custom_spend = lambda x: pytest.mark.parametrize(
        "add_custom_spend",
        [x],
        indirect=True,
        ids=lambda param: param["description"]
    )