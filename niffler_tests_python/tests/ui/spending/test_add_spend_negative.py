import allure

from niffler_tests_python.web_pages.components.HeaderComponent import HeaderComponent
from niffler_tests_python.web_pages.MainPage import MainPage
from niffler_tests_python.web_pages.SpendingPage import SpendingPage


@allure.epic("Траты")
@allure.feature("Создание траты")
@allure.story("UI")
@allure.tag("negative")
@allure.title("Создание траты без заполнения суммы")
def test_add_spending_with_empty_amount(
        main_page: MainPage,
        header: HeaderComponent,
        spending_page: SpendingPage
):
    with allure.step('Переход на главную страницу'):
        main_page.navigate()

    with allure.step('Нажимаем кнопку «Добавить трату»'):
        header.click_new_spending()

    with allure.step('Заполняем поле категории'):
        spending_page.fill_category('category test')

    with allure.step('Нажимаем кнопку «Добавить»'):
        spending_page.submit_form()

    with allure.step('Проверяем невозможность создания пустой траты'):
        with allure.step('Проверяем появление подсказки под полем суммы'):
            spending_page.is_helper_text_amount_shown()

@allure.epic("Траты")
@allure.feature("Создание траты")
@allure.story("UI")
@allure.tag("negative")
@allure.title("Создание траты без выбора категории")
def test_add_spending_with_empty_category(
        main_page: MainPage,
        header: HeaderComponent,
        spending_page: SpendingPage
):
    with allure.step('Переход на главную страницу'):
        main_page.navigate()

    with allure.step('Нажимаем кнопку «Добавить трату»'):
        header.click_new_spending()

    with allure.step('Заполняем поле суммы'):
        spending_page.fill_amount('10')

    with allure.step('Нажимаем кнопку «Добавить»'):
        spending_page.submit_form()

    with allure.step('Проверяем невозможность создания пустой траты'):
        with allure.step('Проверяем появление подсказки под полем категории'):
            spending_page.is_helper_text_category_shown()
