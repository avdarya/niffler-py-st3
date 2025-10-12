import allure

from niffler_tests_python.web_pages.components.HeaderComponent import HeaderComponent
from niffler_tests_python.web_pages.MainPage import MainPage
from niffler_tests_python.web_pages.SpendingPage import SpendingPage


@allure.epic('Spending management')
@allure.feature('Spending creation')
@allure.story('Add empty spend')
def test_add_spending_with_empty_amount(
        main_page: MainPage,
        header: HeaderComponent,
        spending_page: SpendingPage
):
    with allure.step('Go to main page'):
        main_page.navigate()

    with allure.step('Click new spending button'):
        header.click_new_spending()

    with allure.step('Fill category input'):
        spending_page.fill_category('category test')

    with allure.step('Click add button'):
        spending_page.submit_form()

    with allure.step('Assert add empty spend'):
        with allure.step('Verify helper text for amount input'):
            spending_page.is_helper_text_amount_shown()

@allure.epic('Spending management')
@allure.feature('Spending creation')
@allure.story('Add empty spend')
def test_add_spending_with_empty_category(
        main_page: MainPage,
        header: HeaderComponent,
        spending_page: SpendingPage
):
    with allure.step('Go to main page'):
        main_page.navigate()

    with allure.step('Click new spending button'):
        header.click_new_spending()

    with allure.step('Fill amount input'):
        spending_page.fill_amount('10')

    with allure.step('Click add button'):
        spending_page.submit_form()

    with allure.step('Assert add empty spend'):
        with allure.step('Verify helper text for category input'):
            spending_page.is_helper_text_category_shown()
