from _pytest.fixtures import SubRequest
from selenium import webdriver
from pytest import yield_fixture


@yield_fixture(scope="module")
def init_firefox(
    request, width: float = 1920, height: float = 1080, headless: bool = False,
):
    print("Initializing the Firefox WD...")
    options = webdriver.FirefoxOptions()
    options.add_argument("--width=%d" % width)
    options.add_argument("--height=%d" % height)
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    yield driver
    driver.quit()


@yield_fixture(scope="module")
def init_chrome(
    request, width: float = 1920, height: float = 1080, headless: bool = False,
):
    print("Initializing the Chrome WD...")
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=%d,%d" % (width, height))
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@yield_fixture(scope="module")
def init_edge():
    print("Initializing the Edge WD...")
    driver = webdriver.Edge()
    yield driver
    driver.quit()
