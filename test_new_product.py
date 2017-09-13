import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec



@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_add_new_product(driver):
    login_to_admin_page(driver)
    """
Stwórz scenariusz dodania nowego artykułu (produktu) w aplikacji litecart (przez panel administracyjny).

Aby dodać przedmiot należy otworzyć menu Catalog, kliknąć w przycisk Add New Product znajdujący w prawym górnym rogu, wypełnić pola z informacją o artykule i zapisać.

Wystarczy wypełnić tylko informacje na kartach General, Information i Prices. Na tej ostatniej nie ma potrzeby dodawania rabatu (Compains).

Po zapisaniu artykułu w panelu administracyjnym należy upewnić się, że pojawił się w katalogu.

W części sklepu, przeznaczonej dla klientów nie trzeba tego sprawdzać.

Możesz przygotować scenariusz jako test, albo jako oddzielny plik wykonywalny.
"""


def login_to_admin_page(driver):
    driver.get("http://localhost:8080/litecart/admin/")
    driver.find_element_by_xpath("//input[@name='username']").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    wait(driver).until(ec.title_is("My Store"))


def wait(driver):
    waiter = WebDriverWait(driver, 10)
    return waiter


__author__ = "Grzegorz Holak"
