import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
from typing import Text
from ds_messenger import DirectMessenger, DirectMessage
from pathlib import Path
from time import time
import json


class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = []
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    def node_select(self, event):
        selected_items = self.posts_tree.selection()
        if not selected_items:
            return
        selected_id = selected_items[0]  

        entry = self.posts_tree.item(selected_id)["text"]
        if self._select_callback is not None:
            self._select_callback(entry)


    def insert_contact(self, contact: str):
        if not contact:
            print("Skipping empty contact")
            return
        if contact in self._contacts:
            print(f"Contact {contact} already exists")
            return
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        display_name = contact
        if len(contact) > 25:
            display_name = contact[:24] + "..."
        self.posts_tree.insert('', 'end', iid=contact, text=display_name)


    def insert_user_message(self, message:str):
        self.entry_editor.insert(tk.END, message + '\n', 'entry-right')

    def insert_contact_message(self, message:str):
        self.entry_editor.insert(tk.END, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text:str):
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)

class Footer(tk.Frame):
    def __init__(self, root, send_callback=None, add_user_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._add_user_callback = add_user_callback
        self._draw()

    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def add_user_click(self):
        if self._add_user_callback is not None:
            self._add_user_callback()

    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=20, command = self.send_click)
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)


        add_user_button = tk.Button(master = self, text = "Add User", command = self.add_user_click) 
        add_user_button.pack(fill = tk.BOTH, side = tk.LEFT, padx=(125, 5), pady = 5)


class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, server = None, port = 3001, user = None, password = None, path = None):
                 
        self.root = root
        self.server = server
        self.port = port
        self.path = path
        self.user = user
        self.password = password
    
        super().__init__(root, title)

    def body(self, frame):

        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.port_label = tk.Label(frame, width=30, text="Port")
        self.port_label.pack()
        self.port_entry = tk.Entry(frame, width=30)
        self.port_entry.insert(tk.END, str(self.port))
        self.port_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width = 30, text = "Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width = 30)
        self.password_entry.insert(tk.END, self.password)
        self.password_entry['show'] = '*'
        self.password_entry.pack()

        self.path_label = tk.Label(frame, width = 30, text = "Path")
        self.path_label.pack()
        self.path_entry = tk.Entry(frame, width = 30)
        self.path_entry.insert(tk.END, self.path)
        self.path_entry.pack()

    def apply(self):
        self.server = self.server_entry.get()
        self.port = self.port_entry.get()
        self.path = self.path_entry.get()
        self.user = self.username_entry.get()
        self.password = self.password_entry.get()

class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = ''
        self.password = ''
        self.server = ''
        self.port = ''
        self.path = ''
        self.recipient = ''
        self.local = None
        self.messages = []
        self._draw()
        self.configure_server()
        # self.dm = None
        # if self.dm:
        #     self.dm = DirectMessenger(self.server, self.port, self.username, self.password)
        #     print(self.dm)

        # if self.dm:
        #     self.dm = DirectMessenger(self.server, self.port, self.username, self.password)
        #     print('Directmessenger succesfully created!')
        # else:
        #     print('DirectMessenger does not exist!')
        # You must implement this! You must configure and
        # instantiate your DirectMessenger instance after this line.
        #self.direct_messenger = ... continue!

        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the root frame

    def send_message(self):
        # You must implement this!
        message = self.body.get_text_entry()
        recipient = self.recipient
        if not recipient:
            print("No recipient selected!")
            return

        self.publish(message)
        self.body.insert_user_message(message) #edit this
        self.body.set_text_entry("")

    def add_contact(self):
        # You must implement this!
        # Hint: check how to use tk.simpledialog.askstring to retrieve
        # the name of the new contact, and then use one of the body
        # methods to add the contact to your contact list
        contact = simpledialog.askstring("Add Contact", "Please enter the new contact name:")
        if contact:
            self.body.insert_contact(contact)


    def recipient_selected(self, recipient):
        self.recipient = recipient

        self.body.entry_editor.delete('1.0', tk.END)
    

    def configure_server(self):
        ud = NewContactDialog(self.root, "Log In",
                              self.server, self.port, self.username, 
                              self.password, self.path)
        self.server = ud.server
        self.port = ud.port
        self.username = ud.user
        self.password = ud.password
        self.path = ud.path

        print(self.username, self.password, self.server, self.port, self.path)
        # You must implement this!
          
        # You must configure and instantiate your
        # DirectMessenger instance after this line.
        try:
            self.dm = DirectMessenger(
                self.server,
                int(self.port),
                self.username,
                self.password)
            print("DM created!")

        except Exception as e:
            print(f"Failed to create DM, Error: {e}")
        
        path = Path(self.path)
        
        if not path.exists():
            self.save(path)
        else:
            self.load(path)

    def save(self, path: Path) -> None:
        path = Path(path)

        if path.suffix != '.json':
            print("Ivalid file type - must be JSON")
            return
        
        self.local = {
            self.username: {
                'password': self.password,
                'messages': self.messages
            }
        }
        with open(path, 'w', encoding = 'utf-8') as f:
            json.dump(self.local, f)
    
    def load(self, path: Path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            user_data = data.get(self.username, None)
            if user_data:
                self.password = user_data.get('password', '')
                self.messages = user_data.get('messages', [])

                # Update your UI or state here accordingly, e.g.,
                # show posts, update bio text, etc.

                # If you want, you can load messages into your chat display:
                for msg in self.messages:
                    # Insert messages into the chat display (e.g., self.body.insert_contact_message)
                    self.body.insert_contact_message(msg)
            else:
                print(f"No data found for user {self.username}")

        except Exception as e:
            print(f"Failed to load data: {e}")

    def create_direct_messenger(self):
        pass

    def publish(self, message:str) -> bool:
        # You must implement this!
        if self.dm and self.recipient:
            self.dm.send(message, self.recipient)
            
            msg_obj = {
            "sender": self.username,
            "recipient": self.recipient,
            "message": message,
            "timestamp": time()
        }

            self.messages.append(msg_obj)
            return True
        else:
            print("No recipient or message")
            return False

    def check_new(self):
        # You must implement this!
        if self.dm:
            new_messages = self.dm.retrieve_new()
            for msg in new_messages:
                display_text = f"{msg.sender}: {msg.message}"
                self.body.insert_contact_message(display_text)
    
    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New')
        menu_file.add_command(label='Open...')
        menu_file.add_command(label='Close')

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Log In',
                                  command=self.configure_server)
        
        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message, add_user_callback = self.add_contact)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    id = main.after(2000, app.check_new)
    print(id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()
