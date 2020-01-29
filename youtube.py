#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
""" YouTube increase views tool """

import time
import sys
import argparse
from random import randrange
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException


class YouTube:
    """ YouTube class """

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

        wait = WebDriverWait(self.browser, self.default_timeout)
        wait.until(EC.visibility_of_element_located((By.ID, 'video-title')))
        print('title:', self.browser.title)

    def set_input_value(self, xpath, value):
        """ set input value """

        elem_send = self.find_by_xpath(xpath)
        elem_send.send_keys(value)

    def click(self, xpath):
        """ click on element """

        elem_click = self.find_by_xpath(xpath)
        if elem_click:
            elem_click.click()

    def find_by_xpath(self, xpath):
        """ find element by xpath """

        return self.browser.find_element_by_xpath(xpath)

    def find_by_class(self, name):
        """ find element by class name """

        return self.browser.find_element_by_class_name(name)

    def is_element_present(self, how, what):
        """ check if element is present """

        try:
            self.browser.find_element(by=how, value=what)
        except NoSuchElementException:
            return False
        return True

    def disconnect(self):
        """ close webdriver connection """

        self.browser.close()
        self.browser.quit()

    def skip_ad(self, sleep=1):
        """ skip ads """

        while True:
            try:
                button = self.find_by_class('ytp-ad-skip-button-text')
                if button:
                    print(button.get_attribute('textContent'))
                    button.click()
            except ElementNotInteractableException:
                time.sleep(sleep)
            except NoSuchElementException:
                break

    def play_video(self):
        """ click on play button """

        class_name = 'ytp-play-button'
        # xpath = "//button[@class='ytp-play-button ytp-button']"
        # xpath = "//button[@class='ytp-large-play-button ytp-button']"
        wait = WebDriverWait(self.browser, self.default_timeout)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, class_name))).click()
        # wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    def mute_video(self):
        """ click on mute button """

        class_name = 'ytp-mute-button'
        # xpath = "//button[@class='ytp-large-mute-button ytp-button']"
        # xpath = "//button[@class='ytp-mute-button ytp-button']"
        wait = WebDriverWait(self.browser, self.default_timeout)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, class_name))).click()
        # wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    def get_views(self):
        """ get total of views """

        try:
            class_name = 'view-count'
            # class_name = 'short-view-count'
            # xpath = '//*[@id="count"]/yt-view-count-renderer/span[1]'
            # xpath = '//*[@id="count"]/yt-view-count-renderer/span[2]'
            # views = self.find_by_xpath(xpath)
            views = self.find_by_class(class_name)
            print('views:', views.get_attribute('textContent').strip(' views'))
        except NoSuchElementException:
            return None
        return True

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

        _seconds = timedelta(hours=int(_hour), minutes=int(_min), seconds=int(_sec))
        return int(_seconds.total_seconds())

    def login(self):
        """ log into url """

        login_name = input('lala\n')
        login_password = input('lele\n')
        self.get_url()
        time.sleep(3)

        login_type = self.browser.find_element_by_id('switcher_plogin')
        login_type.click()

        username = self.browser.find_element_by_id('u')
        username.clear()
        password = self.browser.find_element_by_id('p')
        password.clear()
        username.send_keys(login_name)
        password.send_keys(login_password)

        submit = self.browser.find_element_by_id('login_button')
        submit.click()
        time.sleep(5)


def get_cli_args():
    """ get command line arguments """

    parser = argparse.ArgumentParser(
        description='YouTube increase views tool',
        add_help=False,
    )

    # main arguments
    main = parser.add_argument_group(
        'Main Arguments',
    )
    main.add_argument(
        '--visits',
        help='amount of visits per video',
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
    youtube.get_url()
    youtube.get_title()
    youtube.play_video()
    # youtube.mute_video()
    youtube.skip_ad()
    youtube.get_views()
    video_duration = youtube.time_duration()
    if video_duration:
        print('video duration time:', video_duration)
    seconds = youtube.to_seconds(duration=video_duration.split(':'))
    print('video duration time in seconds:', seconds)

    sleep_time = randrange(seconds)
    print('stopping video in %s seconds' % sleep_time)
    # time.sleep(sleep_time)
    time.sleep(10)
    youtube.disconnect()


if __name__ == '__main__':
    sys.exit(_main())
