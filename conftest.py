"""Configuración de pytest para SauceDemo."""

import pytest
from pathlib import Path
from selenium import webdriver

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


BASE_URL = "https://www.saucedemo.com"
PASSWORD = "secret_sauce"
SCREENSHOTS = Path("reports/screenshots")


def pytest_addoption(parser):
    """Agregar opciones personalizadas para ejecutar pruebas."""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox", "edge"],
        help="Navegador para ejecutar las pruebas"
    )

    parser.addoption(
        "--headless",
        action="store_true",
        help="Ejecutar sin mostrar el navegador"
    )

    parser.addoption(
        "--grid-url",
        action="store",
        default=None,
        help="Dirección del servidor Selenium Grid"
    )


@pytest.fixture
def driver(request):
    """Crear y cerrar un navegador por cada prueba."""
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    grid_url = request.config.getoption("--grid-url")

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1366,768")
        
        options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        })

        if headless:
            options.add_argument("--headless=new")

        factory = webdriver.Chrome

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("-headless")

        factory = webdriver.Firefox

    else:
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument("--headless=new")

        factory = webdriver.Edge

    if grid_url:
        navegador = webdriver.Remote(   # pylint: disable=not-callable
            command_executor=grid_url,
            options=options
        )
    else:
        navegador = factory(options=options)  # pylint: disable=not-callable

    try:
        yield navegador
    finally:
        navegador.quit()


@pytest.fixture
def inventory(driver): # pylint: disable=redefined-outer-name
    """Iniciar sesión y devolver la página de inventario."""
    login = LoginPage(driver).open(BASE_URL)
    login.login("standard_user", PASSWORD)

    inventario = InventoryPage(driver)
    assert inventario.get_title() == "Products"

    return inventario


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        if "driver" in item.fixturenames:
            navegador = item.funcargs.get("driver")

            if navegador is not None:
                SCREENSHOTS.mkdir(parents=True, exist_ok=True)

                nombre = "".join(
                    c if c.isalnum() or c in "-_." else "_"
                    for c in item.name
                )

                ruta = SCREENSHOTS / f"{nombre}.png"
                navegador.save_screenshot(str(ruta))

                print(f"\nCaptura de error guardada en: {ruta}")
