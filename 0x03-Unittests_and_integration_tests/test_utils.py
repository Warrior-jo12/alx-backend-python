#!/usr/bin/env python3
"""Unit tests for utils functions: access_nested_map, get_json, and memoize."""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize

class TestAccessNestedMap(unittest.TestCase):
    """Test case for access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that access_nested_map returns the expected value.

        Parameters
        ----------
        nested_map : dict
            The dictionary to access.
        path : tuple
            The sequence of keys to traverse.
        expected : any
            The expected result from accessing the nested map.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, key):
        """
        Test that access_nested_map raises KeyError for invalid paths.

        Parameters
        ----------
        nested_map : dict
            The dictionary to access.
        path : tuple
            The sequence of keys to traverse.
        key : str
            The expected key causing KeyError.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), repr(key))


class TestGetJson(unittest.TestCase):
    """Test case for get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """
        Test get_json returns expected JSON without making real HTTP calls.

        Parameters
        ----------
        test_url : str
            The URL to fetch JSON from.
        test_payload : dict
            The expected JSON payload.
        """
        with patch("utils.requests.get") as mocked_get:
            mocked_get.return_value = Mock(
                json=Mock(return_value=test_payload)
            )
            result = get_json(test_url)
            self.assertEqual(result, test_payload)
            mocked_get.assert_called_once_with(test_url)

class TestMemoize(unittest.TestCase):
    """Test case for memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches the result after first call."""

        class TestClass:
            """Dummy class to test memoization."""

            def a_method(self):
                """Return a fixed value."""
                return 42

            @memoize
            def a_property(self):
                """Return a memoized property."""
                return self.a_method()
                
        obj = TestClass()
        with patch.object(TestClass, "a_method", return_value=42) as mocked_method:
            result1 = obj.a_property
            result2 = obj.a_property
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mocked_method.assert_called_once()
if __name__ == "__main__":
    unittest.main()
