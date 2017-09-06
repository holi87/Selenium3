import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec



@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd



def test_number_of_stickers(driver):
    open_main_page(driver)
    lista_produktow = driver.find_elements_by_css_selector("li[class='product column shadow hover-light']")
    #  print(len(lista_produktow))
    for element in lista_produktow:
        tmp = element.find_elements_by_css_selector("div[class^='sticker']")
        #  print(len(tmp))
        assert len(tmp) == 1
"""
check amount of products and make loop in list of them to:
check if every product has exactly one sticker

"""

def open_main_page(driver):
    driver.get("http://localhost:8080/litecart")
    wait(driver).until(ec.title_is("Online Store | My Store"))


def wait(driver):
    waiter = WebDriverWait(driver, 10)
    return waiter


__author__ = "Grzegorz Holak"
