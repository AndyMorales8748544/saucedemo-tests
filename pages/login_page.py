"""Página de inicio de sesión de SauceDemo."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Representa el formulario de inicio de sesión."""

    USERNAME = (By.CSS_SELECTOR, '[data-test="username"]')
    PASSWORD = (By.CSS_SELECTOR, '[data-test="password"]')
    LOGIN_BUTTON = (By.CSS_SELECTOR, '[data-test="login-button"]')
    ERROR_MESSAGE = (By.CSS_SELECTOR, '[data-test="error"]')

    def open(self, url):
        """Abrir la página de SauceDemo."""
        self.driver.get(url)
        return self

    def login(self, username, password):
        """Ingresar las credenciales y presionar Login."""
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        """Obtener el mensaje de error del formulario."""
        return self.find(self.ERROR_MESSAGE).text
    