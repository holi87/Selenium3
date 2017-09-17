import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


@pytest.fixture
def driver(request):
    wd = webdriver.Firefox()
    request.addfinalizer(wd.quit)
    return wd


def test_cart(driver):
    for i in range(3):
        open_main_page(driver)
        add_random_product_to_cart(driver)

    full_cart_quantity = check_number_of_items_in_cart(driver)
    go_to_cart(driver)
    remove_all_items_in_cart(driver, full_cart_quantity)

    wait(driver).until(ec.text_to_be_present_in_element((By.XPATH, "//p/em"), "There are no items in your cart."))


def remove_all_items_in_cart(driver, full_cart_quantity):
    for i in range(full_cart_quantity):
        driver.find_element_by_css_selector("button[name='remove_cart_item']").click()
        table_of_items = driver.find_elements_by_css_selector("td.item")
        wait(driver).until(ec.staleness_of(table_of_items[full_cart_quantity - i - 1]))


def go_to_cart(driver):
    driver.find_element_by_link_text("Checkout »").click()


def add_random_product_to_cart(driver):
    open_random_product_page(driver)
    prods_in_cart = check_number_of_items_in_cart(driver)
    select_size_if_exist(driver)
    add_to_cart(driver, prods_in_cart)


def add_to_cart(driver, prods_in_cart):
    driver.find_element_by_css_selector("button[name='add_cart_product']").click()
    wait(driver).until(ec.text_to_be_present_in_element((By.CSS_SELECTOR, "div#cart span.quantity")
                                                        , str(prods_in_cart + 1)))


def select_size_if_exist(driver):
    try:
        size = Select(driver.find_element_by_xpath("//select[@name='options[Size]']"))
        size.select_by_value(random.choice(["Small", "Medium", "Large"]))
    except NoSuchElementException:
        pass


def check_number_of_items_in_cart(driver):
    prods_in_cart = int(driver.find_element_by_css_selector("div#cart span.quantity").text)
    return prods_in_cart


def open_random_product_page(driver):
    products = driver.find_elements_by_xpath("//li[@class='product column shadow hover-light']")
    random_product = random.choice(products)
    random_product.click()


def open_main_page(driver):
    driver.get("http://localhost:8080/litecart")
    wait(driver).until(ec.title_is("Online Store | My Store"))


def wait(driver):
    waiter = WebDriverWait(driver, 10)
    return waiter


__author__ = "Grzegorz Holak"
