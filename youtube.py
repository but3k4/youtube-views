#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
"""
Tool to increase YouTube views

for more information about selenium, please visit:
https://selenium-python.readthedocs.io/
"""

import time
import sys
import argparse
from random import randrange
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException


class YouTube:
    """ YouTube class """
    # pylint: disable=R0904

    def __init__(self, args):
        """ init variables """

        self.args = args
        # All chrome options
        # https://peter.sh/experiments/chromium-command-line-switches/
        self.options = webdriver.ChromeOptions()
        # Run in headless mode, without a UI or display server dependencies
        self.options.add_argument('--headless')
        # Disables GPU hardware acceleration. If software renderer is not in
        # place, then the GPU process won't launch
        self.options.add_argument('--disable-gpu')
        # Disable audio
        self.options.add_argument('--mute-audio')
        # Sets the initial window size
        # self.options.add_argument('--window-size=1280x1696')
        # Runs the renderer and plugins in the same process as the browser
        self.options.add_argument('--single-process')
        # A string used to override the default user agent with a custom one
        self.user_agent = self.set_user_agent('mac_safari')
        self.options.add_argument('--user-agent={0}'.format(self.user_agent))
        self.browser = webdriver.Chrome(options=self.options)
        self.default_timeout = 20
        self.browser.implicitly_wait(self.default_timeout)

    @staticmethod
    def set_user_agent(name='mac_safari'):
        """ get user agent """

        user_agents = {
            'iphone11_chrome': [
                'Mozilla/5.0',
                '(iPhone; CPU iPhone OS 13_3 like Mac OS X)',
                'AppleWebKit/605.1.15 (KHTML, like Gecko)',
                'CriOS/79.0.3945.73',
                'Mobile/15E148 Safari/604.1',
            ],
            'iphone11_safari': [
                'Mozilla/5.0'
                '(iPhone; CPU iPhone OS 13_3 like Mac OS X)'
                'AppleWebKit/605.1.15',
                '(KHTML, like Gecko)',
                'Version/13.0.4 Mobile/15E148 Safari/604.1',
            ],
            'iphone10_chrome': [
                'Mozilla/5.0',
                '(iPhone; CPU iPhone OS 12_1 like Mac OS X)',
                'AppleWebKit/605.1.15',
                '(KHTML, like Gecko)',
                'Version/12.0 Mobile/15E148 Safari/604.1',
            ],
            'oneplus5_chrome': [
                'Mozilla/5.0'
                '(Linux; Android 9; ONEPLUS A5000)',
                'AppleWebKit/537.36',
                '(KHTML, like Gecko)',
                'Chrome/79.0.3945.136',
                'Mobile Safari/537.36',
            ],
            'oneplus5_firefox': [
                'Mozilla/5.0',
                '(Android 9; Mobile; rv:68.4.2)',
                'Gecko/68.4.2',
                'Firefox/68.4.2',
            ],
            'mac_safari': [
                'Mozilla/5.0',
                '(Macintosh; Intel Mac OS X 10_15_2)',
                'AppleWebKit/605.1.15',
                '(KHTML, like Gecko) Version/13.0.4',
                'Safari/605.1.15',
            ],
            'mac_chrome': [
                'Mozilla/5.0',
                '(Macintosh; Intel Mac OS X 10_15_2)',
                'AppleWebKit/537.36',
                '(KHTML, like Gecko)',
                'Chrome/79.0.3945.130 Safari/537.36',
            ],
            'mac_firefox': [
                'Mozilla/5.0',
                '(Macintosh; Intel Mac OS X 10.15; rv:72.0)',
                'Gecko/20100101 Firefox/72.0',
            ],
            'linux_chrome': [
                'Mozilla/5.0',
                '(X11; Linux x86_64)',
                'AppleWebKit/537.36',
                '(KHTML, like Gecko)',
                'Chrome/79.0.3945.130',
                'Safari/537.36',
            ],
            'linux_firefox': [
                'Mozilla/5.0',
                '(X11; Linux x86_64; rv:72.0)',
                'Gecko/20100101 Firefox/72.0',
            ],
        }
        return ' '.join(user_agents.get(name, 'mac_safari'))

    def find_by_class(self, name):
        """ find element by class name """

        # Use this when you want to locate an element by class attribute name.
        # With this strategy, the first element with the matching class
        # attribute name will be returned. If no element has a matching class
        # attribute name, a NoSuchElementException will be raised.

        return self.browser.find_element_by_class_name(name)

    def find_all_by_class(self, name):
        """ find all elements by class name """

        return self.browser.find_elements_by_class_name(name)

    def find_by_id(self, name):
        """ find element by id """

        # Use this when you know id attribute of an element. With this
        # strategy, the first element with the id attribute value matching the
        # location will be returned. If no element has a matching id attribute,
        # a NoSuchElementException will be raised.

        return self.browser.find_element_by_id(name)

    def find_all_by_id(self, name):
        """ find all elements by id """

        return self.browser.find_elements_by_id(name)

    def find_by_name(self, name):
        """ find element by name """

        # Use this when you know name attribute of an element. With this
        # strategy, the first element with the name attribute value matching
        # the location will be returned. If no element has a matching name
        # attribute, a NoSuchElementException will be raised.

        return self.browser.find_element_by_name(name)

    def find_all_by_name(self, name):
        """ find all elements by name """

        return self.browser.find_elements_by_name(name)

    def find_by_xpath(self, xpath):
        """ find element by xpath """

        # XPath extends beyond (as well as supporting) the simple methods of
        # locating by id or name attributes, and opens up all sorts of new
        # possibilities such as locating the third checkbox on the page.

        # One of the main reasons for using XPath is when you don’t have a
        # suitable id or name attribute for the element you wish to locate.
        # You can use XPath to either locate the element in absolute terms
        # (not advised), or relative to an element that does have an id or
        # name attribute. XPath locators can also be used to specify elements
        # via attributes other than id and name.

        # Absolute XPaths contain the location of all elements from the root
        # (html) and as a result are likely to fail with only the slightest
        # adjustment to the application. By finding a nearby element with an
        # id or name attribute (ideally a parent element) you can locate your
        # target element based on the relationship. This is much less likely
        # to change and can make your tests more robust.

        return self.browser.find_element_by_xpath(xpath)

    def find_all_by_xpath(self, xpath):
        """ find all elements by xpath """

        return self.browser.find_elements_by_xpath(xpath)

    def is_element_present(self, how, what):
        """ check if element is present """

        try:
            self.browser.find_element(by=how, value=what)
        except NoSuchElementException:
            return False
        return True

    def click(self, how, what):
        """ click on element """

        try:
            wait = WebDriverWait(self.browser, self.default_timeout)
            wait.until(EC.element_to_be_clickable((how, what))).click()
        except TimeoutException:
            return False
        return True

    def get_url(self):
        """ get url """

        self.browser.get(self.args.url)

    def get_title(self):
        """ get video title """

        # waits up to 10 seconds before throwing a TimeoutException unless it
        # finds the element to return within 10 seconds. WebDriverWait by
        # default calls the ExpectedCondition every 500 milliseconds until it
        # returns successfully. A successful return is for ExpectedCondition
        # type is Boolean return true or not null return value for all other
        # ExpectedCondition types.

        try:
            wait = WebDriverWait(self.browser, self.default_timeout)
            wait.until(EC.visibility_of_element_located((By.ID, 'video-title')))
            return self.browser.title
        except TimeoutException:
            return False

    def search(self, value):
        """ search for the given input and print the result """

        try:
            # search = self.find_by_xpath('//input[@id="search"]')
            search = self.find_by_name('search_query')
            search.click()
            search.clear()
            search.send_keys(value)
            search.send_keys(Keys.DOWN)
            search.send_keys(Keys.ENTER)
            # self.click(By.ID, 'search-icon-legacy')
            self.click(
                By.XPATH,
                "//div[@id='more']/yt-formatted-string/span[3]")
            wait = WebDriverWait(self.browser, self.default_timeout)
            wait.until(
                EC.presence_of_all_elements_located(
                    (By.ID, 'video-title')))
            items = self.find_all_by_id('video-title')
            index = 0
            for item in items:
                if item.is_displayed():
                    index += 1
                    print(index, item.text)
                    print(index, item.get_attribute('href'))
                    # print(item.get_attribute('innerHTML'))
                    # print(item.get_attribute('outerHTML'))
                    # print(item.get_attribute('innerText'))
                    # print(item.get_attribute('outerText'))
                    # print(item.get_attribute('textContent'))
                    print('-' * 60)
            return True
        except (ElementNotInteractableException, NoSuchElementException):
            return None

    def play_video(self):
        """ click on play button """

        self.click(By.CLASS_NAME, 'ytp-play-button')

    def mute_video(self):
        """ click on mute button """

        self.click(By.CLASS_NAME, 'ytp-mute-button')

    def skip_ad(self, sleep=1):
        """ skip ads """

        while True:
            try:
                button = self.find_by_class('ytp-ad-skip-button-text')
                if self.args.verbose:
                    print(button.get_attribute('textContent'))
                button.click()
            except (ElementNotInteractableException, ElementClickInterceptedException):
                time.sleep(sleep)
            except NoSuchElementException:
                break

    def get_views(self):
        """ get total of views """

        try:
            class_name = 'view-count'
            views = self.find_by_class(class_name)
            if self.args.verbose:
                print('views:', views.get_attribute(
                    'textContent').strip(' views'))
        except NoSuchElementException:
            return False
        return True

    def refresh_page(self):
        """ refresh the page """

        self.browser.refresh()
        # self.browser.execute_script('location.reload()')

    def disconnect(self):
        """ close webdriver connection """

        self.browser.close()
        self.browser.quit()

    def time_duration(self):
        """ get video duration time """

        duration = self.find_by_class('ytp-time-duration')
        if duration:
            return duration.get_attribute('textContent')
        return None

    @staticmethod
    def to_seconds(duration='0:02'):
        """ convert video duration time to seconds """

        if isinstance(duration, str):
            duration = duration.split(':')
        _hour, _min, _sec = (0, 0, 0)
        if len(duration) == 3:
            _hour, _min, _sec = duration
        elif len(duration) == 2:
            _min, _sec = duration

        _seconds = timedelta(
            hours=int(_hour),
            minutes=int(_min),
            seconds=int(_sec))
        return int(_seconds.total_seconds())

    def run(self):
        """ perform all actions """

        count = 1
        self.get_url()
        while (count <= self.args.visits):
            title = self.get_title()
            if self.args.visits > 1:
                print('[{0}] {1}'.format(count, '-' * (len(title) + 4 - len(str(count)))))
            print('title:', title)
            self.play_video()
            self.skip_ad()
            self.get_views()
            video_duration = self.time_duration()
            if video_duration:
                print('video duration time:', video_duration)
            seconds = self.to_seconds(duration=video_duration.split(':'))
            if seconds:
                sleep_time = randrange(seconds)
                if self.args.verbose:
                    print('video duration time in seconds:', seconds)
                print('stopping video in %s seconds' % sleep_time)
                time.sleep(sleep_time)
                self.refresh_page()
                count += 1
        self.disconnect()


def get_cli_args():
    """ get command line arguments """

    parser = argparse.ArgumentParser(
        description='Tool to increase YouTube views',
        add_help=False,
    )

    # main arguments
    main = parser.add_argument_group(
        'Main Arguments',
    )
    main.add_argument(
        '--visits',
        type=int,
        default=1,
        help='amount of visits per video, default: 1',
    )
    main.add_argument(
        '--url',
        help='YouTube video url',
    )
    # optional arguments
    optional = parser.add_argument_group('Optional Arguments')
    optional.add_argument(
        '-v', '--verbose',
        action='store_true',
        default=False,
        help='show more output',
    )
    optional.add_argument(
        '-h', '--help',
        action='store_true',
        default=False,
        help='show this help message and exit',
    )

    args = parser.parse_args()
    if len(sys.argv) == 1 or args.help:
        parser.print_help()
        sys.exit(0)

    return args


def _main():
    """ main function """

    cli_args = get_cli_args()
    youtube = YouTube(cli_args)
    youtube.run()


if __name__ == '__main__':
    sys.exit(_main())
