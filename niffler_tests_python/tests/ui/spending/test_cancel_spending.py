import allure

from niffler_tests_python.web_pages.components.HeaderComponent import HeaderComponent
from niffler_tests_python.web_pages.MainPage import MainPage
from niffler_tests_python.web_pages.SpendingPage import SpendingPage


@allure.epic("Траты")
@allure.feature("Создание траты")
@allure.story("UI")
@allure.tag("positive")
@allure.title("Отмена создания новой траты")
def test_cancel_spending(
        main_page: MainPage,
        header: HeaderComponent,
        spending_page: SpendingPage
):
    with allure.step('Переходим на главную страницу'):
        main_page.navigate()

    with allure.step('Нажимаем кнопку «Добавить трату»'):
        header.click_new_spending()

    with allure.step('Нажимаем кнопку «Отмена»'):
        spending_page.click_cancel()

    with allure.step('Проверяем, что произошел переход на главную страницу'):
        main_page.expected_url()
