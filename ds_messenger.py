# ds_messenger.py
# Connor Ng
# ngce@uci.edu
# ngce
import socket
import time
from ds_protocol import *


class DirectMessage:
    """
    Represents a direct message with sender, recipient, message content, and timestamp information.
    """
    
    def __init__(self,
                 recipient: str = None,
                 message: str = None,
                 sender: str = None,
                 timestamp: float = None) -> None:
        """
        Initialize a DirectMessage object.
        
        Arguments:
        recipient: the username of the message recipient
        message: the content of the message
        sender: the username of the message sender
        timestamp: the timestamp when the message was sent
        """
        self.recipient = recipient
        self.message = message
        self.sender = sender
        self.timestamp = timestamp


class DirectMessenger:
    """
    Handles direct messaging functionality including authentication, sending messages, 
    and retrieving messages from a DSU server.
    """
    
    def __init__(self,
                 dsuserver: str = None,
                 port: int = 3001,
                 username: str = None,
                 password: str = None) -> None:
        """
        Initialize DirectMessenger and establish connection to DSU server with authentication.
        
        Arguments:
        dsuserver: the hostname or IP address of the DSU server
        port: the port number for the DSU server connection (default 3001)
        username: the username for authentication
        password: the password for authentication
        """
        self.port = int(port)
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

    def send(self, 
             message: str, 
             recipient: str) -> bool:
        """
        Send a direct message to a specified recipient.
        
        Arguments:
        message: str, the content of the message to send
        recipient: str, the username of the message recipient
        
        Returns:
        bool: True if message was sent successfully, False otherwise
        """
        if not self.token:
            return False

        direct_message = direct_message_request(
            self.token, message, recipient, time.time())
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

    def retrieve_new(self) -> list[DirectMessage]:
        """
        Retrieve all new (unread) messages from the server.
        
        Returns:
        list: A list of DirectMessage objects containing new messages
        """
        if not self.token:
            return []

        new_fetch_request = fetch_request(self.token, "unread")
        parsed = self.parse_message(new_fetch_request)

        messages = []

        if parsed.type == 'ok' and parsed.messages:
            for msg in parsed.messages:
                dm = DirectMessage(
                    sender=msg.get('from', None),
                    message=msg.get('message', None),
                    timestamp=msg.get('timestamp', None)
                )
                messages.append(dm)
        # elif parsed.type == 'error':
            # pass# incldue condition for this
        return messages

    def retrieve_all(self) -> list[DirectMessage]:
        """
        Retrieve all messages (both read and unread) from the server.
        
        Returns:
        list: A list of DirectMessage objects containing all messages
        """
        if not self.token:
            return []

        all_fetch_request = fetch_request(self.token, "all")
        parsed = self.parse_message(all_fetch_request)
        messages = []

        if parsed.type == 'ok' and parsed.messages:
            for msg in parsed.messages:
                dm = DirectMessage(
                    sender=msg.get('from', None),
                    recipient=self.username,
                    message=msg.get('message', None),
                    timestamp=msg.get('timestamp', None)
                )
                messages.append(dm)
        return messages

    def parse_message(self, fetch_request) -> DSPResponse:
        """
        Send a fetch request to the server and parse the response.
        
        Arguments:
        fetch_request: str, the formatted fetch request string to send to the server
        
        Returns:
        DSPResponse: The parsed response object from the server
        """
        self.writer.write(fetch_request + '\r\n')

        self.writer.flush()
        response = self.reader.readline()
        parsed = extract_json(response)
        return parsed