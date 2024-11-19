import os
import tkinter as tk
from tkinter import filedialog, messagebox
import json

class FileTransfer:
    def __init__(self, socket_client, user):
        """
        Handles file transfers for the chat application.

        :param socket_client: The active socket client connection
        :param user: The authenticated user's data
        """
        self.socket_client = socket_client
        self.user = user

    def send_file(self):
        """
        Allow the user to select a file and send it over the socket connection.
        """
        file_path = filedialog.askopenfilename(title="Select a File to Send")
        if not file_path:
            return  # User canceled file selection

        try:
            # Read the file contents
            file_name = os.path.basename(file_path)
            with open(file_path, "rb") as file:
                file_data = file.read()

            # Create a JSON object to include file metadata and data
            file_message = {
                "type": "file",
                "group_id": "example_group",
                "sender": self.user["username"],
                "file_name": file_name,
                "file_data": file_data.hex()  # Convert binary data to hex for transport
            }

            # Send the file over the socket
            self.socket_client.send_raw(json.dumps(file_message))
            messagebox.showinfo("Success", f"File '{file_name}' sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send file: {str(e)}")

    def receive_file(self, file_message):
        """
        Save a received file to the user's local system.

        :param file_message: The JSON message containing the file details
        """
        try:
            file_name = file_message["file_name"]
            file_data = bytes.fromhex(file_message["file_data"])  # Convert hex back to binary

            # Prompt user for save location
            save_path = filedialog.asksaveasfilename(initialfile=file_name, title="Save File As")
            if not save_path:
                return  # User canceled save

            # Save the file
            with open(save_path, "wb") as file:
                file.write(file_data)

            messagebox.showinfo("Success", f"File saved as '{save_path}'")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
