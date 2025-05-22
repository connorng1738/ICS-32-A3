# ds_messenger.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Connor Ng
# ngce@uci.edu
# ngce
import socket
import time
from ds_protocol import *


class DirectMessage:
  def __init__(self, recipient = None, message = None, sender = None, timestamp = None):
    self.recipient = recipient
    self.message = message
    self.sender = sender
    self.timestamp = timestamp
  
class DirectMessenger:
  def __init__(self, dsuserver = None, port = 3001, username = None, password=None): 
    self.port = port
    self.dsuserver = dsuserver
    self.username = username
    self.password = password
    self.timestamp = None
    self.token = None
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect((self.dsuserver, self.port)) 

    self.writer = self.socket.makefile('w')
    self.reader = self.socket.makefile('r')

    auth_msg = authenticate_request(username, password) 
    self.writer.write(auth_msg + "\r\n")
    self.writer.flush()

    srv_msg = self.reader.readline()
    print(f"Response recieved from server: {srv_msg}")
    
    resp = extract_json(srv_msg)
    if resp.type == 'ok':
      self.token = resp.token
    else:
      raise Exception("Could not authenticate") 

  def send(self, message:str, recipient:str) -> bool:
    # must return true if message successfully sent, false if send failed.

    if not self.token:
      return False 
    
    direct_message = direct_message_request(self.token, message, recipient, time.time())
    print(f"Sending: {direct_message}")
    self.writer.write(direct_message)
    self.writer.flush()

    response = self.reader.readline()
    print(f"Server response: {response}")

    parsed = extract_json(response)
    if parsed.type == 'ok':
      return True
    else:
      print(f"Failed to send: {parsed.message}") 
      return False

  def retrieve_new(self) -> list: 
    # must return a list of DirectMessage objects containing all new messages
    if not self.token:
      return []
    
    new_fetch_request = fetch_request(self.token, "unread")
    parsed = self.parse_message(new_fetch_request)
    
    messages = []

    if parsed.type == 'ok' and parsed.messages:
      print('line 89')
      for msg in parsed.messages: 
        dm = DirectMessage(
          sender = msg.get('from', None),
          message = msg.get('message', None),
          timestamp = msg.get('timestamp',None)
          )
        messages.append(dm)
    #elif parsed.type == 'error': 
      #pass# incldue condition for this
    return messages
          

  def retrieve_all(self) -> list:
    if not self.token:
      return []
    

    all_fetch_request = fetch_request(self.token, "all")
    parsed = self.parse_message(all_fetch_request)
    messages = []

    if parsed.type == 'ok' and parsed.messages:
      for msg in parsed.messages:
        print('line 89')
        dm = DirectMessage(
            sender = msg.get('from',None),
            recipient = self.username,
            message = msg.get('message', None),
            timestamp = msg.get('timestamp', None)
        )

        messages.append(dm)
    return messages

  def parse_message(self, fetch_request) -> DSPResponse:
    self.writer.write(fetch_request + '\r\n')
    
    self.writer.flush()
    response = self.reader.readline()
    parsed = extract_json(response)
    return parsed



      