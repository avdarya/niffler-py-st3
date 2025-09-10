import allure

from niffler_tests_python.web_pages.components.Header import Header
from niffler_tests_python.web_pages.MainPage import MainPage
from niffler_tests_python.web_pages.SpendingPage import SpendingPage


@allure.epic('Spending management')
@allure.feature('Spending creation')
@allure.story('Add empty spend')
def test_add_empty_spend(main_page: MainPage, header: Header, spending_page: SpendingPage):
    with allure.step('Go to main page'):
        main_page.open()

    with allure.step('Click new spending button'):
        header.click_new_spending()

    with allure.step('Click add button'):
        spending_page.click_save_spend()

    with allure.step('Save helper text from spend form'):
        helper_text_amount = spending_page.helper_text_amount_input()
        helper_text_category = spending_page.helper_text_category_input()

    with allure.step('Assert add empty spend'):
        with allure.step('Verify helper text for amount input'):
            assert "Amount has to be not less then 0.01" in helper_text_amount
        with allure.step('Verify helper text for category input'):
            assert "Please choose category" in helper_text_category
