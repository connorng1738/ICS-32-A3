"""
Unit tests for the ds_messenger module.

This module contains test cases for the DirectMessenger class including
authentication, message sending, and message retrieval functionality.
"""

import unittest
from unittest.mock import patch
from ds_messenger import DirectMessenger


class TestMessenger(unittest.TestCase):
    """
    est cases for the DirectMessenger class.
    """

    def setUp(self):
        """
        Set up test fixtures with DirectMessenger instances.
        """
        self.dm = DirectMessenger(
            dsuserver='localhost',
            username='testuser',
            password='testpass'
        )
        self.dm5 = DirectMessenger(
            dsuserver='localhost',
            username='testuser5',
            password='testpass5'
        )

    def test_invalid_user(self):
        """
        Test that invalid credentials raise an exception.
        """
        with self.assertRaises(Exception):
            DirectMessenger(
                dsuserver='localhost',
                username='testuser',
                password='testpass2'
            )

    def test_send_not_token(self):
        """
        Test send method behavior when no authentication token is present.
        """
        self.dm.token = None
        test_send = self.dm.send('test_message', 'test_username')
        self.assertFalse(test_send)

    def test_send_error(self):
        """
        Test send method behavior when server returns an error response.
        """
        self.dm.reader.readline = lambda: (
            '{"response": {"type": "error", "message": "fail"}}\n'
        )
        test_send = self.dm.send('test123', 'test_username')
        self.assertFalse(test_send)

    def test_receive_new_not_token(self):
        """
        Test retrieve_new method behavior when no authentication
        token is present.
        """
        self.dm.token = None
        test_send = self.dm.retrieve_new()
        self.assertIsInstance(test_send, list)

    def test_retrieve_new_returns_list(self):
        """
        Test that retrieve_new method returns a list.
        """
        new_messages = self.dm.retrieve_new()
        self.assertIsInstance(new_messages, list)

    def test_retrieve_new_empty(self):
        """
        Test retrieve_new method with empty message response.
        """
        mock_response = '{"response": {"type": "ok", "messages": []}}'
        with patch.object(self.dm.reader,
                          'readline',
                          return_value=mock_response):
            messages = self.dm.retrieve_new()
            self.assertEqual(len(messages), 0)

    def test_retrieve_new_valid(self):
        """
        Test retrieve_new method with valid message exchange.
        """
        dm2 = DirectMessenger(dsuserver='localhost', username='test_user_2')

        self.dm.send('msg 1', 'test_user_2')
        msgs = dm2.retrieve_new()
        self.assertEqual(len(msgs), 1)
        self.assertEqual(msgs[0].message, "msg 1")

        self.dm.send('msg 2', 'test_user_2')
        msgs = dm2.retrieve_new()
        self.assertEqual(len(msgs), 1)
        self.assertEqual(msgs[0].message, "msg 2")

    def test_retrieve_all(self):
        """
        Test that retrieve_all method returns a list of all messages.
        """
        all_messages = self.dm.retrieve_all()
        self.assertIsInstance(all_messages, list)

    def test_receive_all_not_token(self):
        """
        Test retrieve_all method behavior when no
        authentication token is present.
        """
        self.dm.token = None
        test_send = self.dm.retrieve_all()
        self.assertIsInstance(test_send, list)

    def test_retrieve_all_valid(self):
        """
        Test retrieve_all method with valid message exchange.
        """
        dm3 = DirectMessenger(dsuserver='localhost', username='Leo')
        old_len = len(dm3.retrieve_all())

        self.dm.send('Hi', 'Leo')

        msgs = dm3.retrieve_all()
        self.assertGreater(len(msgs), old_len)
        self.assertEqual(msgs[old_len].message, "Hi")

    def test_retrieve_all_empty(self):
        """
        Test retrieve_all method with empty message response.
        """
        self.dm.reader.readline = lambda: (
            '{"response": {"type": "ok", "messages": []}}\n'
        )
        messages = self.dm.retrieve_all()
        self.assertEqual(len(messages), 0)


if __name__ == '__main__':
    unittest.main()
