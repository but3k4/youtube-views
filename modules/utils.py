# -*- coding: utf-8 -*-
"""
This module provides a collection of utility functions supporting network operations,
Tor interaction, time conversion, command-line argument parsing, and user-agent generation.
These utilities are used by the YouTube bot and can also be consumed by other modules.
"""

import sys
import json
import argparse
import logging
from random import choice
from datetime import timedelta
import socket
import time
import requests
from requests.exceptions import RequestException


def user_agent() -> str:
    """
    Selects and returns a random desktop user-agent string.

    The user-agent strings are chosen from a predefined dictionary representing
    various browser and operating system combinations. This helps in mimicking
    different client environments when making web requests.

    Returns:
        str: A randomly selected user-agent string.
    """
    # Source for user agents: https://www.whatismybrowser.com/guides/the-latest-user-agent/
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
    }
    values = [value for key, value in user_agents.items()]
    return ' '.join(choice(values))


def to_seconds(duration: str = '0:02') -> int:
    """
    Converts a time string in H:M:S, M:S, or S format to total seconds.

    Args:
        duration (str | list[str]): The duration string (e.g., "1:23:45", "23:45", "45")
                                     or a list of strings/integers representing [H, M, S], [M, S], or [S].
                                     Defaults to '0:02'.

    Returns:
        int: The total duration in seconds.

    Raises:
        ValueError: If the input duration components cannot be converted to integers.
    """
    if isinstance(duration, str):
        parts = duration.split(':')
    elif isinstance(duration, (list, tuple)):
        parts = duration
    else:
        raise TypeError("Duration must be a string, list, or tuple.")

    _hour, _min, _sec = (0, 0, 0)
    num_parts = len(parts)

    if num_parts == 3: # H:M:S
        _hour, _min, _sec = map(int, parts)
    elif num_parts == 2: # M:S
        _min, _sec = map(int, parts)
    elif num_parts == 1: # S
        _sec = int(parts[0])
    else:
        raise ValueError("Duration format is invalid. Expected H:M:S, M:S, or S.")

    time_delta = timedelta(hours=_hour, minutes=_min, seconds=_sec)
    return int(time_delta.total_seconds())


def get_ipaddr(url: str = 'http://httpbin.org/ip', proxy: str = None) -> str | None:
    """
    Fetches the external IP address from a given URL, optionally using a proxy.

    It makes a GET request to the specified URL (which should return a JSON
    object with an 'origin' key, like httpbin.org/ip).

    Args:
        url (str): The URL to fetch the IP address from.
                   Defaults to 'http://httpbin.org/ip'.
        proxy (str, optional): Proxy server address in 'ip:port' format.
                               Defaults to None.

    Returns:
        str | None: The external IP address as a string if successful, 
                    otherwise None. Logs warnings on errors.
    """
    proxies = None
    if proxy:
        proxy_url = f'http://{proxy}' 
        proxies = {'http': proxy_url, 'https': proxy_url}

    response = None 
    try:
        response = requests.get(url, proxies=proxies, timeout=10) 
        response.raise_for_status() 
        return response.json().get('origin') 
    except requests.exceptions.HTTPError as http_err:
        logging.warning(f"HTTP error occurred: {http_err} - Status: {response.status_code if response else 'Unknown'}")
        return None
    except requests.exceptions.RequestException as req_err: 
        logging.warning(f"Request failed: {req_err}")
        return None
    except json.JSONDecodeError as json_err: 
        logging.warning(f"Failed to decode JSON response: {json_err}")
        return None
    except AttributeError: 
        logging.warning("Response was not in the expected format.")
        return None


def get_host_by_ipaddr(ipaddr: str) -> str:
    """
    Performs a reverse DNS lookup for the given IP address.

    Args:
        ipaddr (str): The IP address for which to find the hostname.

    Returns:
        str: The hostname if found, or a string indicating the error or
             that no reverse DNS entry was found.
    """
    try:
        socket.inet_aton(ipaddr) # Validate IP address format
        return socket.gethostbyaddr(ipaddr)[0]
    except socket.herror as e: 
        logging.warning(f"Reverse DNS lookup failed for {ipaddr} (herror): {e}")
        return 'no reverse DNS found'
    except socket.gaierror as e: 
        logging.warning(f"Reverse DNS lookup failed for {ipaddr} (gaierror): {e}")
        return 'address-related error in reverse DNS lookup'
    except TypeError as e: 
        logging.warning(f"Illegal IP address string for reverse DNS lookup: {ipaddr}. Error: {e}")
        return 'illegal IP address string'
    except socket.timeout:
        logging.warning(f"DNS timeout during reverse DNS lookup for {ipaddr}")
        return 'DNS timeout'
    except OSError as e: 
        logging.warning(f"OS error during reverse DNS lookup for {ipaddr}: {e}")
        return 'illegal IP address string or OS error'


