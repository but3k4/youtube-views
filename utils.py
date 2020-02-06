# -*- coding: utf-8 -*-
"""
This module provides utility functions that are used within youtube.py that
are also useful for external consumption
"""

import sys
import json
import argparse
from random import choice
from datetime import timedelta
import requests


def user_agent():
    """ returns a random user agent """

    # All user agents
    # https://www.whatismybrowser.com/guides/the-latest-user-agent/

    user_agents = {
        'edge_on_windows': [
            'Mozilla/5.0',
            '(Windows NT 10.0; Win64; x64)',
            'AppleWebKit/537.36',
            '(KHTML, like Gecko)',
            'Chrome/80.0.3987.87',
            'Safari/537.36 Edg/79.0.309.71',
        ],
        'safari_on_mac': [
            'Mozilla/5.0',
            '(Macintosh; Intel Mac OS X 10_13_6)',
            'AppleWebKit/605.1.15',
            '(KHTML, like Gecko)',
            'Version/13.0 Safari/605.1.15',
        ],
        'chrome_on_windows': [
            'Mozilla/5.0',
            '(Windows NT 10.0; Win64; x64)',
            'AppleWebKit/537.36',
            '(KHTML, like Gecko)',
            'Chrome/80.0.3987.87',
            'Safari/537.36',
        ],
        'chrome_on_mac': [
            'Mozilla/5.0',
            '(Macintosh; Intel Mac OS X 10_15_2)',
            'AppleWebKit/537.36',
            '(KHTML, like Gecko)',
            'Chrome/80.0.3987.87',
            'Safari/537.36',
        ],
        'chrome_on_linux': [
            'Mozilla/5.0',
            '(X11; Linux x86_64)',
            'AppleWebKit/537.36',
            '(KHTML, like Gecko)',
            'Chrome/80.0.3987.87',
            'Safari/537.36',
        ],
        'firefox_on_windows': [
            'Mozilla/5.0',
            '(Windows NT 10.0; WOW64; rv:50.0)',
            'Gecko/20100101 Firefox/72.0',
        ],
        'firefox_on_mac': [
            'Mozilla/5.0',
            '(Macintosh; Intel Mac OS X 10.15; rv:72.0)',
            'Gecko/20100101 Firefox/72.0',
        ],
        'firefox_on_linux': [
            'Mozilla/5.0',
            '(X11; Linux x86_64; rv:72.0)',
            'Gecko/20100101 Firefox/72.0',
        ],
        'opera_on_windows': [
            'Mozilla/5.0',
            '(Windows NT 10.0; Win64; x64)',
            'AppleWebKit/537.36',
            '(KHTML, like Gecko)',
            'Chrome/80.0.3987.87',
            'Safari/537.36',
            'OPR/66.0.3515.44',
        ],
        'opera_on_mac': [
            'Mozilla/5.0',
            '(Macintosh; Intel Mac OS X 10_14_5)',
            'AppleWebKit/537.36',
            '(KHTML, like Gecko)',
            'Chrome/80.0.3987.87',
            'Safari/537.36',
            'OPR/66.0.3515.44',
        ],
        'opera_on_linux': [
            'Mozilla/5.0',
            '(X11; Linux x86_64)',
            'AppleWebKit/537.36',
            '(KHTML, like Gecko)',
            'Chrome/80.0.3987.87',
            'Safari/537.36',
            'OPR/66.0.3515.44',
        ],
    }
    values = [value for key, value in user_agents.items()]
    return ' '.join(choice(values))


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


def get_ipaddr(url='http://httpbin.org/ip', proxy=None):
    """ get current external IP """

    if proxy:
        proxy = 'http://{0}'.format(proxy)
        proxies = {'http': proxy, 'https': proxy}
        response = requests.get(url, proxies=proxies)
    else:
        response = requests.get(url)

    if response.status_code == 200:
        try:
            return json.loads(response.content)['origin']
        except json.decoder.JSONDecodeError:
            return None
    return None


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
    main.add_argument(
        '--proxy',
        help='Uses a specified proxy server, e.g: 127.0.0.1:8118',
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


# vim: set et ts=4 sw=4 sts=4 tw=80
