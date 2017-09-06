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



def test_login_admin_page(driver):

    login_to_admin_page(driver)
    wait(driver).until(ec.title_is("My Store"))
    driver.find_element_by_link_text("Countries").click()
    wait(driver).until(ec.title_contains("Countries"))

def test_all_admin_pages(driver):
    login_to_admin_page(driver)
    wait(driver).until(ec.title_is("My Store"))
    lista = driver.find_elements_by_id("app-")
    for j in range(len(lista)):
        tmp_l = driver.find_elements_by_id("app-")
        tmp_l[j].click()
        lista_temp = driver.find_elements_by_css_selector("li#app-.selected li[id^=doc-]")
        for i in range(len(lista_temp)):
            tmp = driver.find_elements_by_css_selector("li#app-.selected li[id^=doc-]")
            tmp[i].click()
            h1 = driver.find_element_by_xpath("//h1").text
            selected = driver.find_element_by_css_selector("li#app-.selected li[id^=doc-].selected").text
            assert h1 == selected


def test_all_admin_pages_only_h1(driver):
    login_to_admin_page(driver)
    wait(driver).until(ec.title_is("My Store"))
    lista = driver.find_elements_by_id("app-")
    for j in range(len(lista)):
        tmp_l = driver.find_elements_by_id("app-")
        tmp_l[j].click()
        lista_temp = driver.find_elements_by_css_selector("li#app-.selected li[id^=doc-]")
        for i in range(len(lista_temp)):
            tmp = driver.find_elements_by_css_selector("li#app-.selected li[id^=doc-]")
            tmp[i].click()
            ec.presence_of_element_located((By.XPATH, "//h1"))



def login_to_admin_page(driver):
    driver.get("http://localhost:8080/litecart/admin/")
    driver.find_element_by_xpath("//input[@name='username']").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()


def wait(driver):
    wait = WebDriverWait(driver, 10)
    return wait

"""
lista = []
lista = driver.find_elements_by_css_selector("li#app-")
print(lista)

li#app-.selected - css selector dla wybranego elementu glownej listy
li#app-.selected li[id^=doc-].selected - css selector dla wybranego elementu wewnątrz aktualnie otwartej podlisty
li#app-.selected li[id^=doc-].selected span - tu jest ukryty tytul linka, ma sie zgadzac z h1


"""

__author__ = "Grzegorz Holak"