def renew_tor_ipaddr(ipaddr: str = '127.0.0.1', port: int = 9051, password: str = None, 
                     time_wait: float = 0.2, verbose: bool = False) -> bool:
    """
    Connects to a Tor controller and requests a new IP address (NEWNYM signal).

    Args:
        ipaddr (str): The IP address of the Tor controller. Defaults to '127.0.0.1'.
        port (int): The port number of the Tor controller. Defaults to 9051.
        password (str, optional): The password for Tor controller authentication. Defaults to None.
        time_wait (float): Short delay used between socket commands. Defaults to 0.2.
        verbose (bool): If True, logs debug messages for successful operations. Defaults to False.

    Returns:
        bool: True if the NEWNYM signal was successfully sent and acknowledged, 
              False otherwise.
    """
    conn = None 
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.settimeout(10) 
        conn.connect((ipaddr, int(port)))
        time.sleep(time_wait)

        auth_command = f'AUTHENTICATE "{password}"\r\n' if password else 'AUTHENTICATE\r\n'
        conn.send(auth_command.encode())
        auth_response = conn.recv(128).decode()
        time.sleep(time_wait)

        if '250 OK' in auth_response or 'OK' in auth_response: 
            if verbose: 
                logging.debug(f'Tor ({ipaddr}:{port}): Authentication success.')
                logging.debug(f'Tor ({ipaddr}:{port}): Requesting new IP address.')
            conn.send('SIGNAL NEWNYM\r\n'.encode())
            signal_response = conn.recv(128).decode()
            if '250 OK' in signal_response or 'OK' in signal_response:
                if verbose:
                    logging.debug(f'Tor ({ipaddr}:{port}): New IP address requested successfully.')
                return True
            else:
                logging.warning(f"Tor ({ipaddr}:{port}): Failed to signal NEWNYM. Response: {signal_response.strip()}")
                return False
        else: 
            logging.warning(f"Tor ({ipaddr}:{port}): Authentication failed. Response: {auth_response.strip()}")
            return False 

    except socket.timeout:
        logging.warning(f"Tor ({ipaddr}:{port}): Socket timeout during connection or operation.")
        return False
    except ConnectionRefusedError:
        logging.warning(f"Tor ({ipaddr}:{port}): Connection refused. Ensure Tor controller is running and accessible.")
        return False
    except (socket.error, OverflowError) as sock_err: 
        logging.warning(f"Tor ({ipaddr}:{port}): Socket error: {sock_err}")
        return False
    finally:
        if conn:
            try:
                if conn._closed is False: # Check if socket is actually open
                     conn.send('QUIT\r\n'.encode())
                     time.sleep(time_wait) 
            except (socket.error, OSError): 
                pass 
            finally:
                conn.close()
    return False


