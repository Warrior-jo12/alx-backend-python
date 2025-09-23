#!/usr/bin/env python3
import unittest
import utils
from parameterized import parameterized
from utils import access_nested_map 
from unittest.mock import patch, Mock
from parameterized import parameterized



class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        # ensure the KeyError message matches the missing key
        self.assertEqual(str(context.exception), repr(path[-1]))

 
class TestGetJson(unittest.TestCase):
    """Unit tests for get_json"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        # Configure the mock to return a response with .json() method
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = utils.get_json(test_url)

        # Assertions
        mock_get.assert_called_once_with(test_url)  # check call with URL
        self.assertEqual(result, test_payload)      # check returned data

if __name__ == "__main__":
    unittest.main()
