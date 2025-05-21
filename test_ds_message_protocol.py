from ds_protocol import *
import unittest
import json

class TestProtocol(unittest.TestCase):
    def test_extract_json(self):
      sample_response ="""
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
      expected = DSPResponse(type='ok', message='Success', token='abc123', messages=[{'from': 'user1', 'message': 'Hi'}])
      self.assertEqual(parsed, expected)

    def test_extract_json_raise_exception(self):
        bad_json = '{"name": "John", "age":30,}'
        output = extract_json(bad_json)
        assert output.token == None and output.message == None and output.messages == [] and output.type == None

    def test_authenticate(self):
        auth_msg = authenticate_request("test_user", "test_pass")
        parsed = json.loads(auth_msg)
        expected = {"authenticate": {"username": "test_user", "password": "test_pass"}}
        self.assertEqual(parsed, expected)

    def test_dm_request(self):
        dm_msg = direct_message_request("token123", "Hello!", "recipient", 123.45)
        parsed = json.loads(dm_msg)
        expected = {"token": "token123", "directmessage": {"entry": "Hello!", "recipient": "recipient", "timestamp": "123.45"}}
        self.assertEqual(parsed, expected)
    
    def test_fetch(self):
        fetch_msg = fetch_request("token123", "all")
        parsed = json.loads(fetch_msg)
        expected = {"token": "token123", "fetch": "all"}
        self.assertEqual(parsed, expected)

if __name__ == '__main__':
    unittest.main()









