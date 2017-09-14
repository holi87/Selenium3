import pytest
import random
import string
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_add_new_product(driver):
    login_to_admin_page(driver)
    go_to_add_new_product_page(driver)
    product_name = random_letters(20)
    fill_general(driver, product_name)
    fill_info(driver)
    fill_price(driver)
    save_product(driver)
    wait(driver).until(ec.title_contains("Catalog | My Store"))
    driver.find_element_by_link_text("Rubber Ducks").click()  # because added new product to this category
    assert driver.find_element_by_link_text(product_name), "product not found"


def save_product(driver):
    driver.find_element_by_xpath("//button[@name='save']").click()


def fill_price(driver):
    element = driver.find_element_by_xpath("//a[@href='#tab-prices']")
    driver.execute_script("arguments[0].click();", element)
    price = random_number(5) + "," + random_number(2)
    driver.find_element_by_name("purchase_price").clear()
    driver.find_element_by_name("purchase_price").send_keys(price)
    select_currency = Select(driver.find_element_by_name("purchase_price_currency_code"))
    if random.choice([0, 1]) == 0:
        select_currency.select_by_value("USD")
    else:
        select_currency.select_by_value("EUR")


def fill_info(driver):
    element = driver.find_element_by_xpath("//a[@href='#tab-information']")
    driver.execute_script("arguments[0].click();", element)
    select_manufacturer = Select(driver.find_element_by_name("manufacturer_id"))
    select_manufacturer.select_by_value("1")
    driver.find_element_by_name("keywords").send_keys(random_letters(25))
    driver.find_element_by_name("short_description[en]").send_keys(random_letters(30))
    # driver.find_element_by_class_name("trumbowyg-editor").send_keys(random_letters(200))
    # just for test AC
    ActionChains(driver).click(driver.find_element_by_class_name("trumbowyg-editor")).send_keys(random_letters(200)) \
        .perform()
    driver.find_element_by_name("head_title[en]").send_keys(random_letters(50))
    driver.find_element_by_name("meta_description[en]").send_keys(random_letters(30))


def fill_general(driver, product_name):
    driver.find_element_by_xpath("//input[@name='status'][1]").click()
    driver.find_element_by_name("name[en]").send_keys(product_name)
    driver.find_element_by_name("code").send_keys(random_letters(5))
    driver.find_element_by_xpath("//input[@data-name='Rubber Ducks']").click()
    select_default_category = Select(driver.find_element_by_name("default_category_id"))
    select_default_category.select_by_visible_text("Rubber Ducks")
    for element in driver.find_elements_by_name("product_groups[]"):
        if random.choice([1, 0]) == 0:
            element.click()
    driver.find_element_by_name("quantity").send_keys(random_number(5))
    select_sold_out_status = Select(driver.find_element_by_name("sold_out_status_id"))
    if random.choice([0, 1]) == 0:
        select_sold_out_status.select_by_value("1")
    else:
        select_sold_out_status.select_by_value("2")
    # Upload image - I don't know how to do it
    # driver.find_element_by_name("new_images[]").click()
    # switch to popup, select image with path, accept
    driver.find_element_by_name("date_valid_from").send_keys("22.02.2001")
    driver.find_element_by_name("date_valid_to").send_keys("22.02.2021")


def random_number(max_len):
    return "".join([random.choice(string.digits) for i in range(random.randrange(max_len))])


def go_to_add_new_product_page(driver):
    driver.find_element_by_link_text("Catalog").click()
    wait(driver).until(ec.title_contains("Catalog | My Store"))
    driver.find_element_by_link_text("Add New Product").click()
    wait(driver).until(ec.title_contains("Add New Product | My Store"))


def login_to_admin_page(driver):
    driver.get("http://localhost:8080/litecart/admin/")
    driver.find_element_by_xpath("//input[@name='username']").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    wait(driver).until(ec.title_is("My Store"))


def random_letters(max_len):
    return "".join([random.choice(string.ascii_letters + " ") for i in range(random.randrange(max_len))])


def wait(driver):
    waiter = WebDriverWait(driver, 10)
    return waiter


__author__ = "Grzegorz Holak"
