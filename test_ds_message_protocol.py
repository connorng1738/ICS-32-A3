"""
Unit tests for the ds_protocol module.

This module contains test cases for various protocol functions including
JSON extraction, authentication, direct messaging, and fetch requests.
"""

import json
import unittest
from ds_protocol import (extract_json,
                         authenticate_request,
                         direct_message_request,
                         fetch_request,
                         DSPResponse)


class TestProtocol(unittest.TestCase):
    """
    Test cases for the ds_protocol module functions.
    """

    def test_extract_json(self):
        """
        Test extraction of JSON from a sample response string.
        """
        sample_response = """
        {
          "response": {
            "type": "ok",
            "message": "Success",
            "token": "abc123",
            "messages": [{"from": "user1", "message": "Hi"}]
          }
        }
        """

        parsed = extract_json(sample_response)
        expected = DSPResponse(
            type='ok',
            message='Success',
            token='abc123',
            messages=[{'from': 'user1', 'message': 'Hi'}]
        )
        self.assertEqual(parsed, expected)

    def test_extract_json_raise_exception(self):
        """
        Test extract_json function with malformed JSON input.
        """
        bad_json = '{"name": "John", "age":30,}'
        output = extract_json(bad_json)

        self.assertIsNone(output.token)
        self.assertIsNone(output.message)
        self.assertEqual(output.messages, [])
        self.assertIsNone(output.type)

    def test_authenticate(self):
        """
        Test authentication request generation.
        """
        auth_msg = authenticate_request("test_user", "test_pass")
        parsed = json.loads(auth_msg)
        expected = {
            "authenticate": {
                "username": "test_user",
                "password": "test_pass"
            }
        }
        self.assertEqual(parsed, expected)

    def test_dm_request(self):
        """
        Test direct message request generation.
        """
        dm_msg = direct_message_request(
            "token123", "Hello!", "recipient", 123.45)
        parsed = json.loads(dm_msg)
        expected = {
            "token": "token123",
            "directmessage": {
                "entry": "Hello!",
                "recipient": "recipient",
                "timestamp": "123.45"
            }
        }
        self.assertEqual(parsed, expected)

    def test_fetch(self):
        """
        Test fetch request generation.
        """
        fetch_msg = fetch_request("token123", "all")
        parsed = json.loads(fetch_msg)
        expected = {"token": "token123", "fetch": "all"}
        self.assertEqual(parsed, expected)


if __name__ == '__main__':
    unittest.main()
