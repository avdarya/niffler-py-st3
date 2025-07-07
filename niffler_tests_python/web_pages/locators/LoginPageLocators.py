from selenium.webdriver.common.by import By

class LoginPageLocators:
    USERNAME_INPUT = (By.CSS_SELECTOR, 'input[name="username"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, 'input[name="password"]')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')
    NIFFLER_LOGO = (By.CSS_SELECTOR, 'img[alt="Niffler logo"]')