import allure

from niffler_tests_python.web_pages.components.HeaderComponent import HeaderComponent
from niffler_tests_python.web_pages.MainPage import MainPage
from niffler_tests_python.web_pages.SpendingPage import SpendingPage


@allure.epic('Spending management')
@allure.feature('Spending creation')
@allure.story('Add empty spend')
def test_cancel_spending(
        main_page: MainPage,
        header: HeaderComponent,
        spending_page: SpendingPage
):
    with allure.step('Go to main page'):
        main_page.navigate()

    with allure.step('Click new spending button'):
        header.click_new_spending()

    with allure.step('Click cancel button'):
        spending_page.click_cancel()

    with allure.step('Verify go to /main page'):
        main_page.expected_url()




