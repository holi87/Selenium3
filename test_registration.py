import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from model.user import User
import random
import string
from selenium.webdriver.common.keys import Keys


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_register_new_user(driver):
    open_main_page(driver)
    open_registration_page(driver)
    user = generate_user()
    fill_registration_form(driver, user)
    logout(driver)
    login(driver, user)
    logout(driver)


def login(driver, user):
    driver.find_element_by_xpath("//input[@type='text']").clear()
    driver.find_element_by_xpath("//input[@type='text']").send_keys(user.email + Keys.TAB + user.password)
    driver.find_element_by_xpath("//button[@name='login']").click()


def logout(driver):
    driver.find_element_by_link_text("Logout").click()
    wait(driver).until(ec.title_is("Online Store | My Store"))


def fill_registration_form(driver, user):
    driver.find_element_by_css_selector("#create-account input[name='firstname']").send_keys(user.first_name
                                                                                             + Keys.TAB
                                                                                             + user.last_name
                                                                                             + Keys.TAB + user.address)
    # driver.find_element_by_css_selector("#create-account input[name='lastname']").send_keys(user.last_name)
    # driver.find_element_by_css_selector("#create-account input[name='address1']").send_keys(user.address)
    driver.find_element_by_css_selector("#create-account input[name='postcode']").send_keys(user.postal_code
                                                                                            + Keys.TAB + user.city)
    # driver.find_element_by_css_selector("#create-account input[name='city']").send_keys(user.city)
    # skipped selecting country because it has huge impact on post code and phone number mask
    driver.find_element_by_css_selector("#create-account input[name='email']").send_keys(user.email + Keys.TAB
                                                                                         + user.phone)
    # driver.find_element_by_css_selector("#create-account input[name='phone']").send_keys(user.phone)
    # uncheck or not for newsletter
    if int(random_number(2)) % 2 == 0:
        driver.find_element_by_css_selector("#create-account input[name='newsletter']").click()
    driver.find_element_by_css_selector("#create-account input[name='password']").send_keys(user.password
                                                                                            + Keys.TAB + user.password)
    # driver.find_element_by_css_selector("#create-account input[name='confirmed_password']").send_keys(user.password)
    driver.find_element_by_css_selector("#create-account button[name='create_account']").click()


def generate_user():
    user = User(first_name=random_letters(10), last_name=random_letters(15), address=random_address(10),
                postal_code=random_postal_code(), city=random_letters(15), email=random_email(15, 7),
                phone=random_number(9), password=random_password(4, 10))
    return user


def open_registration_page(driver):
    driver.find_element_by_link_text("New customers click here").click()
    wait(driver).until(ec.title_is("Create Account | My Store"))


def random_password(min_len, max_len):
    symbols = string.ascii_letters + string.digits + string.punctuation
    return "".join([random.choice(symbols) for i in range(min_len -1, max_len)])


def random_email(max_len_name, max_len_domain):
    symbols = string.ascii_letters + string.digits
    name = "".join([random.choice(symbols) for i in range(random.randrange(max_len_name))])
    domain = "".join([random.choice(symbols) for i in range(random.randrange(max_len_domain))])
    end = "".join([random.choice(string.ascii_lowercase) for i in range(1, 4)])
    return name + "@" + domain + "." + end


def random_letters(max_len):
    return "".join([random.choice(string.ascii_letters + " ") for i in range(random.randrange(max_len))])


def random_number(length):
    return "".join([random.choice(string.digits) for i in range(length)])


def random_address(max_len):
    street = "".join([random.choice(string.ascii_letters + " ") for i in range(random.randrange(max_len))])
    number = "".join([random.choice(string.digits) for i in range(1, 3)])
    return street + " " + number


def random_postal_code():
    prefix = "".join([random.choice(string.digits) for i in range(1, 3)])
    suffix = "".join([random.choice(string.digits) for i in range(1, 4)])
    return prefix + "-" + suffix



def open_main_page(driver):
    driver.get("http://localhost:8080/litecart")
    wait(driver).until(ec.title_is("Online Store | My Store"))


def wait(driver):
    waiter = WebDriverWait(driver, 10)
    return waiter


__author__ = "Grzegorz Holak"