def get_new_tor_ipaddr(password: str = None, proxy: str = None, max_attempts: int = 10, 
                       time_wait: int = 5, verbose: bool = False) -> str | None:
    """
    Attempts to obtain a new external IP address by signaling a Tor controller.

    This function first gets the current IP, then repeatedly signals Tor for a 
    new identity (NEWNYM) and checks if the external IP has changed.

    Args:
        password (str, optional): Password for the Tor controller. Defaults to None.
        proxy (str, optional): The proxy server to use for fetching the external IP address.
                               If provided, its IP part is assumed to be the Tor controller IP.
                               Format: 'ip:port'. Defaults to None.
        max_attempts (int): Maximum number of attempts to get a new IP. Defaults to 10.
        time_wait (int): Base time in seconds to wait after signaling Tor. This time is
                         also used as a base for slight backoff on repeated failures.
                         Defaults to 5.
        verbose (bool): If True, enables detailed debug logging. Defaults to False.

    Returns:
        str | None: The new external IP address if successful, otherwise None.
    """
    attempts = 0
    current_ipaddr = get_ipaddr(proxy=proxy) 
    if current_ipaddr and verbose:
        logging.debug(f"Initial IP for Tor renewal: {current_ipaddr}")
    elif not current_ipaddr and verbose:
        logging.debug("Could not get initial IP before Tor renewal process.")

    # new_ipaddr = current_ipaddr # No need, new_ipaddr_attempt is used

    while attempts < max_attempts:
        logging.debug(f"Tor IP renewal attempt {attempts + 1} of {max_attempts}.")
        
        tor_controller_ip = '127.0.0.1' 
        if proxy:
            try:
                tor_controller_ip = proxy.split(':')[0]
            except Exception as e: 
                logging.warning(f"Could not parse Tor controller IP from proxy string '{proxy}'. Using default {tor_controller_ip}. Error: {e}")
        
        renew_success = renew_tor_ipaddr(ipaddr=tor_controller_ip, password=password, verbose=verbose)
        
        if not renew_success:
            logging.warning(f"Tor IP renewal signal failed on attempt {attempts + 1}.")
            time.sleep(time_wait) 
            attempts += 1
            continue 

        logging.debug(f"Waiting for {time_wait} seconds for IP to change...")
        time.sleep(time_wait)
        
        new_ipaddr_attempt = get_ipaddr(proxy=proxy)
        if new_ipaddr_attempt and verbose:
            logging.debug(f"New IP after renewal attempt {attempts + 1}: {new_ipaddr_attempt}")

        if new_ipaddr_attempt and new_ipaddr_attempt != current_ipaddr:
            logging.info(f"Successfully changed Tor IP from {current_ipaddr} to {new_ipaddr_attempt}")
            return new_ipaddr_attempt
        elif new_ipaddr_attempt == current_ipaddr:
            logging.debug(f"Tor IP address did not change from {current_ipaddr} on attempt {attempts + 1}.")
        elif not new_ipaddr_attempt:
            logging.warning(f"Could not fetch new IP address after Tor renewal signal on attempt {attempts + 1}.")

        attempts += 1
        if attempts < max_attempts: 
            wait_before_next_try = time_wait + attempts 
            logging.debug(f"Waiting {wait_before_next_try}s before next attempt...")
            time.sleep(wait_before_next_try)

    last_fetched_ip_str = new_ipaddr_attempt if 'new_ipaddr_attempt' in locals() else 'N/A'
    logging.error(f"Failed to get a new Tor IP address after {max_attempts} attempts. Last known IP: {current_ipaddr}, last fetched new IP: {last_fetched_ip_str}")
    return None 


def get_cli_args() -> argparse.Namespace:
    """
    Parses and returns command line arguments for the YouTube bot.

    Defines arguments for visits, URL, proxy, Tor usage, verbosity, and help.
    Handles basic validation like requiring --proxy if --enable-tor is used.
    Exits if --help is invoked or if required arguments are missing/invalid.

    Returns:
        argparse.Namespace: An object containing the parsed command line arguments.
                            Program exits if essential arguments are problematic.
    """
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
        help='amount of times the video will be viewed. Default: 1',
    )
    main.add_argument(
        '--url',
        help='YouTube video url',
    )
    main.add_argument(
        '--proxy',
        help='set the proxy server to be used. e.g: 127.0.0.1:8118',
    )
    main.add_argument(
        '--enable-tor',
        action='store_true',
        help='enable TOR support (You must have installed TOR at your system)',
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
        help='show this help message and exit',
    )

    args = parser.parse_args()
    if len(sys.argv) == 1 or args.help:
        parser.print_help()
        sys.exit(0) # Successful exit for help
    if args.enable_tor is True and args.proxy is None:
        # parser.error already prints to stderr and exits
        # However, if we want to log it additionally or change exit code:
        logging.error('--enable-tor requires --proxy. Please specify a proxy.')
        # parser.error will cause exit(2). If we want to control exit code,
        # we might print help and exit manually.
        # For now, let parser.error handle the exit after logging.
        parser.error('--enable-tor requires --proxy') # This will exit.
        # The following line is effectively unreachable due to parser.error exiting.
        # Consider removing parser.error if manual exit control is desired.
        sys.exit(1) 

    return args


# vim: set et ts=4 sw=4 sts=4 tw=80
