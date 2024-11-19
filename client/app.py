import tkinter as tk
from auth import AuthWindow
from chat_logic import ChatApp

def start_app():
    root = tk.Tk()
    def on_login(user):
        root.destroy()
        chat_root = tk.Tk()
        ChatApp(chat_root, user)
        chat_root.mainloop()

    AuthWindow(root, on_login)
    root.mainloop()

if __name__ == "__main__":
    start_app()
