import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_links(driver):
    login_to_admin_page(driver)
    go_to_countries(driver)
    add_new_country(driver)
    main_window = driver.current_window_handle
    for i in range(len(driver.find_elements_by_xpath("//a/i[@class='fa fa-external-link']/.."))):
        old_windows = driver.window_handles
        driver.find_elements_by_xpath("//a/i[@class='fa fa-external-link']/..")[i].click()
        wait(driver).until(ec.new_window_is_opened(old_windows))
        driver.switch_to_window(new_window_uid(driver, old_windows))
        wait_until_page_is_loaded(driver)
        close_window_and_swith_to_main(driver, main_window)


def wait_until_page_is_loaded(driver):
    wait(driver).until(ec.presence_of_element_located((By.XPATH, "//body")))  # just to be sure that page is loaded


def close_window_and_swith_to_main(driver, main_window):
    driver.close()
    driver.switch_to_window(main_window)


def new_window_uid(driver, old_windows):
    return [i for i in driver.window_handles if i not in old_windows][0]  # there should be only one element


def add_new_country(driver):
    driver.find_element_by_css_selector("a.button").click()


def go_to_countries(driver):
    driver.get("http://localhost:8080/litecart/admin/?app=countries&doc=countries")
    wait(driver).until(ec.title_contains("Countries"))


def open_new_window(driver):
    driver.execute_script("window.open()")


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
