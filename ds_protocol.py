# ds_protocol.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Connor Ng
# ngce@uci.edu
# ngce

import json
from collections import namedtuple


# Create a namedtuple to hold the values we expect to retrieve from json messages.
DSPResponse = namedtuple('DSPResponse', ['type', 'message', 'token', 'messages'])

def extract_json(json_msg:str) -> DSPResponse:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  '''
  try:
    json_obj = json.loads(json_msg)
    response = json_obj.get('response')
    type_ = response.get('type')
    message = response.get('message')
    token = response.get('token')
    messages = response.get('messages', [])
    return DSPResponse(type_, message, token, messages)

  except json.JSONDecodeError: #do i need to test this error
    print("Json cannot be decoded.")
    return DSPResponse(None, None, None, [])

def authenticate_request(username: str, password: str) -> str:
  return json.dumps({"authenticate": 
                     {"username": username,
                      "password": password}})

def direct_message_request(token: str, message: str, recipient: str, timestamp: float) -> str:
  return json.dumps({"token": token,
                     "directmessage":{
                        "entry": message,
                        "recipient": recipient,
                        "timestamp": str(timestamp)
                     }})

def fetch_request(token: str, fetch_type: str) -> str:
  return json.dumps({
    "token": token,
    "fetch": fetch_type
  })

"""def send() -> namedtuple:
  #send data to serverm receive hte response, and return the parsed respons eot caller
  pass

def recieve_json() -> namedtuple:
  pass"""

