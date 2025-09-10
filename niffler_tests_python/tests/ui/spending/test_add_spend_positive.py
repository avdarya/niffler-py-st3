# +
test_spending_navigation
def test_navigation_main_to_spending_and_back(main_page, header, spending_page):
    expect(main_page.page).to_have_url(/main)
    header.click_new_spending()
    expect(spending_page.page).to_have_url(/spending)

    # заполнение минимальными валидными данными
    spending_page.enter_amount_input("10")
    spending_page.click_currency_input(); spending_page.click_currency_value("RUB")
    spending_page.click_category("Food")
    spending_page.enter_date_input("09/06/2025")
    spending_page.enter_description_input("smoke")
    spending_page.click_save_spend()

    expect(main_page.page).to_have_url(/main)


# -