from niffler_tests_python.configuration.ConfigProvider import ConfigProvider
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:

    __driver: WebDriver
    __url: str
    __timeout: float

    def __init__(self, driver: WebDriver, config: ConfigProvider):
        self.__driver = driver
        self.__url = config.get_frontend_auth_url() + "/login"
        self.__timeout = config.get_timeout()

    def open(self) -> None:
        self.__driver.get(self.__url)

    def enter_username(self, username: str) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'input[name="username"]').send_keys(username)

    def enter_password(self, password: str) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'input[name="password"').send_keys(password)

    def click_login_button(self) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'button[type="submit"').click()
        WebDriverWait(self.__driver, self.__timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'img[alt="Niffler logo"]'))
        )
