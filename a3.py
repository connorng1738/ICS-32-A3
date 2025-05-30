"""
Defines the GUI for the messaging system, leveraging the server
and client connection.
"""
import tkinter as tk
from pathlib import Path
from time import time
from tkinter import ttk, simpledialog, messagebox
from ds_messenger import DirectMessenger
from notebook import (DirectMessage,
                      Conversation,
                      Notebook,
                      IncorrectNotebookError,
                      DirectMessageError)


class Body(tk.Frame):
    """
    The Body class represents the main content area of the messaging app UI.

    This frame includes the contact list and the message display area.
    It handles the visual structure and user interactions related to
    selecting contacts and viewing messages.
    """

    def __init__(self, root, recipient_selected_callback=None):
        """
        Initialize the Body frame which contains the contact
        list and message display.

        Arguments:
        root: The parent tkinter widget
        recipient_selected_callback: Callback function to handle
        contact selection
        """
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = []
        self._select_callback = recipient_selected_callback
        self._draw()

    def node_select(self, event):
        """
        Handle selection of a contact from the tree view.
        """
        print(event)
        selection = self.posts_tree.selection()
        if not selection:
            return
        try:
            index = int(selection[0])
            if index < len(self._contacts):
                entry = self._contacts[index]
                if self._select_callback is not None:
                    self._select_callback(entry)
        except (ValueError, IndexError):
            pass

    def clear_contacts(self):
        """
        Clear all contacts from the tree view and internal contact list.
        """
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)

        self._contacts = []

    def clear_messages(self):
        """
        Clear all messages from the message display area.
        """
        self.entry_editor.delete('1.0', tk.END)

    def insert_contact(self, contact: str):
        """
        Add a new contact to the contact list and tree view.

        Arguments:
        contact: The contact name to add
        """
        self._contacts.append(contact)
        contact_id = len(self._contacts) - 1
        self._insert_contact_tree(contact_id, contact)

    def _insert_contact_tree(self, contact_id, contact: str):
        """
        Insert a contact into the tree view widget.

        Arguments:
        contact_id: The index position for the contact
        contact: The contact name to display
        """
        if len(contact) > 25:
            contact = contact[:24] + "..."
        self.posts_tree.insert('', contact_id, contact_id, text=contact)

    def insert_user_message(self, message: str):
        """
        Add a message from the current user to the message display.

        Arguments:
        message: The message text to display
        """
        self.entry_editor.insert(tk.END, message + '\n', 'entry-right')

    def insert_contact_message(self, message: str):
        """
        Add a message from a contact to the message display.

        Arguments:
        message: The message text to display
        """
        self.entry_editor.insert(tk.END, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        """
        Get the current text from the message input field.

        Returns:
        The text content from the message editor
        """
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        """
        Set the text in the message input field.

        Arguments:
        text: The text to set in the message editor
        """
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def get_contacts(self):
        """
        Get the list of contacts.

        Returns:
        List of contact names
        """
        return self._contacts.copy()

    def _draw(self):
        """
        Create and layout all the GUI components for the Body frame.
        """
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
                                        foreground='white',
                                        background='#0078D7',
                                        lmargin1=50, rmargin=10,
                                        spacing1=4, spacing3=4,
                                        wrap='word')
        self.entry_editor.tag_configure('entry-left', justify='left',
                                        foreground='black',
                                        background='#E5E5EA',
                                        lmargin1=10, rmargin=50,
                                        spacing1=4, spacing3=4,
                                        wrap='word')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    """
    The Footer class represents the bottom section of the messaging app UI.

    This frame contains action buttons for sending messages and adding
    new users. It handles user interactions related to composing messages
    and managing contacts.
    """

    def __init__(self, root, send_callback=None, add_user_callback=None):
        """
        Initialize the Footer frame which contains action buttons.

        Arguments:
        root: The parent tkinter widget
        send_callback: Callback function for sending messages
        add_user_callback: Callback function for adding new users
        """
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._add_user_callback = add_user_callback
        self._draw()

    def send_click(self):
        """
        Handle the send button click event.
        """
        if self._send_callback is not None:
            self._send_callback()

    def add_user_click(self):
        """
        Handle the add user button click event.
        """
        if self._add_user_callback is not None:
            self._add_user_callback()

    def _draw(self):
        """
        Create and layout the footer buttons.
        """
        save_button = tk.Button(master=self, text="Send",
                                width=20, command=self.send_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        add_user_button = tk.Button(
            master=self, text="Add User", command=self.add_user_click)
        add_user_button.pack(fill=tk.BOTH, side=tk.LEFT, padx=(125, 5), pady=5)


class NewContactDialog(tk.simpledialog.Dialog):
    """
    The NewContactDialog class represents a pop-up dialog for entering server
    connection details and user credentials.

    This dialog allows the user to input or confirm information such as the
    server address, username, password, and notebook file path before
    connecting to the messaging service.
    """

    def __init__(self,
                 root,
                 title=None,
                 server=None,
                 user: str = None,
                 password=None,
                 path=None):
        """
        Initialize the login dialog for entering server connection details.

        Arguments:
        root: The parent tkinter widget
        title: The dialog window title
        server: Default server address
        user: Default username
        password: Default password
        path: Default notebook file path
        """

        self.root = root
        self.server = server
        self.path = path
        self.user = user
        self.password = password

        super().__init__(root, title)

    def body(self, frame):
        """
        Create the input fields for the login dialog.

        Arguments:
        frame: The frame to add the input fields to
        """
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

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry.insert(tk.END, self.password)
        self.password_entry['show'] = '*'
        self.password_entry.pack()

        self.path_label = tk.Label(frame, width=30, text="Notebook Path")
        self.path_label.pack()
        self.path_entry = tk.Entry(frame, width=30)
        self.path_entry.insert(tk.END, self.path)
        self.path_entry.pack()

    def apply(self):
        """
        Save the entered values when the dialog is accepted.
        """
        self.server = self.server_entry.get()
        self.path = self.path_entry.get()
        self.user = self.username_entry.get()
        self.password = self.password_entry.get()


class MainApp(tk.Frame):
    """
    The MainApp class represents the primary interface
    for the messaging application.

    This class manages the overall layout, user session,
    message sending, contact management, and communication with the server.
    It integrates the Body and Footer UI components and handles interactions
    between the user and the messaging backend.
    """

    def __init__(self, root):
        """
        Initialize the main application window and components.

        Arguments:
        root: The root tkinter window
        """
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = ''
        self.password = ''
        self.server = ''
        self.path = ''
        self.direct_messenger = None
        self.notebook = None
        self.recipient = ''
        self.all_messages = None
        self.body = None
        self.footer = None

        self._draw()
        self.configure_server()

    def clear_gui(self):
        """
        Clear all GUI components when switching user accounts.
        """
        self.body.clear_contacts()
        self.body.clear_messages()
        self.body.set_text_entry("")
        self.recipient = ''

    def send_message(self):
        """
        Send a message to the currently selected recipient.
        """
        message = self.body.get_text_entry()
        recipient = self.recipient

        if not recipient:
            messagebox.showerror("Error", "No recipient selected!")
            return

        success = self.publish(message)
        if not success:
            messagebox.showerror(
                "Error", "Message not sent - failed to reach server")
            return

        self.body.insert_user_message(message)
        direct_message = DirectMessage(
            message, self.username, self.recipient, time())

        if recipient in self.notebook.conversations:
            self.notebook.conversations[recipient].add_message(direct_message)
        else:
            conv = Conversation(recipient)
            conv.add_message(direct_message)
            self.notebook.conversations[recipient] = conv

        self.notebook.save(self.notebook.path)
        self.body.set_text_entry("")

    def add_contact(self):
        """
        Prompt user to add a new contact to their contact list.
        """
        contact = simpledialog.askstring(
            "Add Contact", "Please enter the new contact name:")
        if contact:
            self.body.insert_contact(contact)

    def recipient_selected(self, recipient: str):
        """
        Handle selection of a recipient and load their conversation history.

        Arguments:
        recipient: The selected contact's name
        """
        self.recipient = recipient

        self.body.entry_editor.delete('1.0', tk.END)

        if recipient in self.notebook.conversations:
            conversation = self.notebook.conversations[recipient]
            for message in conversation.get_message():
                if message['sender'] == self.username:
                    self.body.insert_user_message(message['entry'])
                else:
                    self.body.insert_contact_message(message['entry'])

    def configure_server(self):
        """
        Configure server connection and initialize user session.
        """
        self.prompt_login()
        self.clear_gui()
        dm_created = self.create_dm()

        if dm_created:
            self.setup_notebook(dm_created)

        if dm_created:
            self.check_new()

    def prompt_login(self):
        """
        Display login dialog and collect user credentials.
        """
        dialog = NewContactDialog(self.root, "Log In",
                                  self.server, self.username,
                                  self.password, self.path)

        self.server = dialog.server
        self.username = dialog.user
        self.password = dialog.password
        self.path = dialog.path

        self.direct_messenger = None
        self.notebook = None

    def create_dm(self) -> bool:
        """
        Create DirectMessenger connection to the server.

        Returns:
        bool: True if connection successful, False otherwise
        """
        try:
            self.direct_messenger = DirectMessenger(
                self.server,
                self.username,
                self.password)

            self.all_messages = self.direct_messenger.retrieve_all()
            return True
        except DirectMessageError:
            messagebox.showerror("Failed to create DM")
            return False

    def setup_notebook(self, dm_created: bool):
        """
        Initialize notebook and load existing conversations.

        Arguments:
        dm_created: Boolean indicating if
        DirectMessenger was successfully created
        """
        try:
            self.notebook = Notebook(username=self.username,
                                     password=self.password,
                                     host=self.server,
                                     path=self.path)

            if not self.notebook:
                return

            path = Path(self.path)
            if path.suffix == '.json':
                if path.exists():
                    self._load_existing_notebook()
                elif dm_created:
                    self.notebook.save(self.notebook.path)
                else:
                    messagebox.showerror(
                        "Error", "No existing notebook or server!")

                if dm_created and self.direct_messenger:
                    self.sync_server_messages()
                else:
                    messagebox.showerror(
                        "Error", "Offline: no server connection!")

        except IncorrectNotebookError:
            messagebox.showerror("Invalid login. Please try again.")

    def _load_existing_notebook(self):
        """
        Load existing notebook and populate contacts.
        """
        self.notebook.load(self.notebook.path)
        for contact in self.notebook.conversations:
            if contact and contact.strip().lower() != "null":
                self.body.insert_contact(contact)

    def sync_server_messages(self):
        """
        Retrieve and sync all messages from the server.
        """
        try:
            for msg in self.all_messages:
                direct_message = DirectMessage(
                    msg.message, msg.sender, self.username, msg.timestamp)

                if self.notebook.add_unique_message(msg.sender,
                                                    direct_message):
                    current_contacts = self.body.get_contacts()
                    if msg.sender not in current_contacts:
                        self.body.insert_contact(msg.sender)
            self.notebook.save(self.notebook.path)
        except (DirectMessageError, ConnectionError) as error:
            messagebox.showerror(f"Unable to sync messages. Error: {error}")

    def publish(self, message: str) -> bool:
        """
        Send a message to the server.

        Arguments:
        message: The message text to send

        Returns:
        bool: True if message sent successfully, False otherwise
        """
        if not self.direct_messenger and self.recipient:
            return False
        try:
            self.direct_messenger.send(message, self.recipient)
            return True
        except DirectMessageError:
            messagebox.showerror("Unable to publish.")
            return False

    def check_new(self):
        """
        Check for new messages from the server and update the interface.
        """
        if self.direct_messenger:
            new_messages = self.direct_messenger.retrieve_new()
            for msg in new_messages:
                direct_message = DirectMessage(
                    msg.message, msg.sender, self.username, msg.timestamp)

                if msg.sender in self.notebook.conversations:
                    self.notebook.conversations[msg.sender].add_message(
                        direct_message)
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
        """
        Create and layout the main application components and menu system.
        """
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
        self.footer = Footer(
            self.root,
            send_callback=self.send_message,
            add_user_callback=self.add_contact)
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
    after_id = main.after(1000, app.check_new)
    print(after_id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).›
    main.mainloop()
