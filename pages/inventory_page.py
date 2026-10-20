"""Página de inventario de SauceDemo."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Representa el inventario de productos."""

    TITLE = (By.CSS_SELECTOR, '[data-test="title"]')
    CART_BADGE = (By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')
    CART_LINK = (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')
    SORT_SELECT = (By.CSS_SELECTOR, '[data-test="product-sort-container"]')
    PRODUCT_NAMES = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
    PRODUCT_PRICES = (By.CSS_SELECTOR, '[data-test="inventory-item-price"]')

    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def get_title(self):
        """Obtener el título del inventario."""
        return self.find(self.TITLE).text

    def add_to_cart(self, product_name):
        """Agregar un producto al carrito."""
        product_id = product_name.lower().replace(" ", "-")
        locator = (By.CSS_SELECTOR, f'[data-test="add-to-cart-{product_id}"]')
        self.click(locator)

    def remove_from_cart(self, product_name):
        """Eliminar un producto del carrito."""
        product_id = product_name.lower().replace(" ", "-")
        locator = (By.CSS_SELECTOR, f'[data-test="remove-{product_id}"]')
        self.click(locator)

    def cart_count(self):
        """Obtener la cantidad de productos del carrito."""
        elements = self.driver.find_elements(*self.CART_BADGE)

        if not elements:
            return 0

        return int(elements[0].text)

    def go_to_cart(self):
        """Abrir el carrito de compras."""
        self.click(self.CART_LINK)

    def sort_by(self, option):
        """Ordenar los productos según la opción indicada."""
        select = Select(self.find(self.SORT_SELECT))
        select.select_by_value(option)

    def names(self):
        """Obtener los nombres de los productos."""
        elements = self.driver.find_elements(*self.PRODUCT_NAMES)
        return [element.text for element in elements]

    def prices(self):
        """Obtener los precios como números decimales."""
        elements = self.driver.find_elements(*self.PRODUCT_PRICES)
        return [float(element.text.replace("$", "")) for element in elements]

    def logout(self):
        """Cerrar la sesión del usuario."""
        self.click(self.MENU_BUTTON)

        # Esperar a que el menú lateral termine de abrirse
        self.wait.until(
            EC.visibility_of_element_located(self.LOGOUT_LINK)
        )

        # Cerrar sesión
        self.click(self.LOGOUT_LINK)

