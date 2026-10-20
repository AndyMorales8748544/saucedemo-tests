"""Pruebas automatizadas del inicio de sesión de SauceDemo."""

import pytest
import time

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@pytest.mark.smoke
def test_tc01_login_exitoso(driver):
    """TC-01: Verificar inicio de sesión con credenciales válidas."""

    # Abrir SauceDemo
    login = LoginPage(driver)
    login.open("https://www.saucedemo.com")

    # Iniciar sesión
    login.login("standard_user", "secret_sauce")

    # Comprobar la dirección de la página
    assert driver.current_url.endswith("/inventory.html")

    # Comprobar el título del inventario
    inventory = InventoryPage(driver)
    assert inventory.get_title() == "Products"


@pytest.mark.regression
def test_tc02_usuario_bloqueado(driver):
    """TC-02: Verificar que un usuario bloqueado no pueda iniciar sesión."""

    # Abrir SauceDemo
    login = LoginPage(driver)
    login.open("https://www.saucedemo.com")

    # Intentar iniciar sesión con un usuario bloqueado
    login.login("locked_out_user", "secret_sauce")

    # Comprobar el mensaje de error
    mensaje = login.get_error_message()

    assert "Sorry, this user has been locked out." in mensaje


@pytest.mark.regression
@pytest.mark.parametrize(
    "usuario,contrasena",
    [
        ("standard_user", "clave_incorrecta"),
        ("usuario_inexistente", "secret_sauce"),
    ],
)
def test_tc03_credenciales_incorrectas(driver, usuario, contrasena):
    """TC-03: Verificar el rechazo de credenciales incorrectas."""

    # Abrir SauceDemo
    login = LoginPage(driver)
    login.open("https://www.saucedemo.com")

    # Intentar iniciar sesión
    login.login(usuario, contrasena)

    # Obtener el mensaje de error
    mensaje = login.get_error_message()

    # Comprobar que las credenciales fueron rechazadas
    assert "Username and password do not match" in mensaje


@pytest.mark.regression
@pytest.mark.parametrize(
    "usuario,contrasena,error_esperado",
    [
        ("", "secret_sauce", "Username is required"),
        ("standard_user", "", "Password is required"),
    ],
)
def test_tc04_campos_obligatorios(
    driver, usuario, contrasena, error_esperado
):
    """TC-04: Validar los campos obligatorios del login."""

    # Abrir SauceDemo
    login = LoginPage(driver)
    login.open("https://www.saucedemo.com")

    # Intentar iniciar sesión con un campo vacío
    login.login(usuario, contrasena)

    # Obtener el mensaje de error
    mensaje = login.get_error_message()

    # Verificar que aparezca el error correspondiente
    assert error_esperado in mensaje


@pytest.mark.regression
def test_tc11_tiempo_inicio_sesion(driver):
    """TC-11: Verificar que el login tarde menos de 5 segundos."""

    # Abrir la página de inicio de sesión
    login = LoginPage(driver)
    login.open("https://www.saucedemo.com")

    # Completar las credenciales
    login.type(login.USERNAME, "standard_user")
    login.type(login.PASSWORD, "secret_sauce")

    # Iniciar la medición
    inicio = time.perf_counter()

    # Presionar el botón Login
    login.click(login.LOGIN_BUTTON)

    # Esperar hasta visualizar el inventario
    inventory = InventoryPage(driver)
    assert inventory.get_title() == "Products"

    # Calcular el tiempo transcurrido
    duracion = time.perf_counter() - inicio

    print(f"Tiempo de inicio de sesión: {duracion:.2f} segundos")

    # Comprobar el límite de 5 segundos
    assert duracion < 5, (
        f"El inicio de sesión tardó {duracion:.2f} segundos"
    )


@pytest.mark.regression
def test_tc12_compatibilidad_navegadores(driver):
    """TC-12: Verificar el login en distintos navegadores."""

    # Abrir SauceDemo
    login = LoginPage(driver)
    login.open("https://www.saucedemo.com")

    # Iniciar sesión
    login.login("standard_user", "secret_sauce")

    # Comprobar que se muestra el inventario
    inventory = InventoryPage(driver)

    assert inventory.get_title() == "Products"
    assert driver.current_url.endswith("/inventory.html")