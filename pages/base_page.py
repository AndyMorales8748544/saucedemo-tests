"""Clase base para interactuar con las páginas de SauceDemo."""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Funciones comunes para las páginas web."""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def find(self, locator):
        """Esperar hasta que un elemento sea visible."""
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    def click(self, locator):
        """Esperar y hacer clic en un elemento."""
        self.wait.until(
            EC.element_to_be_clickable(locator)
        ).click()

    def type(self, locator, text):
        """Limpiar un campo y escribir texto."""
        element = self.find(locator)
        element.clear()
        element.send_keys(text)
        