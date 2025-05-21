import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
from typing import Text
from ds_messenger import DirectMessenger


class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback=None):
    # Initializes the Body frame, sets up contacts list, and draws UI elements.
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    def node_select(self, event):
    # Called when a contact is selected; notifies the callback with selected contact.
            index = int(self.posts_tree.selection()[0])
            entry = self._contacts[index]
            if self._select_callback is not None:
                self._select_callback(entry)

    def insert_contact(self, contact: str):
    # Adds a new contact to the contact list and GUI tree view.
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
    # Inserts contact into the tree widget (truncate if name is long).

        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message:str):
    # Adds the user’s own message to the top of the display, right-aligned.
        self.entry_editor.insert(1.0, message + '\n', 'entry-right')

    def insert_contact_message(self, message:str):
    # Adds a received message to the top of the display, left-aligned.
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
    # Retrieves the current message typed by the user.
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text:str):
    # Replaces the current text in the input area with the provided text.

        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
    # Constructs and arranges the UI components inside the Body frame.
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
# Initializes Footer frame and sets up the send callback.
    def __init__(self, root, send_callback=None, add_user_callback = None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._add_user_callback = add_user_callback
        self._draw()

    def send_click(self):
    # Triggered when the Send button is clicked.
        if self._send_callback is not None:
            self._send_callback()
    
    def add_user_click(self):
        if self._add_user_callback is not None:
            self._add_user_callback()

    def _draw(self):
    # Creates and places the Send button and status label. #also added add_user button
        save_button = tk.Button(master=self, text="Send", width=5, height = 2, command = self.send_click)
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        add_user_button = tk.Button(master = self, text = "Add User", command = self.add_user_click) 
        add_user_button.pack(fill = tk.BOTH, side = tk.LEFT, padx=(125, 5), pady = 5) #what should this button do?


class NewContactDialog(tk.simpledialog.Dialog):
# Dialog to collect server, username, and password from the user.
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
    # Creates input fields for server address and username (and TODO for password).
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        # You need to implement also the region for the user to enter
        # the Password. The code is similar to the Username you see above
        # but you will want to add self.password_entry['show'] = '*'
        # such that when the user types, the only thing that appears are
        # * symbols.
        #self.password...


    def apply(self):
    # Retrieves the user's inputs when they click OK.
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
# Sets up the main app logic, contact list, and GUI components.

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.messages_by_contact = {}
        self.username = ''
        self.password = ''
        self.server = '127.0.0.1'
        self.recipient = ''
        # You must implement this! You must configure and
        # instantiate your DirectMessenger instance after this line.
        #self.direct_messenger = ... continue!
        #self.dm = DirectMessenger(self.server, self.username, self.password)
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the root frame
        self._draw()
        self.body.insert_contact("studentexw23") # adding one example student.

    def send_message(self):
    # Called when the user hits send
    # You must implement this!
        message = self.body.get_text_entry()
        recipient = self.recipient

        if not recipient:
            print("Error: No recipient selected.")
            return

        if not message.strip():
            return
        self.body.insert_user_message(f"You: {message}")
        self.body.set_text_entry("")

        # Store the sent message locally
        if recipient not in self.messages_by_contact:
            self.messages_by_contact[recipient] = []
        self.messages_by_contact[recipient].append(f"You: {message}")

        try:
            response = self.dm.send(recipient, message)
            print("Message sent:", response)
        except Exception as e:
            print(f"Send failed: {e}")

    def add_contact(self):
    # Prompts user to add a new contact (needs implementation).
        # You must implement this!
        # Hint: check how to use tk.simpledialog.askstring to retrieve
        # the name of the new contact, and then use one of the body
        # methods to add the contact to your contact list
        contact = simpledialog.askstring("Add Contact", "Please enter the new contact name:")
        if contact:
            self.body.insert_contact(contact)

    def recipient_selected(self, recipient):
    # Stores the selected recipient from the contact list.
        self.recipient = recipient
        self.body.entry_editor.delete('1.0', tk.END)
        if recipient in self.messages_by_contact:
            for msg in self.messages_by_contact[recipient]:
                self.body.insert_contact_message(msg)

    def configure_server(self):
    # Opens the configuration dialog to set server, username, and password.
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        # You must implement this!
        # You must configure and instantiate your
        # DirectMessenger instance after this line.
        if self.username and self.password and self.server:
            self.dm  = DirectMessenger(dsuserver = self.server, username = self.username, password = self.password)

    def publish(self, message:str):
    # Publishes a message to the server (to be implemented).
        # You must implement this!
        pass

    def check_new(self):
        if self.dm:
            try:
                new_messages = self.dm.retrieve_new()
                for msg in new_messages:
                    sender = msg['from']
                    message = msg['message']
                    if sender not in self.messages_by_contact:
                        self.messages_by_contact[sender] = []
                        self.body.insert_contact(sender)
                    self.messages_by_contact[sender].append(message)
                    if self.recipient == sender:
                        self.body.insert_contact_message(message, sender)
            except Exception as e:
                print(f"Check new errors: {e}")
    # Checks for new incoming messages (to be implemented).
        # You must implement this!

    def _draw(self):
    # Builds the full GUI layout including menu, Body, and Footer.


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
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message, add_user_callback = self.add_contact)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
# Starts the application window and initializes MainApp.
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
