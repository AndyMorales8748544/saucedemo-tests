"""Páginas del carrito y checkout de SauceDemo."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    """Representa el carrito de compras."""

    CART_ITEMS = (By.CSS_SELECTOR, '[data-test="inventory-item"]')
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, '[data-test="checkout"]')

    def item_count(self):
        """Obtener la cantidad de productos en el carrito."""
        self.find((By.CSS_SELECTOR, '[data-test="cart-list"]'))
        elements = self.driver.find_elements(*self.CART_ITEMS)
        return len(elements)

    def checkout(self):
        """Iniciar el proceso de compra."""
        self.click(self.CHECKOUT_BUTTON)


class CheckoutPage(BasePage):
    """Representa el formulario y la confirmación de compra."""

    FIRST_NAME = (By.CSS_SELECTOR, '[data-test="firstName"]')
    LAST_NAME = (By.CSS_SELECTOR, '[data-test="lastName"]')
    POSTAL_CODE = (By.CSS_SELECTOR, '[data-test="postalCode"]')

    CONTINUE_BUTTON = (By.CSS_SELECTOR, '[data-test="continue"]')
    FINISH_BUTTON = (By.CSS_SELECTOR, '[data-test="finish"]')

    TOTAL = (By.CSS_SELECTOR, '[data-test="total-label"]')
    ERROR_MESSAGE = (By.CSS_SELECTOR, '[data-test="error"]')
    CONFIRMATION = (By.CSS_SELECTOR, '[data-test="complete-header"]')

    def fill_info(self, first_name, last_name, postal_code):
        """Completar los datos del comprador."""
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.POSTAL_CODE, postal_code)
        self.click(self.CONTINUE_BUTTON)

    def get_total(self):
        """Obtener el importe total de la compra."""
        return self.find(self.TOTAL).text

    def finish(self):
        """Finalizar la compra."""
        self.click(self.FINISH_BUTTON)

    def get_confirmation(self):
        """Obtener el mensaje de confirmación."""
        return self.find(self.CONFIRMATION).text

    def get_error_message(self):
        """Obtener el mensaje de validación del formulario."""
        return self.find(self.ERROR_MESSAGE).text
    