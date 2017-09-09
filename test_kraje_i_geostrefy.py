import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec



@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_countries(driver):
    login_to_admin_page(driver)
    driver.get("http://localhost:8080/litecart/admin/?app=countries&doc=countries")
    wait(driver).until(ec.title_contains("Countries | My Store"))
    lista_krajow = []
    for row in driver.find_elements_by_class_name("row"):
        lista_krajow.append(row.find_element_by_xpath(".//a").text)
    assert lista_krajow == sorted(lista_krajow)


def test_geozones(driver):
    login_to_admin_page(driver)
    driver.get("http://localhost:8080/litecart/admin/?app=geo_zones&doc=geo_zones")
    wait(driver).until(ec.title_contains("Geo Zones | My Store"))


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
