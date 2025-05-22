import time
from notebook import Notebook, DirectMessage, Conversation

def test_save_and_load():
    # Create notebook and add messages
    nb1 = Notebook('alice', '1234', 'localhost', 8000, 'alice_test.json')

    # Received message from Bob
    dm1 = DirectMessage("Hi Bob!", "alice", "bob", time.time())
    dm2 = DirectMessage("Hey Alice!", "bob", None, time.time()) 
    dm3 = DirectMessage("How is your day Bob!", "alice", "bob", time.time()) 
    
    # Recieved message from Connor
   

    conv = Conversation("bob")
    conv.add_message(dm1)
    conv.add_message(dm2)
    conv.add_message(dm3)

    nb1.conversations["bob"] = conv

   
    dm4 = DirectMessage("Hi connor", "alice", "connor", time.time())
    dm5 = DirectMessage("Hey Alice!", "connor", None, time.time())

    conv = Conversation("connor")
    conv.add_message(dm4)
    conv.add_message(dm5)

    nb1.conversations["connor"] = conv

    nb1.save(nb1.path)
    nb2 = Notebook('', '', '', 0, 'alice_test.json')
    nb2.load(nb2.path)

    # Check if data matches
    # Check username
    # assert nb2.username == 'alice', "Username does not match after loading"

    # # Check conversations keys
    # assert "bob" in nb2.conversations, "Conversation with 'bob' missing after loading"

    # # Check messages count
    # loaded_messages = nb2.conversations["bob"].get_message()
    # # assert len(loaded_messages) == 2, f"Expected 2 messages, got {len(loaded_messages)}"

    # # Check message content and fields
    # assert loaded_messages[0].entry == "Hi Bob!", "First message content mismatch"
    # assert loaded_messages[0].sender == "alice", "First message sender mismatch"
    # assert loaded_messages[0].recipient == "bob", "First message recipient mismatch"

    # assert loaded_messages[1].entry == "Hey Alice!", "Second message content mismatch"
    # assert loaded_messages[1].sender == "bob", "Second message sender mismatch"

    # print("All tests passed!")

if __name__ == "__main__":
    test_save_and_load()
