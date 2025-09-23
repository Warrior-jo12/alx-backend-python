import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize

# ------------------------
# Tests for access_nested_map
# ------------------------
class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b")
    ])
    def test_access_nested_map_exception(self, nested_map, path, key):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), repr(key))

# ------------------------
# Tests for get_json
# ------------------------
class TestGetJson(unittest.TestCase):
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload):
        with patch("utils.requests.get") as mocked_get:
            mocked_get.return_value = Mock(json=Mock(return_value=test_payload))
            result = get_json(test_url)

            # Test result
            self.assertEqual(result, test_payload)
            # Test requests.get called exactly once with test_url
            mocked_get.assert_called_once_with(test_url)

# ------------------------
# Tests for memoize
# ------------------------
class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        obj = TestClass()
        with patch.object(TestClass, "a_method", return_value=42) as mocked_method:
            # Call the property twice
            result1 = obj.a_property
            result2 = obj.a_property

            # Assert results are correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Assert a_method called only once
            mocked_method.assert_called_once()

# Run all tests
if __name__ == "__main__":
    unittest.main()
