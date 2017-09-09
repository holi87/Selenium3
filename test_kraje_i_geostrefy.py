import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec



@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd

# task 9 - part 1


def test_countries(driver):
    login_to_admin_page(driver)
    driver.get("http://localhost:8080/litecart/admin/?app=countries&doc=countries")
    wait(driver).until(ec.title_contains("Countries | My Store"))
    lista_krajow = []
    kraje_stref = []
    for row in driver.find_elements_by_class_name("row"):
        lista_krajow.append(row.find_element_by_xpath(".//a").text)
        if row.find_element_by_xpath(".//td[6]").text != str(0):  #  making list of urls where zones > 0 to use later
            kraje_stref.append(row.find_element_by_xpath(".//a").get_attribute("href"))
    assert lista_krajow == sorted(lista_krajow)
    #  here starting b) part - checking pages of countries with more zones than 0
    for i in range(len(kraje_stref)):
        driver.get(kraje_stref[i])
        lista_stref = []
        dlugosc_tablicy = len(driver.find_elements_by_xpath("//table[@id='table-zones']/*/tr"))
        for j in range(2, dlugosc_tablicy):
            lista_stref.append(driver.find_element_by_xpath("//*[@id='table-zones']/tbody/tr[%s]/td[3]" % j).text)
        assert lista_stref == sorted(lista_stref)


# task 9 - part 2


def test_geozones(driver):
    login_to_admin_page(driver)
    driver.get("http://localhost:8080/litecart/admin/?app=geo_zones&doc=geo_zones")
    wait(driver).until(ec.title_contains("Geo Zones | My Store"))
    for i in range(len(driver.find_elements_by_class_name("row"))):
        tmp = driver.find_elements_by_class_name("row")
        tmp[i].find_element_by_xpath(".//a").click()
        #  this if is for EU
        if driver.find_element_by_name("name").get_attribute("value") == "European Union":
            print("\nIn European Union are countries not zones!")
            # this part will check if countries are sorted alphabetically
            lista_panstw = driver.find_elements_by_xpath("//td[2]/select/option[@selected]")
            for j in range(len(lista_panstw)):
                lista_panstw[j] = lista_panstw[j].text
            assert lista_panstw == sorted(lista_panstw)
        else:
            lista_stref = driver.find_elements_by_xpath("//td[3]/select/option[@selected]")
            for j in range(len(lista_stref)):
                lista_stref[j] = lista_stref[j].text
            assert lista_stref == sorted(lista_stref)
        driver.execute_script("history.go(-1);")




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
