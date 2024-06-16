import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope='session')
def driver() -> WebDriver:
    """
    Fixture to create a chrome webdriver instance
    :return Webdriver
    """
    chrome_options = Options()
    mobile_emulation = {"deviceName": "iPhone SE"}
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--enable-popup-blocking")
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    driver = webdriver.Chrome(chrome_options)

    yield driver
    driver.quit()
