import unittest

from action_parser.options import Options


class TestOptions(unittest.TestCase):
    def setUp(self):
        self.event = {"foo": {"bar": "World"}}

    def test_format(self):
        """Test that the contents of the Options object are formatted correctly when the keys are all found in the
        event."""
        event = self.event
        options = Options(type="Message", content="Hello {{foo.bar}}!")
        options.format(event)
        actual = options.content
        expected = "Hello World!"
        self.assertEqual(actual, expected, "Expected content to be formatted in another way.")

    def test_format_key_error(self):
        """Tests that the contents of the Options object are formatted correctly when a key error occurs."""
        event = self.event
        options = Options(type="Message", content="Hello {{foo.qux}}!")
        options.format(event)
        actual = options.content
        expected = "Hello !"
        self.assertEqual(actual, expected, "Expected content to be formatted in another way.")

    def test_format_incomplete_braces(self):
        """Tests that the contents of the Options object are formatted correctly when there are incomplete braces."""
        event = self.event
        options = Options(type="Message", content="Hello {{foo.bar}!")
        options.format(event)
        actual = options.content
        expected = "Hello {{foo.bar}!"
        self.assertEqual(actual, expected, "Expected content to be formatted in another way.")

    def test_format_additional_braces(self):
        """Tests that the contents of the Options object are formatted correctly when there are additional braces."""
        event = self.event
        options = Options(type="Message", content="Hello {{foo.bar}}! }}")
        options.format(event)
        actual = options.content
        expected = "Hello World! }}"
        self.assertEqual(actual, expected, "Expected content to be formatted in another way.")

    def test_get_option_value_with_periods(self):
        """Test that returns the correct value, if a dot-delimited option key is passed."""
        option_key = "foo.bar"
        event = self.event
        actual = Options.get_option_value(option_key, event)
        expected = "World"
        self.assertEqual(actual, expected, "Expected to return another option value.")

    def test_get_option_value_single_without_periods(self):
        """Test that returns the correct value if a non-dot-delimited option key is passed."""
        option_key = "Hello"
        event = {"Hello": "World"}
        actual = Options.get_option_value(option_key, event)
        expected = "World"
        self.assertEqual(actual, expected, "Expected to return another option value.")

    def test_get_option_value_key_error(self):
        """Tests for an empty string to be returned if a key error occurs."""
        option_key = "foo.qux"
        event = self.event
        actual = Options.get_option_value(option_key, event)
        expected = ""
        self.assertEqual(actual, expected, "Expected to return another option value.")
