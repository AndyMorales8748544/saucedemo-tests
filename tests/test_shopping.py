"""Pruebas automatizadas de compras en SauceDemo."""

import pytest
from pages.checkout_page import CartPage, CheckoutPage
from pages.login_page import LoginPage


@pytest.mark.smoke
def test_tc05_agregar_productos(inventory):
    """TC-05: Verificar que dos productos se agreguen al carrito."""

    # Agregar el primer producto
    inventory.add_to_cart("Sauce Labs Backpack")

    # Agregar el segundo producto
    inventory.add_to_cart("Sauce Labs Bike Light")

    # Comprobar que el carrito muestre dos productos
    assert inventory.cart_count() == 2


@pytest.mark.regression
def test_tc06_eliminar_producto(inventory):
    """TC-06: Verificar que se pueda eliminar un producto del carrito."""

    # Agregar un producto al carrito
    inventory.add_to_cart("Sauce Labs Backpack")

    # Comprobar que el carrito tenga un producto
    assert inventory.cart_count() == 1

    # Eliminar el producto
    inventory.remove_from_cart("Sauce Labs Backpack")

    # Comprobar que el carrito esté vacío
    assert inventory.cart_count() == 0


@pytest.mark.regression
@pytest.mark.parametrize(
    "opcion",
    ["lohi", "hilo", "az", "za"],
)
def test_tc07_ordenar_productos(inventory, opcion):
    """TC-07: Verificar las cuatro opciones de ordenamiento."""

    # Seleccionar el ordenamiento
    inventory.sort_by(opcion)

    # Verificar el resultado según la opción seleccionada
    if opcion == "lohi":
        precios = inventory.prices()
        assert precios == sorted(precios)

    elif opcion == "hilo":
        precios = inventory.prices()
        assert precios == sorted(precios, reverse=True)

    elif opcion == "az":
        nombres = inventory.names()
        assert nombres == sorted(nombres)

    elif opcion == "za":
        nombres = inventory.names()
        assert nombres == sorted(nombres, reverse=True)


@pytest.mark.smoke
def test_tc08_compra_completa(inventory):
    """TC-08: Verificar el proceso completo de compra."""

    # Agregar un producto al carrito
    inventory.add_to_cart("Sauce Labs Backpack")
    assert inventory.cart_count() == 1

    # Abrir el carrito
    inventory.go_to_cart()

    # Comprobar el producto e iniciar checkout
    cart = CartPage(inventory.driver)
    assert cart.item_count() == 1
    cart.checkout()
    
    # Completar los datos del comprador
    checkout = CheckoutPage(inventory.driver)
    checkout.fill_info("Ana", "Pérez", "15073")

    # Comprobar que se muestre el total
    assert "Total:" in checkout.get_total()

    # Finalizar la compra
    checkout.finish()

    # Verificar el mensaje de confirmación
    assert checkout.get_confirmation() == "Thank you for your order!"


@pytest.mark.regression
@pytest.mark.parametrize(
    "nombre,apellido,codigo_postal,error_esperado",
    [
        ("", "Pérez", "15073", "First Name is required"),
        ("Ana", "", "15073", "Last Name is required"),
        ("Ana", "Pérez", "", "Postal Code is required"),
    ],
)
def test_tc09_campos_obligatorios_checkout(
    inventory, nombre, apellido, codigo_postal, error_esperado
):
    """TC-09: Validar los campos obligatorios del checkout."""

    # Agregar un producto y abrir el carrito
    inventory.add_to_cart("Sauce Labs Backpack")
    inventory.go_to_cart()

    # Iniciar el checkout
    cart = CartPage(inventory.driver)
    cart.checkout()

    # Completar el formulario con un campo vacío
    checkout = CheckoutPage(inventory.driver)
    checkout.fill_info(nombre, apellido, codigo_postal)

    # Comprobar el mensaje de error
    mensaje = checkout.get_error_message()
    assert error_esperado in mensaje


@pytest.mark.regression
def test_tc10_cierre_sesion(inventory):
    """TC-10: Verificar logout y protección de rutas."""

    # Cerrar sesión desde el inventario
    inventory.logout()

    # Comprobar que regresamos al login
    assert inventory.driver.current_url.rstrip("/") == (
        "https://www.saucedemo.com"
    )

    # Intentar acceder directamente al inventario
    inventory.driver.get(
        "https://www.saucedemo.com/inventory.html"
    )

    # Verificar que se impida el acceso sin sesión
    login = LoginPage(inventory.driver)
    mensaje = login.get_error_message()

    assert "You can only access '/inventory.html' when you are logged in." in mensaje
