import sys
import os
import unittest
import json
from unittest.mock import patch, MagicMock

# Add the parent directory (project root) to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules import utils

class TestUtils(unittest.TestCase):

    def test_to_seconds_hms_format(self):
        self.assertEqual(utils.to_seconds("1:10:30"), 4230)

    def test_to_seconds_ms_format(self):
        self.assertEqual(utils.to_seconds("10:30"), 630)

    def test_to_seconds_s_format_string(self):
        # Current implementation of to_seconds expects H:M:S, M:S.
        # If only one value 'S' is given, it's treated as M by current logic if it's a string.
        # e.g. "30" -> M:S -> 30 minutes. This test reflects current behavior.
        # If it were to support "S" directly, to_seconds("30") would be 30.
        # For now, testing as "0:S"
        self.assertEqual(utils.to_seconds("0:30"), 30) 
        self.assertEqual(utils.to_seconds("30"), 1800) # "30" is treated as 30 minutes

    def test_to_seconds_list_input(self):
        self.assertEqual(utils.to_seconds(['1', '10', '30']), 4230)
        self.assertEqual(utils.to_seconds(['0','0','30']), 30)

    def test_to_seconds_zero_values(self):
        self.assertEqual(utils.to_seconds("0:0:0"), 0)
        self.assertEqual(utils.to_seconds("0:0"), 0)
        self.assertEqual(utils.to_seconds("0"), 0) # "0" treated as 0 minutes

    def test_to_seconds_invalid_format(self):
        with self.assertRaises(ValueError):
            utils.to_seconds("1:2:3:4") # Too many parts
        with self.assertRaises(ValueError):
            utils.to_seconds("a:b:c") # Non-numeric
        with self.assertRaises(TypeError):
            utils.to_seconds(123) # Incorrect type
        with self.assertRaises(ValueError):
            utils.to_seconds("1:") # Incomplete parts

    def test_user_agent_returns_string(self):
        ua = utils.user_agent()
        self.assertIsInstance(ua, str)
        self.assertTrue(len(ua) > 0)

    def test_user_agent_looks_like_ua(self):
        ua = utils.user_agent()
        self.assertIn("Mozilla", ua) # Basic sanity check

    @patch('modules.utils.requests.get')
    def test_get_ipaddr_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'origin': '123.45.67.89'}
        mock_get.return_value = mock_response

        ip = utils.get_ipaddr()
        self.assertEqual(ip, '123.45.67.89')
        mock_get.assert_called_once_with('http://httpbin.org/ip', proxies=None, timeout=10)

    @patch('modules.utils.requests.get')
    def test_get_ipaddr_request_exception(self, mock_get):
        mock_get.side_effect = utils.RequestException("Test network error")
        ip = utils.get_ipaddr()
        self.assertIsNone(ip)

    @patch('modules.utils.requests.get')
    def test_get_ipaddr_http_error(self, mock_get):
        mock_response = MagicMock()
        # Configure the mock to simulate raise_for_status() raising an HTTPError
        mock_http_error = utils.requests.exceptions.HTTPError("Test HTTP error")
        mock_http_error.response = MagicMock() # Mock the response attribute of the error
        mock_http_error.response.status_code = 404
        mock_response.raise_for_status.side_effect = mock_http_error
        mock_get.return_value = mock_response
        
        ip = utils.get_ipaddr()
        self.assertIsNone(ip)

    @patch('modules.utils.requests.get')
    def test_get_ipaddr_json_decode_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200 # HTTP request is fine
        mock_response.json.side_effect = json.JSONDecodeError("e", "doc", 0)
        mock_get.return_value = mock_response

        ip = utils.get_ipaddr()
        self.assertIsNone(ip)

    @patch('modules.utils.requests.get')
    def test_get_ipaddr_with_proxy(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'origin': '123.45.67.89'}
        mock_get.return_value = mock_response
        
        proxy_str = "127.0.0.1:8118"
        ip = utils.get_ipaddr(proxy=proxy_str)
        self.assertEqual(ip, '123.45.67.89')
        expected_proxies = {'http': f'http://{proxy_str}', 'https': f'http://{proxy_str}'}
        mock_get.assert_called_once_with('http://httpbin.org/ip', proxies=expected_proxies, timeout=10)


if __name__ == '__main__':
    unittest.main()
