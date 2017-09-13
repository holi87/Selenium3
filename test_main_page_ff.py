import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


@pytest.fixture
def driver(request):
    wd = webdriver.Firefox()
    request.addfinalizer(wd.quit)
    return wd


def test_item_in_campaigns(driver):
    open_main_page(driver)
    product_list = driver.find_elements_by_css_selector("div#box-campaigns li")

    # product_list[0] - because we have to check first element

    product_name = product_list[0].find_element_by_xpath(".//div[@class='name']")
    product_r_pr = product_list[0].find_element_by_xpath(".//*[@class='regular-price']")
    product_c_pr = product_list[0].find_element_by_xpath(".//*[@class='campaign-price']")

    main_page_checklist = [product_name.text, product_r_pr.text, product_c_pr.text]

    # this part is prepared for Firefox, which is not working with rgba, but on Chrome is exception in chromedriver
    # that makes impossible to click product and go to product page. Could make workaround by go to url, but want to
    # leave it as human would do.
    assert product_r_pr.value_of_css_property("color") == "rgb(119, 119, 119)", "regular price color is not gray #777"
    assert product_c_pr.value_of_css_property("color") == "rgb(204, 0, 0)", "campaign price color is not red #c00"
    assert product_r_pr.value_of_css_property("text-decoration") == "line-through", " regular price is not striked!"
    # as webdriver gives it as int not as string value like "bold", checked in css what is "normal" then everything
    # with higher value is marked as bold
    assert int(product_c_pr.value_of_css_property("font-weight")) > 400, "campaign price is not bolded!"

    product_list[0].click()

    # product page now

    pp_product_name = driver.find_element_by_css_selector("h1")
    pp_reg_pr = driver.find_element_by_css_selector("div.content .regular-price")
    pp_camp_pr = driver.find_element_by_css_selector("div.content .campaign-price")
    product_page_checklist = [pp_product_name.text, pp_reg_pr.text, pp_camp_pr.text]
    for i in range(len(main_page_checklist)):
        assert main_page_checklist[i] == product_page_checklist[i], "It's not same product!"

    # rgb(102,102,102) is still gray, but different than on main page, but it's really untestable to make what is grey
    # and what is not exactly, cause it's impossible to make it in range of gray scale.

    assert pp_reg_pr.value_of_css_property("color") == "rgb(102, 102, 102)", "regular price color is not gray #777"
    assert pp_camp_pr.value_of_css_property("color") == "rgb(204, 0, 0)", "campaign price color is not red #c00"
    assert pp_reg_pr.value_of_css_property("text-decoration") == "line-through", "regular price is not striked!"
    # as webdriver gives it as int not as string value like "bold", checked in css what is "normal" then everything
    # with higher value is marked as bold
    assert int(pp_camp_pr.value_of_css_property("font-weight")) > 400, "campaign price is not bolded!"


def open_main_page(driver):
    driver.get("http://localhost:8080/litecart")
    wait(driver).until(ec.title_is("Online Store | My Store"))


def wait(driver):
    waiter = WebDriverWait(driver, 10)
    return waiter

__author__ = "Grzegorz Holak"
