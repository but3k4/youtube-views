#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
"""
This script implements a bot designed to automate viewing YouTube videos,
potentially for increasing view counts. It supports features like using Tor for
IP address rotation and configurable number of visits.
"""

import sys
import time
import logging
from random import randrange
from modules.youtube import YouTube
from modules import utils


class Bot:
    """
    A bot designed to automate the process of visiting a YouTube URL multiple times.

    It can be configured with options such as the target URL, number of visits,
    proxy settings, and whether to use Tor for IP rotation. The bot logs its
    actions and progress.
    """
    # pylint: disable=R0903,R0912 # R0903: Too few public methods, R0912: Too many branches (in run)

    def __init__(self, options: argparse.Namespace):
        """
        Initializes the Bot with command-line options and sets up logging.

        Args:
            options (argparse.Namespace): An object containing parsed command-line
                                          arguments and options. Expected attributes include
                                          `verbose` (for logging level), `visits`, `url`,
                                          `proxy`, and `enable_tor`.
        """
        self.opts = options
        self._setup_logging()

    def _setup_logging(self):
        """
        Configures basic logging for the bot.

        Sets the logging level based on the `verbose` option (DEBUG if True,
        INFO otherwise). The log format includes timestamp, log level, and message.
        """
        log_level = logging.DEBUG if self.opts.verbose else logging.INFO
        logging.basicConfig(level=log_level,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    @staticmethod
    def player_status(value: int) -> str:
        """
        Converts a YouTube player state code to a human-readable string.

        Args:
            value (int): The player state code, typically obtained from the
                         YouTube player API.

        Returns:
            str: A string describing the player state (e.g., 'playing', 'paused'),
                 or 'unknown' if the code is not recognized.
        """
        status_map = { # Renamed for clarity
            -1: 'unstarted',
            0: 'ended',
            1: 'playing',
            2: 'paused',
            3: 'buffering',
            5: 'video cued',
        }
        return status_map.get(value, 'unknown') # Use .get for default value

    def _get_current_ip(self) -> str | None:
        """
        Fetches the current external IP address.
        If Tor is enabled in options, it attempts to get a new IP address via Tor.
        Otherwise, it fetches the IP address directly (possibly via a standard proxy).

        Returns:
            str | None: The current IP address as a string, or None if it could not be determined.
        """
        ipaddr = None
        if self.opts.enable_tor:
            logging.debug("Attempting to get new Tor IP address.")
            ipaddr = utils.get_new_tor_ipaddr(proxy=self.opts.proxy, verbose=self.opts.verbose)
        
        if not ipaddr: # Fallback if Tor is not enabled or failed
            logging.debug("Attempting to get regular IP address (or using non-Tor proxy).")
            ipaddr = utils.get_ipaddr(proxy=self.opts.proxy)
        
        return ipaddr

    def _process_video(self, youtube: YouTube, current_visit_count: int) -> bool:
        """
        Handles the process of interacting with a YouTube video page for a single visit.

        This includes retrieving video title, channel info, views, subscribers,
        skipping ads, determining video duration, and simulating watch time.

        Args:
            youtube (YouTube): An initialized instance of the YouTube class,
                               connected to a video page.
            current_visit_count (int): The current visit number in the loop,
                                       used for logging.

        Returns:
            bool: True if the video was processed successfully (title retrieved and watch time simulated),
                  False if the video title could not be retrieved, indicating a failure for this visit.
        """
        title = youtube.get_title()
        if not title:
            logging.warning('Could not retrieve video title. Skipping this attempt.')
            return False 

        if self.opts.visits > 1: # Log visit count only if multiple visits are planned
            header_len = len(title) + 4 - len(str(current_visit_count))
            logging.info(f'[{current_visit_count}] {"-" * header_len}')
        
        logging.info(f'Title: {title}')
        
        channel_name = youtube.get_channel_name()
        if channel_name:
            logging.info(f'Channel name: {channel_name}')
        
        subscribers = youtube.get_subscribers()
        if subscribers:
            logging.info(f'Subscribers: {subscribers}')
            
        views = youtube.get_views()
        if views:
            logging.info(f'Views: {views}')
            
        # youtube.play_video() # Currently, play_video is not explicitly called.
                             # Assumes video plays automatically or interaction is through skip_ad.
        youtube.skip_ad()
        
        player_state_code = youtube.get_player_state()
        logging.debug(f'Video status: {self.player_status(player_state_code)}')
        
        video_duration_str = youtube.time_duration()
        seconds_to_watch = 30 # Default watch time in seconds
        if video_duration_str:
            logging.info(f'Video duration time: {video_duration_str}')
            try:
                # Attempt to parse the full duration of the video
                parsed_seconds = utils.to_seconds(duration=video_duration_str.split(':'))
                if parsed_seconds > 0:
                    seconds_to_watch = parsed_seconds # Watch the full video
                    logging.debug(f'Video duration in seconds: {seconds_to_watch}')
            except ValueError:
                logging.warning(f"Could not parse video duration: {video_duration_str}. "
                                f"Using default watch time: {seconds_to_watch}s.")
        
        # Ensure seconds_to_watch is positive for randrange; sleep at least 1s.
        sleep_time = randrange(1, seconds_to_watch + 1) if seconds_to_watch > 0 else 1
        logging.info(f'Watching video for {sleep_time} seconds.')
        time.sleep(sleep_time)
        return True

    def run(self):
        """
        Main execution loop for the bot.

        Iterates for the configured number of visits, performing the following for each:
        1. Fetches/renews the IP address (using Tor if enabled).
        2. Opens the YouTube URL using the YouTube class (as a context manager).
        3. Calls `_process_video` to interact with the video.
        4. Handles exceptions and logs progress.
        """
        count = 1
        while count <= self.opts.visits:
            logging.info(f"Starting visit {count} of {self.opts.visits}.")
            ip_address = self._get_current_ip()
            if ip_address:
                logging.info(f"Current IP Address: {ip_address}")
            else:
                logging.warning("Could not determine external IP address for this visit.")
                # Decide if to continue without IP or skip/fail visit
                # For now, let's assume we can proceed but YouTube access might fail

            try:
                # Use YouTube as a context manager
                with YouTube(url=self.opts.url, proxy=self.opts.proxy, verbose=self.opts.verbose) as youtube:
                    if not self._process_video(youtube, count):
                        logging.warning("Failed to process video for visit {count}.")
                        if self.opts.enable_tor: 
                            logging.debug("Tor is enabled. A new IP will be attempted for the next visit.")
                            # The delay for Tor IP renewal is handled by get_new_tor_ipaddr's time_wait
                            # Adding a small extra random delay here before the next visit loop.
                            time.sleep(randrange(1, 4)) 
                        # Continue to the next visit count
                        count += 1
                        continue 
            
            except Exception as e:
                logging.error(f"An unexpected error occurred during visit {count}: {e}", exc_info=True)
                if self.opts.enable_tor:
                    logging.info("Attempting to get a new IP via Tor due to error for the next visit.")
                    # Delay to allow Tor to potentially recover or get a new circuit
                    time.sleep(randrange(5, 10)) 
                # Decide if to break or continue. For now, let's continue to the next visit.

            count += 1
        logging.info("All visits completed.")


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
