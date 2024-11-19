import socket
import threading
import json

class SocketClient:
    def __init__(self, user):
        self.user = user
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("localhost", 12345))

    def send_message(self, message):
        data = json.dumps({"group_id": "example_group", "sender": self.user["username"], "message": message})
        self.sock.sendall(data.encode())

    def start_listening(self, callback):
        def listen():
            while True:
                try:
                    data = self.sock.recv(1024).decode()
                    if data:
                        callback(json.loads(data)['message'])
                except Exception as e:
                    print(f"Error: {e}")
                    break

        threading.Thread(target=listen, daemon=True).start()

    def send_raw(self, data):
#     """
#     Send raw data over the socket connection.

#   :param data: JSON string or plain text to send
#     """
        self.sock.sendall(data.encode())
