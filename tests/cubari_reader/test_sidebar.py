# Deals with testing settings from the sidebar from the reader.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
import pytest
from typing import NewType, Optional, Union, Dict
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from pytest import lazy_fixture  # type: ignore
from enum import Enum
import time

BROWSER_FIXTURES = [lazy_fixture("init_firefox"), lazy_fixture("init_chrome")]
DEMO_CHAPTER = "https://guya.moe/read/manga/Kaguya-Wants-To-Be-Confessed-To/163/1/"

DriverType = NewType("DriverType", Union[webdriver.Firefox, webdriver.Chrome])


@pytest.mark.sidebar
class TestSidebar:
    """
    Common sidebar testing fixtures and functions.
    """

    @pytest.fixture()
    def sidebar(self, browser: DriverType):
        browser.get(DEMO_CHAPTER)
        sidebar = WebDriverWait(browser, 5).until(
            EC.visibility_of_element_located((By.TAG_NAME, "aside"))
        )
        return sidebar


class TestGeneralSidebar(TestSidebar):
    """
    Tests general stuff regarding the sidebar.  Reeeeesponsiveness, 
    buttons that don't fall under other categories, etc.
    """

    def test_hide_sidebar(self):
        pass

    def test_resizing_and_sidebar(self):
        pass


@pytest.mark.sidebar_fit_mode
@pytest.mark.parametrize(
    "browser", [lazy_fixture("init_firefox"), lazy_fixture("init_chrome")],
)
class TestFitMode(TestSidebar):
    """
    For testing how physically fit the modes ar- I mean, if the mode selection
    is behaving and actually changing the image sizes correctly.
    """

    class FitMode(Enum):
        """
        The fitmodes and their attribute names.
        Probably *very* delicate --- tests relying
        on the values will break if they're renamed!
        """

        ALL = "all"
        WIDTH = "width"
        HEIGHT = "height"
        NONE = "none"
        ALL_LIMIT = "all_limit"
        WIDTH_LIMIT = "width_limit"
        HEIGHT_LIMIT = "height_limit"

    def click_to_mode(self, sidebar: WebElement, mode: FitMode, timeout: int = 14):
        """
        Click the button~

        To the beat~
        

        Returns either the final button or None if nothing is found; can be an
        easy way to check if the mode set is correct.
        """
        fit_button: WebElement = sidebar.find_element_by_css_selector(
            "button[data-bind='fit_button']"
        )
        timeout_count = 0
        while timeout_count < timeout:
            fit_button.click()
            fit_button = sidebar.find_element_by_css_selector(
                "button[data-bind='fit_button']"
            )
            observed_mode = self.FitMode(fit_button.get_attribute("data-lyt.fit"))
            if observed_mode and observed_mode == mode:
                return fit_button

            timeout_count += 1
            time.sleep(0.015)

        return None

    def get_current_page_image_size(
        self, driver: DriverType, page_index: int = 0
    ) -> Dict[str, float]:
        """
        Returns the currently displayed image's width and height
        (in that order).
        """

        # TODO: Index out of bounds, no handling of timeouts, oh boy!
        current_image: Optional[WebElement] = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div[data-bind='image_container']")
            )
        ).find_elements_by_tag_name("div")[page_index]

        return current_image.size

    def test_stretch_width(self, browser: DriverType, sidebar: WebElement):
        """
        Tests whether the stretch-width button will properly
        fit the page in terms of width.
        """
        assert self.click_to_mode(
            sidebar, self.FitMode.WIDTH
        ), "Could not find stretch width button."

        image_dim = self.get_current_page_image_size(browser)
        browser_dim = browser.get_window_size()

        # Simple test
        assert image_dim.get("width") <= browser_dim.get("width")

        # Now resize...

        # And resize back...

    def test_stretch_height(self, browser: DriverType, sidebar: WebElement):
        """
        Tests whether the stretch-height button will properly
        fit the page in terms of height.
        """

    def test_stretch_all(self, browser: DriverType, sidebar: WebElement):
        """
        Tests whether the stretch-all button will properly
        expand to the page in terms of width or height.
        """

    def test_limit_width(self, browser: DriverType, sidebar: WebElement):
        """
        Tests whether the limit-width button that does not
        exceed max width.
        """

    def test_limit_height(self, browser: DriverType, sidebar: WebElement):
        """
        Tests whether the limit-height button that does not
        exceed max height.
        """

    def test_limit_all(self, browser: DriverType, sidebar: WebElement):
        """
        Tests whether the limit-all button will properly
        fit the page in terms of width and height.
        """

    def test_one_to_one(self, browser: DriverType, sidebar: WebElement):
        """
        Tests whether the 1:1 button will just show the
        original page without any size changes.
        """


class TestPageControls(TestSidebar):
    """
    For testing general page controls, like chapter and volume controls.
    """

    def test_previous_chapter(self):
        pass

    def test_next_chapter(self):
        pass

    def test_previous_volume(self):
        pass

    def test_next_volume(self):
        pass


class TestPageSpread(TestSidebar):
    """
    For testing 1P, 2P, and 2P offset.
    """
