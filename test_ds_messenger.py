import unittest
from unittest.mock import patch
from ds_messenger import *
import time
# coverage run -m --branch pytest .
# coverage report -m

#run auth_request again with different token
class TestMessenger(unittest.TestCase):
    def setUp(self):
        self.dm = DirectMessenger(dsuserver = 'localhost', username = 'testuser', password = 'testpass')
        self.dm5 =  DirectMessenger(dsuserver = 'localhost', username = 'testuser5', password = 'testpass5')
    
    def test_invalid_user(self):
        with self.assertRaises(Exception):
            self.dm_invalid = DirectMessenger(dsuserver = 'localhost', username = 'testuser', password = 'testpass2')

    def test_send_not_token(self):
        self.dm.token = None
        test_send = self.dm.send('test_message', 'test_username')
        self.assertFalse(test_send)

    def test_send_error(self):
        self.dm.reader.readline = lambda: '{"response": {"type": "error", "message": "fail"}}\n'
        test_send = self.dm.send('test123', 'test_username')
        self.assertFalse(test_send)
  
    def test_recieve_new_not_token(self): 
        self.dm.token = None
        test_send = self.dm.retrieve_new()
        self.assertIsInstance(test_send, list)

    def test_retrieve_new_returns_list(self):
        new_messages = self.dm.retrieve_new()
        self.assertIsInstance(new_messages, list)
    

    
    def test_retrieve_new_empty(self):
        with patch.object(self.dm.reader, 'readline', return_value = '{"response": {"type": "ok", "messages": []}}'):
            messages = self.dm.retrieve_new()
            self.assertEqual(len(messages), 0)  # Should return empty list
            
    def test_retrieve_new_valid(self):
        dm2 = DirectMessenger(dsuserver ='localhost', username = 'test_user_2')
        self.dm.send('msg 1','test_user_2')
        msgs = dm2.retrieve_new()
        self.assertEqual(len(msgs), 1)
        self.assertEqual(msgs[0].message, "msg 1")

        self.dm.send('msg 2','test_user_2')
        msgs = dm2.retrieve_new()
        self.assertEqual(len(msgs), 1)
        self.assertEqual(msgs[0].message, "msg 2")

    def test_retrieve_all(self): #in the setup, send a message to an imaginary server, in the test cases, you see how would fetch all work. #
        #in on test case, you fetch unread from the other party, you can take two direct messengers, one from alice to bob, and fetch unread from bob's side. 
        #the recieved message from bob is the one that alice sent

        all_messages = self.dm.retrieve_all()
        self.assertIsInstance(all_messages, list)

    def test_recieve_all_not_token(self):
        self.dm.token = None
        test_send = self.dm.retrieve_all()
        self.assertIsInstance(test_send, list)
        
    def test_retrieve_all_valid(self): 
        dm3 = DirectMessenger(dsuserver='localhost', username='Leo')
        old_len = len(dm3.retrieve_all())

        self.dm.send('Hi', 'Leo')

        msgs = dm3.retrieve_all()
        self.assertGreater(len(msgs), old_len)
        self.assertEqual(msgs[old_len].message, "Hi")
                         
    def test_retrieve_all_empty(self):
        self.dm.reader.readline = lambda: '{"response": {"type": "ok", "messages": []}}\n' 
        messages = self.dm.retrieve_all()
        self.assertEqual(len(messages), 0)

if __name__ == '__main__':
    unittest.main()
    