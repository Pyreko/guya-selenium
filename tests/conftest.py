from selenium import webdriver
from pytest import yield_fixture


@yield_fixture(scope="module")
def init_firefox():
    print("Initializing the Firefox WD...")
    driver = webdriver.Firefox()
    yield driver
    driver.quit()


@yield_fixture(scope="module")
def init_chrome():
    print("Initializing the Chrome WD...")
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@yield_fixture(scope="module")
def init_edge():
    print("Initializing the Edge WD...")
    driver = webdriver.Edge()
    yield driver
    driver.quit()
