import json
import allure
import dotenv
import os
import pytest
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any
from collections.abc import Generator

from _pytest.config import Config
from _pytest.main import Session
from allure_commons.reporter import AllureReporter
from allure_commons.types import AttachmentType
from allure_pytest.listener import AllureListener
from pytest import Item, FixtureDef, FixtureRequest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options
from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.clients.user_client import UserApiClient
from niffler_tests_python.config import Server
from niffler_tests_python.configuration.ConfigProvider import ConfigProvider
from niffler_tests_python.databases.spend_db import SpendModelDB, SpendDB
from niffler_tests_python.databases.userdata_db import UserdataDB
from niffler_tests_python.model.category import CategoryModel
from niffler_tests_python.model.config import Envs
from niffler_tests_python.model.spend import SpendModel, SpendModelAdd
from niffler_tests_python.utils.base_session import BaseSession
from niffler_tests_python.web_pages.components.Header import Header
from niffler_tests_python.web_pages.LoginPage import LoginPage
from niffler_tests_python.web_pages.MainPage import MainPage
from niffler_tests_python.web_pages.ProfilePage import ProfilePage
from niffler_tests_python.web_pages.SpendingPage import SpendingPage


def allure_logger(config) -> AllureReporter:
    listener: AllureListener = config.pluginmanager.get_plugin("allure_listener")
    return listener.allure_logger

def pytest_collection_modifyitems(session: Session, config: Config, items: list[Item]):
    for item in items:
        usefixtures_args = []
        for marker in item.iter_markers(name='usefixtures'):
            usefixtures_args.extend(marker.args)
        if usefixtures_args:
            item._fixture_tags = set(usefixtures_args)

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_setup(item: Item):
    for fx_name in getattr(item, '_fixture_tags', []):
        allure.dynamic.tag(f'@pytest.mark.usefixtures({fx_name})')
    yield

@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_call(item: Item):
    yield
    allure.dynamic.title(" ".join(item.name.split("_")[1:]).title())

    logger = allure_logger(item.config)
    test_result = logger.get_last_item()
    if test_result:
        test_result.labels = [
            lbl
            for lbl in test_result.labels
            if not (lbl.name == "tag" and "usefixtures" in lbl.value)
        ]

@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_fixture_setup(fixturedef: FixtureDef, request: FixtureRequest):
    yield
    logger = allure_logger(request.config)
    item = logger.get_last_item()
    scope_letter = fixturedef.scope[0].upper()
    item.name = f"[{scope_letter}] " + " ".join(fixturedef.argname.split("_")).title()

def pytest_addoption(parser) -> None:
    parser.addoption("--env", default="dev")

@pytest.fixture(scope="session")
def env(request: FixtureRequest) -> str:
    return request.config.getoption("--env")

@pytest.fixture(scope="session")
def config() -> ConfigProvider:
    return ConfigProvider()

@pytest.fixture(scope="session")
def envs(config: ConfigProvider) -> Envs:
    dotenv.load_dotenv()
    envs_instance = Envs(
        frontend_url=config.get_frontend_url(),
        # gateway_url=base_session.,
        spend_db_url=os.getenv("SPEND_DB_URL"),
        userdata_db_url=os.getenv("USERDATA_DB_URL"),
        username=os.getenv("LOGIN"),
        password=os.getenv("PASSWORD"),
    )
    # allure.attach(envs_instance.model_dump_json(indent=2), name='envs.json', attachment_type=AttachmentType.JSON)
    return envs_instance

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
    browser.maximize_window()

    yield browser

    browser.quit()

@pytest.fixture(scope='session')
def login_page(browser: WebDriver, config: ConfigProvider) -> LoginPage:
    return LoginPage(browser, config)

@pytest.fixture(scope="session")
def auth_browser(browser: WebDriver, login_page: LoginPage, envs: Envs) -> WebDriver:
    login_page.open()
    login_page.enter_username(envs.username)
    login_page.enter_password(envs.password)
    login_page.click_login_button()
    return browser

