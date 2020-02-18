#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
""" Bot to increase YouTube views """

import sys
import time
from random import randrange
from modules.youtube import YouTube
from modules import utils


class Bot:
    """ A bot to increase YouTube views """
    # pylint: disable=R0903,R0912

    def __init__(self, options):
        """ init variables """

        self.opts = options

    @staticmethod
    def player_status(value):
        """ returns the status based one the input code """

        status = {
            -1: 'unstarted',
            0: 'ended',
            1: 'playing',
            2: 'paused',
            3: 'buffering',
            5: 'video cued',
        }
        return status[value] if value in status else 'unknown'

    def run(self):
        """ run """

        count = 1
        ipaddr = None
        while count <= self.opts.visits:
            if self.opts.enable_tor:
                ipaddr = utils.get_new_tor_ipaddr(proxy=self.opts.proxy)
            if not ipaddr:
                ipaddr = utils.get_ipaddr(proxy=self.opts.proxy)
            youtube = YouTube(
                url=self.opts.url,
                proxy=self.opts.proxy,
                verbose=self.opts.verbose
            )
            title = youtube.get_title()
            if not title:
                if self.opts.verbose:
                    print('there was a problem loading this page. Retrying...')
                    youtube.disconnect()
                    continue
            if self.opts.visits:
                length = (len(title) + 4 - len(str(count)))
                print('[{0}] {1}'.format(count, '-' * length))
            if ipaddr:
                print('external IP address:', ipaddr)
            channel_name = youtube.get_channel_name()
            if channel_name:
                print('channel name:', channel_name)
            subscribers = youtube.get_subscribers()
            if subscribers:
                print('subscribers:', subscribers)
            print('title:', title)
            views = youtube.get_views()
            if views:
                print('views:', views)
            # youtube.play_video()
            youtube.skip_ad()
            if self.opts.verbose:
                status = youtube.get_player_state()
                print('video status:', self.player_status(status))
            video_duration = youtube.time_duration()
            seconds = 30
            if video_duration:
                print('video duration time:', video_duration)
                seconds = utils.to_seconds(duration=video_duration.split(':'))
                if seconds:
                    if self.opts.verbose:
                        print('video duration time in seconds:', seconds)
            sleep_time = randrange(seconds)
            print('stopping video in %s seconds' % sleep_time)
            time.sleep(sleep_time)
            youtube.disconnect()
            count += 1


def _main():
    """ main """

    try:
        cli_args = utils.get_cli_args()
        bot = Bot(cli_args)
        bot.run()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    sys.exit(_main())

# vim: set et ts=4 sw=4 sts=4 tw=80
