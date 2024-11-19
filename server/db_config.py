import pymongo
from datetime import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["ChatApp"]
messages_collection = db["messages"]

def log_message(message):
    """Logs a chat message to the database."""
    message["timestamp"] = datetime.now()
    messages_collection.insert_one(message)
    print(f"Message logged: {message}")

def broadcast_message(message):
    print(f"Broadcasting: {message}")
