import socket
import threading
import json
from db_config import log_message, broadcast_message, get_user_by_username

clients = {}  # Store clients by group or user

def handle_client(client_socket, address):
    """Handles the communication for each connected client"""
    print(f"New connection from {address}")
    username = None
    try:
        # Receive username on initial connection
        username = client_socket.recv(1024).decode()
        if username not in clients:
            clients[username] = client_socket

        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            message = json.loads(data)

            # Log the message into MongoDB
            log_message(message)

            recipient = message.get("recipient")  # This could be a user or a group

            # Broadcast to the recipient (user or group)
            if recipient in clients:
                recipient_socket = clients[recipient]
                recipient_socket.sendall(json.dumps(message).encode())
            else:
                print(f"Recipient {recipient} not found")
    except Exception as e:
        print(f"Error with {address}: {e}")
    finally:
        if username:
            del clients[username]
        client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 12345))
    server.listen(5)
    print("Server started on port 12345")

    while True:
        client_socket, address = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, address), daemon=True).start()

if __name__ == "__main__":
    main()
