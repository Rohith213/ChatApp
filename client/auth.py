import tkinter as tk
from tkinter import messagebox
from utils.helper import hash_password, authenticate_user, register_user

class AuthWindow:
    def __init__(self, root, on_login):
        self.root = root
        self.on_login = on_login
        self.mode = "login"

        tk.Label(root, text="Chat App Login", font=("Arial", 14)).pack(pady=10)
        tk.Label(root, text="Username:").pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)

        tk.Label(root, text="Password:").pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        self.submit_button = tk.Button(root, text="Login", command=self.handle_submit)
        self.submit_button.pack(pady=10)

        self.toggle_button = tk.Button(root, text="Sign Up", command=self.toggle_mode)
        self.toggle_button.pack()

    def toggle_mode(self):
        self.mode = "signup" if self.mode == "login" else "login"
        self.submit_button.config(text="Sign Up" if self.mode == "signup" else "Login")
        self.toggle_button.config(text="Login" if self.mode == "signup" else "Sign Up")

    def handle_submit(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if self.mode == "login":
            user = authenticate_user(username, password)
            if user:
                self.on_login(user)
            else:
                messagebox.showerror("Error", "Invalid credentials")
        else:
            if register_user(username, password):
                messagebox.showinfo("Success", "Account created successfully!")
                self.toggle_mode()
            else:
                messagebox.showerror("Error", "Username already exists")
