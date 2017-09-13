import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_register_new_user(driver):
    open_main_page(driver)
    """
1)    Rejestracja nowego konta z unikalnym adresem mailowym (tak, aby nie kolidował 
z wcześniej utworzonymi użytkownikami),

2)    Wylogowanie (logout), ponieważ po udanej rejestracji następuje automatyczne zalogowanie

3)    Ponowne zalogowanie na dopiero co utworzone konto

4)    Ponowne wylogowanie"""


def open_main_page(driver):
    driver.get("http://localhost:8080/litecart")
    wait(driver).until(ec.title_is("Online Store | My Store"))


def wait(driver):
    waiter = WebDriverWait(driver, 10)
    return waiter


__author__ = "Grzegorz Holak"
