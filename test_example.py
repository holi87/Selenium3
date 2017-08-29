import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    driver.get("http://amberteam.pl/")
    driver.find_element_by_link_text("Testowanie").click()
    WebDriverWait(driver, 10).until(EC.title_is("AmberTeam / Testowanie"))

__author__ = "Grzegorz Holak"
