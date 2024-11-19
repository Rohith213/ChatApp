import hashlib
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["ChatApp"]
users_collection = db["users"]

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    return users_collection.find_one({"username": username, "password": hash_password(password)})

def register_user(username, password):
    if users_collection.find_one({"username": username}):
        return False
    users_collection.insert_one({"username": username, "password": hash_password(password)})
    return True
