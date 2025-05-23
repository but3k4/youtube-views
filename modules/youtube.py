# -*- coding: utf-8 -*-
"""
This module provides the YouTube class for interacting with YouTube website
using Selenium. It allows for actions like searching, retrieving video information,
and basic player control.

For more information about Selenium, please visit:
https://selenium-python.readthedocs.io/
"""

import time
import logging # For TODOs
from selenium import webdriver
from selenium.webdriver.common.by import By
# Removed duplicate import of By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import JavascriptException
from selenium.common.exceptions import WebDriverException
from modules import utils


class YouTube:
    """
    A class to interact with the YouTube website using Selenium.

    This class encapsulates browser interactions to perform actions such as
    opening URLs, searching for videos, retrieving video details (title, views, etc.),
    and managing video playback (play, mute, skip ads).

    It uses a predefined dictionary of CSS selectors for locating elements on YouTube pages,
    which can be updated if YouTube's page structure changes.

    The class is designed to be used as a context manager.
    """
    # pylint: disable=R0904

    # SELECTORS dictionary stores CSS selectors, XPaths, or IDs used to locate elements on YouTube.
    # This approach centralizes selectors, making them easier to update if YouTube's frontend changes.
    SELECTORS = {
        'search_query': 'search_query', # NAME
        'video_title_link': 'a.yt-simple-endpoint.style-scope.ytd-video-renderer#video-title', # CSS_SELECTOR
        'video_renderer': '//*[@id="contents"]/ytd-video-renderer', # XPATH
        'video_title_id': 'video-title', # ID
        'channel_name_class': 'ytd-channel-name', # CLASS_NAME
        'formatted_string_class': 'yt-formatted-string', # CLASS_NAME
        'more_button_xpath': "//div[@id='more']/yt-formatted-string/span[3]", # XPATH
        'play_button_class': 'ytp-play-button', # CLASS_NAME
        'mute_button_class': 'ytp-mute-button', # CLASS_NAME
        'skip_ad_button_class': 'ytp-ad-skip-button-text', # CLASS_NAME
        'view_count_class': 'view-count', # CLASS_NAME
        'owner_sub_count_id': 'owner-sub-count', # ID
        'movie_player_id': 'movie_player', # ID, used for JS player state
        'time_duration_class': 'ytp-time-duration', # CLASS_NAME
    }

    def __init__(self, url='https://youtube.com', proxy=None, verbose=False):
        """
        Initializes the YouTube class.

        Sets up Chrome WebDriver options (headless, proxy, user-agent) and
        initializes the WebDriver instance.

        Args:
            url (str): The initial URL to open (defaults to YouTube homepage).
            proxy (str, optional): Proxy server address (e.g., 'ip:port'). Defaults to None.
            verbose (bool): If True, enables more detailed output (currently affects some methods).
                            Note: This parameter's usage might be inconsistent and logging is preferred.
        """
        self.url = url
        self.proxy = proxy
        self.verbose = verbose # TODO: Replace verbose flag with standard logging levels.

        # Configure Chrome options
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--mute-audio')
        self.options.add_argument('--single-process')
        self.options.add_argument('--autoplay-policy=no-user-gesture-required')
        if self.proxy:
            self.options.add_argument(f'--proxy-server={self.proxy}')
        
        self.user_agent = utils.user_agent()
        self.options.add_argument(f'--user-agent={self.user_agent}')
        
        self.browser = webdriver.Chrome(options=self.options)
        self.default_timeout = 20
        self.browser.implicitly_wait(self.default_timeout)
        self.browser.set_window_size(1920, 1080)
        # self.open_url() # Page opening is deferred to __enter__ or an explicit call.

    def __enter__(self):
        """
        Enters the runtime context related to this object.
        Opens the initial URL.
        """
        try:
            self.open_url()
        except WebDriverException as e:
            # TODO: Replace print with logging.error
            print(f"Error opening URL: {e}") 
            # Depending on desired behavior, might want to quit browser here
            # or allow __exit__ to handle it. For now, let __exit__ handle.
            raise
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the runtime context related to this object.
        Ensures the browser connection is closed.
        """
        self.disconnect()

    def find_by_class(self, class_name):
        """
        Finds the first element matching the given class name.

        Args:
            class_name (str): The class name of the element to find.

        Returns:
            WebElement: The first WebElement found.
            
        Raises:
            NoSuchElementException: If no element is found.
        """
        return self.browser.find_element(By.CLASS_NAME, class_name)

    def find_all_by_class(self, class_name):
        """
        Finds all elements matching the given class name.

        Args:
            class_name (str): The class name of the elements to find.

        Returns:
            list[WebElement]: A list of WebElements found, or an empty list.
        """
        return self.browser.find_elements(By.CLASS_NAME, class_name)

    def find_by_id(self, id_name):
        """
        Finds the first element matching the given ID.

        Args:
            id_name (str): The ID of the element to find.

        Returns:
            WebElement: The first WebElement found.

        Raises:
            NoSuchElementException: If no element is found.
        """
        return self.browser.find_element(By.ID, id_name)

    def find_all_by_id(self, id_name):
        """
        Finds all elements matching the given ID.

        Args:
            id_name (str): The ID of the elements to find.

        Returns:
            list[WebElement]: A list of WebElements found, or an empty list.
        """
        return self.browser.find_elements(By.ID, id_name)

    def find_by_name(self, name):
        """
        Finds the first element matching the given name attribute.

        Args:
            name (str): The name attribute of the element to find.

        Returns:
            WebElement: The first WebElement found.

        Raises:
            NoSuchElementException: If no element is found.
        """
        return self.browser.find_element(By.NAME, name)

    def find_all_by_name(self, name):
        """
        Finds all elements matching the given name attribute.

        Args:
            name (str): The name attribute of the elements to find.

        Returns:
            list[WebElement]: A list of WebElements found, or an empty list.
        """
        return self.browser.find_elements(By.NAME, name)

    def find_by_xpath(self, xpath):
        """
        Finds the first element matching the given XPath.

        Args:
            xpath (str): The XPath expression.

        Returns:
            WebElement: The first WebElement found.

        Raises:
            NoSuchElementException: If no element is found.
        """
        return self.browser.find_element(By.XPATH, xpath)

    def find_all_by_xpath(self, xpath):
        """
        Finds all elements matching the given XPath.

        Args:
            xpath (str): The XPath expression.

        Returns:
            list[WebElement]: A list of WebElements found, or an empty list.
        """
        return self.browser.find_elements(By.XPATH, xpath)

    def click(self, how: By, what: str):
        """
        Clicks on an element identified by `how` and `what`.
        Waits for the element to be clickable before attempting to click.

        Args:
            how (By): The Selenium By strategy (e.g., By.ID, By.XPATH).
            what (str): The selector string.

        Returns:
            bool: True if click was successful, False otherwise (e.g., timeout, element not interactable).
        """
        try:
            wait = WebDriverWait(self.browser, self.default_timeout)
            wait.until(EC.element_to_be_clickable((how, what))).click()
            return True
        except (ElementClickInterceptedException, TimeoutException):
            # TODO: Consider logging this exception.
            return False
        

    def open_url(self):
        """
        Opens the URL stored in `self.url`.
        
        Raises:
            WebDriverException: If the URL fails to load or another WebDriver error occurs.
        """
        try:
            self.browser.get(self.url)
        except WebDriverException as e:
            # TODO: Replace print with logging.error
            print(f"WebDriverException opening url: {self.url} - {e}")
            raise

    def get_current_url(self):
        """
        Gets the current URL of the browser.

        Returns:
            str | None: The current URL as a string, or None if a WebDriverException occurs.
        """
        try:
            return self.browser.current_url
        except WebDriverException:
            # TODO: Log this exception
            return None

    def get_title(self):
        """
        Gets the title of the current page (typically the video title).
        Waits for the video title element to be present.

        Returns:
            str | None: The page title as a string, or None if not found or a timeout/error occurs.
        """
        try:
            wait = WebDriverWait(self.browser, self.default_timeout)
            wait.until(EC.presence_of_element_located((By.ID, self.SELECTORS['video_title_id'])))
            return self.browser.title
        except (TimeoutException, NoSuchElementException):
            # Log error or handle as needed
            # TODO: Log this exception
            return None

    def search(self, query: str):
        """
        Searches YouTube for the given query.

        Performs a search, clicks the "more" button (if applicable, though this UI element might change),
        and attempts to extract information for each video found in the results.

        Args:
            query (str): The search term(s).

        Returns:
            dict | None: A dictionary where keys are video IDs and values are dictionaries
                         containing video details ('id', 'video title', 'video url', 
                         'channel name', 'channel url', 'element').
                         Returns None if a significant error occurs during the initial search setup.
                         Returns an empty dict if no results are found.
                         Individual video processing errors are logged (if verbose) and skipped.
        """
        result = {}
        try:
            # Find search input, click, clear, and type query
            search_input = self.find_by_name(self.SELECTORS['search_query'])
            time.sleep(2) # Consider replacing with explicit waits
            search_input.click()
            time.sleep(2) # Consider replacing with explicit waits
            search_input.clear()
            search_input.send_keys(query)
            time.sleep(10) # Consider replacing with explicit waits for search suggestions or results
            search_input.send_keys(Keys.DOWN) # Navigate to first suggestion
            search_input.send_keys(Keys.ENTER) # Execute search

            # Click 'more' button - this might need adjustment if UI changes
            # self.click(By.XPATH, self.SELECTORS['more_button_xpath']) # This action's purpose is unclear from context.

            # Wait for video results to be visible
            wait = WebDriverWait(self.browser, self.default_timeout)
            wait.until(
                EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, self.SELECTORS['video_title_link'])
                )
            )
            
            items = self.find_all_by_xpath(self.SELECTORS['video_renderer'])
            if not items:
                return {} # No results found

            for item in items:
                try:
                    if item.is_displayed():
                        v_info = item.find_element(By.ID, self.SELECTORS['video_title_id'])
                        c_info = item.find_element(By.CLASS_NAME, self.SELECTORS['channel_name_class'])
                        
                        v_link = v_info.get_attribute('href')
                        if not v_link:
                            continue # Skip if no link

                        v_id = v_link.strip('https://www.youtube.com/watch?v=')
                        v_title = v_info.get_attribute('title')
                        
                        c_url_element = c_info.find_element(By.CLASS_NAME, self.SELECTORS['formatted_string_class'])
                        c_url = c_url_element.get_attribute('href') if c_url_element else None
                        if not c_url:
                            continue # Skip if no channel URL

                        result[v_id] = {
                            'id': v_id,
                            'video title': v_title,
                            'video url': v_link,
                            'channel name': c_info.text,
                            'channel url': c_url,
                            # Storing WebElement 'element': v_info can lead to StaleElementReferenceException
                            # if the page changes or element is no longer valid. Best to extract all needed data.
                        }
                except (NoSuchElementException, AttributeError, TimeoutException) as e_item:
                    # TODO: Replace print with logging.warning or logging.debug
                    if self.verbose:
                        print(f"Error processing search item: {e_item}")
                    continue 
            return result
        except (NoSuchElementException, TimeoutException) as e_search: 
            # TODO: Replace print with logging.error
            if self.verbose:
                print(f"Error in search setup: {e_search}")
            return None 

    def play_video(self):
        """
        Clicks on the play button of the video player.
        Assumes a video page is loaded and the play button is available.
        """
        self.click(By.CLASS_NAME, self.SELECTORS['play_button_class'])

    def mute_video(self):
        """
        Clicks on the mute button of the video player.
        Assumes a video page is loaded and the mute button is available.
        """
        self.click(By.CLASS_NAME, self.SELECTORS['mute_button_class'])

    def skip_ad(self, max_attempts=20, time_wait=0.5):
        """
        Attempts to skip a video ad by clicking the skip button.
        Retries a number of times if the button is not immediately available or clickable.

        Args:
            max_attempts (int): Maximum number of attempts to find and click the skip button.
            time_wait (float): Time in seconds to wait between attempts.
        """
        attempts = 0
        while attempts <= max_attempts:
            try:
                button = self.find_by_class(self.SELECTORS['skip_ad_button_class'])
                if button.is_enabled() or button.is_displayed():
                    # TODO: Replace print with logging.debug
                    if self.verbose:
                        print(button.get_attribute('textContent').lower())
                    # Attempt to click, handle cases where it might fail
                    WebDriverWait(self.browser, 1).until(EC.element_to_be_clickable(button)).click()
                    break # Ad skipped
            except (ElementNotInteractableException, ElementClickInterceptedException, TimeoutException):
                time.sleep(time_wait)
            except (NoSuchElementException, AttributeError): 
                # If button not found or other attribute error, assume no skippable ad.
                break
            attempts += 1

    def get_views(self):
        """
        Gets the total views for the current video.

        Returns:
            str | None: The number of views as a string (e.g., "1,234,567"), 
                         or None if the view count element is not found or an error occurs.
        """
        try:
            element = self.find_by_class(self.SELECTORS['view_count_class'])
            return element.get_attribute('textContent').strip(' views')
        except (NoSuchElementException, AttributeError): 
            # TODO: Log this exception
            return None

    def get_channel_name(self):
        """
        Gets the name of the channel for the current video.

        Returns:
            str | None: The channel name, or None if not found or an error occurs.
        """
        try:
            element = self.find_by_class(self.SELECTORS['channel_name_class'])
            return element.text
        except (NoSuchElementException, AttributeError): 
            # TODO: Log this exception
            return None

    def get_subscribers(self):
        """
        Gets the total number of subscribers for the current channel.

        Returns:
            str | None: The subscriber count as a string (e.g., "1.23M"), 
                         or None if not found or an error occurs.
        """
        try:
            element = self.find_by_id(self.SELECTORS['owner_sub_count_id'])
            return element.text.strip(' subscribers')
        except (NoSuchElementException, AttributeError): 
            # TODO: Log this exception
            return None

    def get_player_state(self):
        """
        Returns the state of the YouTube video player using JavaScript.

        Possible states (from YouTube IFrame API documentation):
        -1: unstarted
         0: ended
         1: playing
         2: paused
         3: buffering
         5: video cued

        Returns:
            int | -2: The player state code as an integer. 
                      Returns -2 if a JavascriptException occurs during execution.
        """
        # The comment block above the method already explains the states well.
        try:
            js_element = f"return document.getElementById('{self.SELECTORS['movie_player_id']}').getPlayerState()"
            return self.browser.execute_script(js_element)
        except JavascriptException:
            # TODO: Log this exception
            return -2

    def refresh_page(self):
        """
        Refreshes the current page.
        Handles WebDriverException if the refresh fails.
        """
        try:
            self.browser.refresh()
        except WebDriverException:
            # TODO: Log this exception
            pass # Error handled by caller or ignored

    def time_duration(self):
        """
        Gets the total duration time of the current video.

        Returns:
            str | None: The video duration as a string (e.g., "10:32"),
                         or None if not found or an error occurs.
        """
        try:
            duration = self.find_by_class(self.SELECTORS['time_duration_class'])
            if duration: 
                return duration.get_attribute('textContent')
            return None 
        except (NoSuchElementException, AttributeError): 
            # TODO: Log this exception
            return None

    def disconnect(self):
        """
        Closes the browser connection and quits the WebDriver.
        Sets the browser attribute to None.
        """
        if hasattr(self, 'browser') and self.browser:
            self.browser.quit()
            self.browser = None 

# vim: set et ts=4 sw=4 sts=4 tw=80
