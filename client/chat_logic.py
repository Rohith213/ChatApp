import tkinter as tk
from utils.file_transfer import FileTransfer
from utils.socket_client import SocketClient

class ChatApp:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.sock = SocketClient(user)

        self.chat_display = tk.Text(root, state="disabled", width=50, height=20)
        self.chat_display.pack(pady=10)

        self.message_entry = tk.Entry(root, width=40)
        self.message_entry.pack(side=tk.LEFT, padx=10)

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT)

        self.file_button = tk.Button(root, text="Send File", command=self.send_file)
        self.file_button.pack(side=tk.LEFT)

        self.file_transfer = FileTransfer(self.sock, user)
        self.sock.start_listening(self.display_message)

    def send_message(self):
        message = self.message_entry.get().strip()
        if message:
            self.message_entry.delete(0, tk.END)
            self.sock.send_message(message)

    def send_file(self):
        self.file_transfer.send_file()

    def display_message(self, message):
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.config(state="disabled")
