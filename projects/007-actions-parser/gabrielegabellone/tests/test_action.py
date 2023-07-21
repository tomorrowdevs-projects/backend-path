import unittest
from unittest.mock import MagicMock, patch
import io
import sys

from action_parser.action import Action


class TestActionHTTPRequestAction(unittest.TestCase):
    def setUp(self):
        self.name = "location"
        self.type = "HTTPRequestAction"
        self.options = {"url": "http://free.ipwhois.io/json/"}

    @patch("action_parser.action.requests")
    def test_execute(self, mock_requests):
        """Goes to test that when the action is performed, the event returned in output is equal to the one given in
        input plus a key that is the name of the action performed and whose value is the JSON returned by the
        request."""
        action = Action(self.type, self.name, self.options)
        event_input = {}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "country_phone": "+39",
            "region": "Lazio",
            "city": "Rome"
        }

        mock_requests.get.return_value = mock_response

        actual = action.execute(event_input)
        expected = {"location": {"country_phone": "+39", "region": "Lazio", "city": "Rome"}}
        self.assertEqual(actual, expected, "Expected a different output event.")

    @patch("action_parser.action.requests")
    def test_execute_status_code_non_2XX(self, mock_requests):
        """Tests that if, during the execution of an action, a non-2XX status code is returned from a request,
        the program is stopped."""
        action = Action(self.type, self.name, self.options)
        event_input = {}

        mock_response = MagicMock()
        mock_response.status_code = 404

        mock_requests.get.return_value = mock_response

        with self.assertRaises(SystemExit):
            action.execute(event_input)

    @patch("action_parser.action.requests")
    def test_execute_connection_error(self, mock_requests):
        """Tests that if a ConnectionError occurs during the execution of an action, the program is stopped."""
        action = Action(self.type, self.name, self.options)
        event_input = {}

        mock_requests.get.side_effect = ConnectionError

        with self.assertRaises(SystemExit):
            action.execute(event_input)


class TestActionPrintAction(unittest.TestCase):
    def setUp(self):
        self.name = "print"
        self.type = "PrintAction"
        self.options = {"message": "test print action"}

    def test_execute(self):
        """Goes to test that when the action is executed, the message in the options attribute is printed to the
        console and that the event returned in output is equal to the one given in input."""
        action = Action(self.type, self.name, self.options)
        event_input = {"location": {"region": "Lazio", "city": "Rome"}}

        captured_output = io.StringIO()     # create StringIO object
        sys.stdout = captured_output        # redirect stdout
        event_output = action.execute(event_input)  # call function that does the print
        sys.stdout = sys.__stdout__         # reset redirect

        actual = captured_output.getvalue().strip()
        expected = "test print action"
        self.assertEqual(actual, expected, "Expected another string printed in console.")

        self.assertEqual(event_output, event_input, "Expected that the returned output event is equal to the input "
                                                    "event when the action is of type 'PrintAction'.")


