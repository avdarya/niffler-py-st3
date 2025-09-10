import allure

from niffler_tests_python.databases.auth_db import AuthDB
from niffler_tests_python.databases.userdata_db import UserdataDB
from niffler_tests_python.utils.waiters import wait_until_timeout
from niffler_tests_python.web_pages.MainPage import MainPage
from niffler_tests_python.web_pages.RegisterPage import RegisterPage
from niffler_tests_python.web_pages.SpendingPage import SpendingPage


@allure.epic("Spending management")
@allure.feature("Spending creation")
@allure.story("Positive")
@allure.title("E2E: Создание траты → запись в БД и отображение траты на странице /main")
def test_add_spend_e2e(
    main_page: MainPage,
    spending_page: SpendingPage,
):