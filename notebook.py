# ICS 32
# Assignment #1: Diary
#
# Author: Aaron Imani
#
# v0.1.0

# You should review this code to identify what features you need to support
# in your program for assignment 1.
#
# YOU DO NOT NEED TO READ OR UNDERSTAND THE JSON SERIALIZATION ASPECTS OF THIS CODE 
# RIGHT NOW, though can you certainly take a look at it if you are curious since we 
# already covered a bit of the JSON format in class.

import json, time
from pathlib import Path


class NotebookFileError(Exception):
    """
    NotebookFileError is a custom exception handler that you should catch in your own code. It
    is raised when attempting to load or save Notebook objects to file the system.
    """
    pass

class IncorrectNotebookError(Exception):
    """
    NotebookError is a custom exception handler that you should catch in your own code. It
    is raised when attempting to deserialize a notebook file to a Notebook object.
    """
    pass


class Diary(dict):
    """ 

    The Diary class is responsible for working with individual user diaries. It currently 
    supports two features: A timestamp property that is set upon instantiation and 
    when the entry object is set and an entry property that stores the diary message.

    """
    def __init__(self, entry:str = None, timestamp:float = 0):
        self._timestamp = timestamp
        self.set_entry(entry)

        # Subclass dict to expose Diary properties for serialization
        # Don't worry about this!
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)
    
    def set_entry(self, entry):
        self._entry = entry 
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):
        return self._entry
    
    def set_time(self, time:float):
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)
    
    def get_time(self):
        return self._timestamp

    """

    The property method is used to support get and set capability for entry and 
    time values. When the value for entry is changed, or set, the timestamp field is 
    updated to the current time.

    """ 
    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)

class DirectMessage(Diary):
    def __init__(self, entry, sender, recipient, timestamp = 0):
        super().__init__(entry, timestamp)
        self.sender = sender
        self.recipient = recipient
        dict.__setitem__(self, 'sender', sender)
        if recipient:
            dict.__setitem__(self, 'recipient', recipient)
    
    def to_dict(self):
        base = {
            "message": self.entry,
            "timestamp": self.timestamp,
        }
        if self.recipient:
            base['recipient'] = self.recipient
        else:
            base['from'] = self.sender
        return base

    @classmethod
    def from_dict(cls, d):
        entry = d['message']
        timestamp = d['timestamp']
        if 'from' in d:
            sender = d['from']
            return cls(entry, sender, None, timestamp)
        elif 'recipient' in d:
            sender = d.get('sender', '')
            recipient = d['recipient']
            return cls(entry, sender, recipient, timestamp)
        else:
            raise ValueError

class Conversation:
    def __init__ (self, recipient: str):
        self.recipient = recipient
        self.messages =[]
    
    def add_message(self, message: Diary):
        self.messages.append(message)
    
    def get_message(self) -> list[Diary]:
        return self.messages
    
    def get_recipient(self) -> list[Diary]:
        return self.recipient

    
class Notebook:
    """Notebook is a class that can be used to manage a diary notebook."""

    def __init__(self, username: str, password: str, host: str, port: int, path: str):
        """Creates a new Notebook object. 
        
        Args:
            username (str): The username of the user.
            password (str): The password of the user
        """
        self.username = username 
        self.password = password 
        self.host = host
        self.port = port
        self.path = path
        self._diaries = []
        self.conversations = {} #recipient:str -> list[direct message objects]
    

    def add_diary(self, diary: Diary) -> None:
        """Accepts a Diary object as parameter and appends it to the diary list. Diaries 
        are stored in a list object in the order they are added. So if multiple Diary objects 
        are created, but added to the Profile in a different order, it is possible for the 
        list to not be sorted by the Diary.timestamp property. So take caution as to how you 
        implement your add_diary code.

        """
        self._diaries.append(diary)


    def del_diary(self, index: int) -> bool:
        """
        Removes a Diary at a given index and returns `True` if successful and `False` if an invalid index was supplied. 

        To determine which diary to delete you must implement your own search operation on 
        the diary returned from the get_diaries function to find the correct index.

        """
        try:
            del self._diaries[index]
            return True
        except IndexError:
            return False
        
    def get_diaries(self) -> list[Diary]:
        """Returns the list object containing all diaries that have been added to the Notebook object"""
        return self._diaries

    def save(self, path: str) -> None:
        """
        Accepts an existing notebook file to save the current instance of Notebook to the file system.

        Example usage:
        
        ```
        notebook = Notebook('jo)
        notebook.save('/path/to/file.json')
        ```

        Raises NotebookFileError, IncorrectNotebookError
        """
        p = Path(path)

        if p.suffix != '.json':
            raise NotebookFileError("Invalid notebook file path or type")

    # Convert conversations dictionary into serializable form
        conversations_serializable = {
            recipient: conv.get_message()
            for recipient, conv in self.conversations.items()
        }

        notebook_dict = {
            'username': self.username,
            'password': self.password,
            'host': self.host,
            'port': self.port,
            '_diaries': [dict(diary) for diary in self._diaries],
            'conversations': conversations_serializable
        }

        try:
            with open(p, 'w', encoding='utf-8') as f:
                json.dump(notebook_dict, f, indent=4)
        except Exception as ex:
            raise NotebookFileError("Error while attempting to process the notebook file.", ex)

    def load(self, path: str) -> None:
        """
        Populates the current instance of Notebook with data stored in a notebook file.

        Example usage: 

        ```
        notebook = Notebook()
        notebook.load('/path/to/file.json')
        ```

        Raises NotebookFileError, IncorrectNotebookError
        """
        p = Path(path)

        if not (p.exists() and p.suffix == '.json'):
            raise NotebookFileError()

        try:
            with open(p, 'r', encoding='utf-8') as f:
                obj = json.load(f)

            self.username = obj['username']
            self.password = obj['password']
            self.host = obj['host']
            self.port = obj['port']

            self._diaries = [Diary(d['entry'], d['timestamp']) for d in obj.get('_diaries', [])]

            self.conversations = {}
            convs = obj.get('conversations', {})
            for recipient, messages in convs.items():
                conv = Conversation(recipient)
                for m in messages:
                    conv.add_message(m)
                self.conversations[recipient] = conv

        except Exception as ex:
            raise IncorrectNotebookError(ex)

        