@pytest.fixture(scope="session")
def token(auth_browser: WebDriver) -> str:
    def token_present(driver: WebDriver) -> str:
        return auth_browser.execute_script('return window.localStorage.getItem("id_token")')
    token = WebDriverWait(auth_browser, 5).until(token_present)
    allure.attach(token, name='token.txt', attachment_type=AttachmentType.TEXT)
    return token

@pytest.fixture(scope='session')
def main_page(auth_browser: WebDriver, config: ConfigProvider) -> MainPage:
    return MainPage(driver=auth_browser, config=config)

@pytest.fixture(scope='session')
def spending_page(auth_browser: WebDriver, config: ConfigProvider) -> SpendingPage:
    return SpendingPage(driver=auth_browser, config=config)

@pytest.fixture(scope='session')
def profile_page(auth_browser: WebDriver, config: ConfigProvider) -> ProfilePage:
    return ProfilePage(driver=auth_browser, config=config)

@pytest.fixture(scope='session')
def header(auth_browser: WebDriver, config: ConfigProvider) -> Header:
    return Header(driver=auth_browser, config=config)

@pytest.fixture(scope='function')
def go_to_main_page(main_page: MainPage) -> None:
    main_page.open()

@pytest.fixture(scope='function')
def go_to_main_page_after_spend(main_page: MainPage, spend: SpendModel) -> None:
    main_page.open()

@pytest.fixture(scope='function')
def go_to_main_page_after_fill_spends(main_page: MainPage, fill_spends: SpendModel) -> None:
    main_page.open()

@pytest.fixture(scope='function')
def go_to_profile_page(main_page: MainPage, profile_page: ProfilePage, header: Header) -> None:
    main_page.open()
    header.click_menu_button()
    header.click_profile()

@pytest.fixture(scope='function')
def go_to_profile_after_category(
        main_page: MainPage,
        profile_page: ProfilePage,
        header: Header,
        category: CategoryModel
) -> None:
    main_page.open()
    header.click_menu_button()
    header.click_profile()

@pytest.fixture(scope="session")
def base_session(env: str, token: str) -> BaseSession:
    gateway_url = Server(env).gateway_url
    return BaseSession(gateway_url=gateway_url, token=token)

@pytest.fixture(scope="session")
def user_client(base_session: BaseSession) -> UserApiClient:
    return UserApiClient(session=base_session)

@pytest.fixture(scope="session")
def category_client(base_session: BaseSession) -> CategoryApiClient:
    return CategoryApiClient(session=base_session)

@pytest.fixture(scope="session")
def spend_client(base_session: BaseSession) -> SpendApiClient:
    return SpendApiClient(session=base_session)

@pytest.fixture(scope="session")
def spend_db(envs) -> SpendDB:
    return SpendDB(db_url=envs.spend_db_url)

@pytest.fixture(scope="session")
def userdata_db(envs) -> UserdataDB:
    return UserdataDB(db_url=envs.userdata_db_url)

@pytest.fixture
def category(request: FixtureRequest, category_client: CategoryApiClient, spend_db: SpendModelDB) -> Generator[CategoryModel, Any, None]:
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
    base_dir = Path(__file__).resolve().parent
    spends_path = base_dir.parent / 'spend_data.json'
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

class Pages:
    go_to_main_page = pytest.mark.usefixtures("go_to_main_page")
    go_to_main_page_after_spend = pytest.mark.usefixtures("go_to_main_page_after_spend")
    go_to_main_page_after_fill_spends = pytest.mark.usefixtures("go_to_main_page_after_fill_spends")
    go_to_profile_page = pytest.mark.usefixtures("go_to_profile_page")
    go_to_profile_after_category = pytest.mark.usefixtures("go_to_profile_after_category")

class TestData:
    fill_spends = pytest.mark.usefixtures("fill_spends")
    category = lambda x: pytest.mark.parametrize("category", [x], indirect=True)
    archive_category = lambda x: pytest.mark.parametrize("archive_category", [x], indirect=True)
    spend = lambda x: pytest.mark.parametrize(
        "spend",
        [x],
        indirect=True,
        ids=lambda param: param.description
    )
    custom_date_spend = lambda x: pytest.mark.parametrize(
        "custom_date_spend",
        [x],
        indirect=True,
        ids=lambda param: param.description
    )
