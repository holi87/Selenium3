import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_logs_in_catalogs_admin_page(driver):
    login_to_admin_page(driver)
    go_to_catalog_page(driver)
    open_all_subcategories(driver)
    go_through_products(driver)


def go_through_products(driver):
    products = driver.find_elements_by_css_selector("table.dataTable tr.row td:nth-child(3) a[href*='product_id=']")
    for i in range(len(products)):
        driver.find_elements_by_css_selector("table.dataTable tr.row td:nth-child(3) a[href*='product']")[i].click()
        print_browser_logs(driver)
        wait(driver).until(ec.element_to_be_clickable((By.NAME, "cancel")))  # wait for cancel button
        driver.execute_script("history.go(-1);")


def print_browser_logs(driver):
    for l in driver.get_log("browser"):
        print(l)


def open_all_subcategories(driver):  # could make it as for loop and open all subcategories, but it's not scope of task
    try:
        driver.find_element_by_link_text("Rubber Ducks").click()
        wait(driver).until(ec.element_to_be_clickable((By.LINK_TEXT, "Subcategory")))
        driver.find_element_by_link_text("Subcategory").click()
    except NoSuchElementException:
        pass


def go_to_catalog_page(driver):
    driver.find_element_by_link_text("Catalog").click()
    wait(driver).until(ec.title_contains("Catalog"))


def login_to_admin_page(driver):
    driver.get("http://localhost:8080/litecart/admin/")
    driver.find_element_by_xpath("//input[@name='username']").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    wait(driver).until(ec.title_is("My Store"))


def wait(driver):
    waiter = WebDriverWait(driver, 10)
    return waiter


'''

for l in driver.get_log("browser"):
    print(l)
'''


__author__ = "Grzegorz Holak"
