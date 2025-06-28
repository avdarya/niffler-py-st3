from niffler_tests.web_pages.HeaderPage import HeaderPage
from niffler_tests.web_pages.MainPage import MainPage
from niffler_tests.web_pages.SpendingPage import SpendingPage

def test_add_empty_spend(
        main_page: MainPage,
        header_page: HeaderPage,
        spending_page: SpendingPage,
        add_spend: dict
):
    main_page.open()

    header_page.click_new_spending()

    spending_page.click_save_spend()

    helper_text_amount = spending_page.helper_text_amount_input()
    helper_text_category = spending_page.helper_text_category_input()

    assert "Amount has to be not less then 0.01" in helper_text_amount
    assert "Please choose category" in helper_text_category
