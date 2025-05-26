import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
from typing import Text
from ds_messenger import DirectMessenger
from notebook import Notebook, Diary, Conversation, DirectMessage, NotebookFileError
from pathlib import Path
from time import time


class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = []
        self._select_callback = recipient_selected_callback
        self._draw()

    def node_select(self, event):
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        if len(contact) > 25:
            contact = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

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
        self.entry_editor.tag_configure('entry-right', justify='right',
                                        foreground = 'white', 
                                        background = '#0078D7',
                                        lmargin1 = 50, rmargin = 10, 
                                        spacing1=4, spacing3=4,
                                        wrap = 'word')
        self.entry_editor.tag_configure('entry-left', justify='left',
                                        foreground = 'black', 
                                        background = '#E5E5EA',
                                        lmargin1 = 10, rmargin = 50,
                                        spacing1=4, spacing3=4,
                                        wrap = 'word')
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

        self.path_label = tk.Label(frame, width = 30, text = "Notebook Path")
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
        self.dm = None
        self.notebook = None
        self.recipient = ''
        

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
        self._draw()
        self.configure_server()

    def send_message(self):
        # You must implement this!
        message = self.body.get_text_entry()
        recipient = self.recipient

        if not recipient:
            print("No recipient selected!")
        
        success = self.publish(message)
        if not success:
            print("Message not sent - failed to reach server")
            return
        
        self.body.insert_user_message(message)
        direct_message = DirectMessage(message, self.username, self.recipient, time())

        if recipient in self.notebook.conversations:
            self.notebook.conversations[recipient].add_message(direct_message)
            print(type(self.notebook.conversations[recipient]))
        else:
            conv = Conversation(recipient)
            conv.add_message(direct_message)
            self.notebook.conversations[recipient] = conv
        
        self.notebook.save(self.notebook.path)
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

        if recipient in self.notebook.conversations: 
            conversation = self.notebook.conversations[recipient]
            for message in conversation.get_message():
                print(f"message data {message}")
                print(message['sender'])
                if message['sender'] == self.username:
                    self.body.insert_user_message(message['entry'])
                else:
                    self.body.insert_contact_message(message['entry'])
    
    def configure_server(self):
        ud = NewContactDialog(self.root, "Log In",
                              self.server, self.port, self.username, 
                              self.password, self.path)
        self.server = ud.server
        self.port = ud.port
        self.username = ud.user
        self.password = ud.password
        self.path = ud.path
        # You must implement this!
          
        # You must configure and instantiate your
        # DirectMessenger instance after this line.

        dm_created = False
        try:
            self.dm = DirectMessenger(
                self.server,
                int(self.port),
                self.username,
                self.password)
            dm_created = True
            print("DM created!")
        except Exception as e:
            print(f"Failed to create DM, Error: {e}")

        try:
            self.notebook = Notebook(username = self.username, #once the program is succesful include stuff about checking whether the password is correct or not.
                                password = self.password,
                                host = self.server,
                                port = self.port,
                                path = self.path)
            if self.notebook:
                path = Path(self.path)
                if path.exists():
                    self.notebook.load(self.notebook.path)
                    print('Notebook loaded success!')

                    for contact in self.notebook.conversations.keys():
                        print('does this hit line 296')
                        if contact != "null" and contact.strip() != '':
                            print('contact inserted line 297')
                            self.body.insert_contact(contact)

                elif dm_created:
                    self.notebook.save(self.notebook.path)
                    print('Notebook saved success!')
                else:
                    print('No existing notebook or server!')
                if dm_created and self.dm:
                    try:
                        all_messages = self.dm.retrieve_all()
                        for msg in all_messages:
                            direct_message = DirectMessage(msg.message, msg.sender, self.username, msg.timestamp)
                            if self.notebook.add_unique_message(msg.sender, direct_message):
                                if msg.sender not in self.body._contacts:
                                    self.body.insert_contact(msg.sender)
                        self.notebook.save(self.notebook.path)
                        print('Server sync complete!')
                    except Exception as e:
                        print(f'Server sync failed!')
                else:
                    print('Offline: no server conneciton!')
        except Exception as e:
            print(f'Notebook creation exception: {e}')
            return
        if dm_created:
            self.check_new()


    def create_direct_messenger(self):
        pass
    
    def save_to_notebook(self):
        pass

    def publish(self, message:str) -> bool:
        # You must implement this!

        if self.dm and self.recipient:
            try:
                self.dm.send(message, self.recipient)
                return True
            except:
                print("Failed to send message: {e}")
                return False
        else:
            print("No recipient or message")
            return False

    def check_new(self):
        # You must implement this!
        if self.dm:
            new_messages = self.dm.retrieve_new()
            for msg in new_messages:
                direct_message = DirectMessage(msg.message, msg.sender, self.username,  msg.timestamp)

                if msg.sender in self.notebook.conversations:
                    self.notebook.conversations[msg.sender].add_message(direct_message)
                else:
                    new_convo = Conversation(msg.sender)
                    new_convo.add_message(direct_message)
                    self.notebook.conversations[msg.sender] = new_convo
                    self.body.insert_contact(msg.sender)
                
                if self.recipient == msg.sender:
                    self.body.insert_contact_message(msg.message)
            
            self.notebook.save(self.notebook.path)
        
        self.root.after(1000, self.check_new)
    
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
    id = main.after(1000, app.check_new)
    print(id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()