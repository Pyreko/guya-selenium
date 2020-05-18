# Deals with testing searching from the reader.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
import pytest
from pytest import lazy_fixture  # type: ignore
from typing import List, Union
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import time


# Randomly selected page.  Shouldn't matter; just make sure that the route is still
# correct in the future.
DEMO_CHAPTER = "https://guya.moe/read/manga/Kaguya-Wants-To-Be-Confessed-To/163/1/"
INVALID_SEARCH_WORD = "floccinaucinihilipilification"
TEXT_SEARCH_WORD = "cubari"
TEXT_SEARCH_BROWSER_TITLE = "The 67th Student Council"
TITLE_SEARCH_WORD = "Kaguya Wants to Eat"

BROWSER_FIXTURES = [lazy_fixture("init_firefox"), lazy_fixture("init_chrome")]


@pytest.mark.cubari_search
class TestSearch:
    @pytest.fixture()
    def search_bar(self, browser: Union[webdriver.Firefox, webdriver.Chrome]):
        browser.get(DEMO_CHAPTER)
        search_button = WebDriverWait(browser, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "search"))
        )
        assert search_button, "Search button could not be detected."
        search_button.click()
        search_bar = WebDriverWait(browser, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "UI Input"))
        )
        assert search_bar, "Search bar could not be detected."

        return search_bar

    def slow_send_keys(self, input_field, query: str):
        """
        A required hack to deal with send_keys being *too* fast
        for the input sometimes (noticed on Chrome).
        """
        time.sleep(0.03)
        for q in query:
            time.sleep(0.025)
            input_field.send_keys(q)


class TestChapterSearch(TestSearch):
    def search_chapter_title(
        self,
        browser: Union[webdriver.Firefox, webdriver.Chrome],
        search_bar: WebElement,
        query: str,
        locator_type: str,
        locator_value: str,
    ) -> List:
        """
        Searches for titles.  Will return a list of Elements for results;
        if there are no results then it will return an empty List.
        """

        self.slow_send_keys(search_bar, query)
        try:
            counter = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//div[contains(@class, 'UI Tab is-active')]//i[number(text()) = number(text())]",
                    )
                )
            )

            if int(counter.text) == 0:
                return []
            else:
                elements = browser.find_elements(locator_type, locator_value)
                return elements if elements else []
        except BaseException:
            # Note we want to return an empty list if it does time out, as that
            # indicates nothing loaded.
            # It's up to the test to handle this and work out if that's a failure/success.
            return []

    @pytest.mark.parametrize("browser", BROWSER_FIXTURES)
    def test_valid(self, browser, search_bar):
        """
        Tests getting results for a valid title search
        """
        results = self.search_chapter_title(
            browser,
            search_bar,
            TITLE_SEARCH_WORD,
            By.XPATH,
            "//i[text()='Kaguya Wants to Eat']",
        )
        assert len(results), "Could not find a result for a valid title search!"

    @pytest.mark.parametrize("browser", BROWSER_FIXTURES)
    def test_invalid(self, browser, search_bar):
        """
        Tests getting results for an invalid title search
        """
        results = self.search_chapter_title(
            browser,
            search_bar,
            INVALID_SEARCH_WORD,
            By.XPATH,
            "//div[contains(@class, 'MangaSearch')]//div[contains(@class, 'ChapterUnit')]",
        )
        assert not len(results), "Found a result for an invalid title search!"

    # TODO: For all click results, might be better to not have to re-search?  idk.
    @pytest.mark.parametrize("browser", BROWSER_FIXTURES)
    def test_click_result_chapter(self, browser, search_bar):
        """
        Tests clicking the chapter result from searching for title
        """
        results = self.search_chapter_title(
            browser,
            search_bar,
            TITLE_SEARCH_WORD,
            By.XPATH,
            "//i[text()='Kaguya Wants to Eat']",
        )
        assert len(results), "Could not find a result for a valid title search!"
        results[0].click()
        assert TITLE_SEARCH_WORD in browser.title


class TestIndexSearch(TestSearch):
    def search_indexer(
        self,
        browser: Union[webdriver.Firefox, webdriver.Chrome],
        search_bar: WebElement,
        query: str,
        locator_type: str,
        locator_value: str,
    ) -> List:
        """
        Searches via indexer.  Will return a list of Elements for results; 
        if there are no results then it will return an empty List.

        Behaviour to `search_chapter_title` is pretty much identical, but
        this also sends a `<RETURN>` key to trigger search-by-text rather than
        by-title.
        """

        self.slow_send_keys(search_bar, query)
        search_bar.send_keys(Keys.RETURN)
        try:
            counter = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//div[contains(@class, 'UI Tab is-active')]//i[number(text()) = number(text())]",
                    )
                )
            )

            if int(counter.text) == 0:
                return []
            else:
                elements = browser.find_elements(locator_type, locator_value)
                return elements if elements else []
        except BaseException:
            # Note we want to return an empty list if it does time out, as that
            # indicates nothing loaded.
            # It's up to the test to handle this and work out if that's a failure/success.
            return []

    @pytest.mark.parametrize("browser", BROWSER_FIXTURES)
    def test_valid(self, browser, search_bar):
        """
        Tests getting results for a valid text search
        """
        results = self.search_indexer(
            browser,
            search_bar,
            TEXT_SEARCH_WORD,
            By.XPATH,
            "//div[contains(@class, 'IndexSearch')]//div[contains(@class, 'ChapterUnit')]",
        )
        assert len(results), "Could not find a result for a valid text search!"

    @pytest.mark.parametrize("browser", BROWSER_FIXTURES)
    def test_invalid(self, browser, search_bar):
        """
        Tests getting results for an invalid text search
        """
        results = self.search_indexer(
            browser,
            search_bar,
            INVALID_SEARCH_WORD,
            By.XPATH,
            "//div[contains(@class, 'IndexSearch')]//div[contains(@class, 'ChapterUnit')]",
        )
        assert not len(results), "Found a result for an invalid text search!"

    @pytest.mark.parametrize("browser", BROWSER_FIXTURES)
    def test_click_result_chapter(self, browser, search_bar):
        """
        Tests clicking the chapter result from searching for text
        """
        results = self.search_indexer(
            browser,
            search_bar,
            TEXT_SEARCH_WORD,
            By.XPATH,
            "//div[contains(@class, 'IndexSearch')]//div[contains(@class, 'ChapterUnit')]",
        )
        assert len(results), "Could not find a result for a valid text search!"
        results[0].click()
        assert TEXT_SEARCH_BROWSER_TITLE in browser.title

    @pytest.mark.parametrize("browser", BROWSER_FIXTURES)
    def test_click_result_page(self, browser, search_bar):
        """
        Tests clicking the page result from searching for text
        """
        results = self.search_indexer(
            browser,
            search_bar,
            TEXT_SEARCH_WORD,
            By.XPATH,
            "//div[contains(@class, 'IndexSearch')]//div[contains(@class, 'ChapterUnit')]",
        )
        assert len(results), "Could not find a result for a valid text search!"

        page_num_element = results[0].find_element_by_xpath(
            ".//div[number(text()) = number(text()) and contains(@class, 'UI')]"
        )
        page_num = int(page_num_element.text)
        page_num_element.click()

        assert TEXT_SEARCH_BROWSER_TITLE in browser.title
        assert format("Page %d" % page_num) in browser.title
