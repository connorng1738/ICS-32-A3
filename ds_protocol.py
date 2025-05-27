# ds_protocol.py

# Starter code for assignment 2 in ICS 32 Programming with Software
# Libraries in Python

# Replace the following placeholders with your information.

# Connor Ng
# ngce@uci.edu
# ngce

import json
from collections import namedtuple
from typing import Optional, List, Dict, Any


# Create a namedtuple to hold the values we expect to retrieve from json
# messages.
DSPResponse = namedtuple(
    'DSPResponse', [
        'type', 'message', 'token', 'messages'])


def extract_json(json_msg: str) -> DSPResponse:
    """
    Call the json.loads function on a json string and convert it to a DSPResponse object.
    
    Arguments:
    json_msg: the JSON string to parse and extract data from
    
    Returns:
    DSPResponse: namedtuple containing type, message, token, and messages from the JSON
    """
    try:
        json_obj = json.loads(json_msg)
        response = json_obj.get('response')
        type_ = response.get('type')
        message = response.get('message')
        token = response.get('token')
        messages = response.get('messages', [])
        return DSPResponse(type_, message, token, messages)

    except json.JSONDecodeError:  # do i need to test this error
        print("Json cannot be decoded.")
        return DSPResponse(None, None, None, [])


def authenticate_request(username: str, password: str) -> str:
    """
    Create a JSON authentication request string with username and password.
    
    Arguments:
    username: the username for authentication
    password: the password for authentication
    
    Returns:
    str: JSON string containing the authentication request
    """
    return json.dumps({"authenticate":
                       {"username": username,
                        "password": password}})


def direct_message_request(
        token: str,
        message: str,
        recipient: str,
        timestamp: float) -> str:
    """
    Create a JSON direct message request string with token, message content, recipient, and timestamp.
    
    Arguments:
    token: the authentication token for the request
    message: the message content to send
    recipient: the username of the message recipient
    timestamp: the timestamp when the message was created
    
    Returns:
    str: JSON string containing the direct message request
    """
    return json.dumps({"token": token,
                       "directmessage": {
                           "entry": message,
                           "recipient": recipient,
                           "timestamp": str(timestamp)
                       }})


def fetch_request(token: str, fetch_type: str) -> str:
    """
    Create a JSON fetch request string to retrieve messages from the server.
    
    Arguments:
    token: the authentication token for the request
    fetch_type: the type of fetch request ("all" or "unread")
    
    Returns:
    str: JSON string containing the fetch request
    """
    return json.dumps({
        "token": token,
        "fetch": fetch_type
    })