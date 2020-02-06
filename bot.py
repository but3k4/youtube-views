#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
""" Bot to increase YouTube views """

import sys
import time
from random import randrange
from youtube import YouTube
import utils


class Bot:
    """ A bot to increase YouTube views """
    # pylint: disable=R0903

    def __init__(self, options):
        """ init variables """

        self.opts = options

    def run(self):
        """ run """

        count = 1
        while count <= self.opts.visits:
            youtube = YouTube(
                url=self.opts.url,
                proxy=self.opts.proxy,
                verbose=self.opts.verbose
            )
            youtube.get_url()
            title = youtube.get_title()
            if self.opts.visits > 1 and title:
                length = (len(title) + 4 - len(str(count)))
                print('[{0}] {1}'.format(count, '-' * length))
            ip_address = utils.get_ipaddr(proxy=self.opts.proxy)
            if ip_address:
                print('external IP address:', ip_address)
            if title:
                print('title:', title)
            youtube.play_video()
            youtube.get_views()
            video_duration = youtube.time_duration()
            if video_duration:
                print('video duration time:', video_duration)
            seconds = utils.to_seconds(duration=video_duration.split(':'))
            if seconds:
                sleep_time = randrange(seconds)
                if self.opts.verbose:
                    print('video duration time in seconds:', seconds)
                print('stopping video in %s seconds' % sleep_time)
                time.sleep(sleep_time)
            youtube.disconnect()
            count += 1


def _main():
    """ main """

    cli_args = utils.get_cli_args()
    bot = Bot(cli_args)
    bot.run()


if __name__ == '__main__':
    sys.exit(_main())

# vim: set et ts=4 sw=4 sts=4 tw=80
