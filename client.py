
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
import json

HOST = "127.0.0.1"
PORT = 1234

DARK_GREY = "#121212"
MEDIUM_GREY = "#1F1B24"
OCEAN_BLUE = "#464EB8"
WHITE = "white"

FONT = ("Helvetica", 15)
BUTTON_FONT = ("Helvetica", 13, "bold")
SMALL_FONT = ("Helvetica", 12)

client = None
connected = False
username = ""
send_lock = threading.Lock()


def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + "\n")
    message_box.see(tk.END)
    message_box.config(state=tk.DISABLED)


def send_data(data):
    global client

    try:
        encoded_data = (json.dumps(data) + "\n").encode("utf-8")

        with send_lock:
            client.sendall(encoded_data)

        return True

    except (OSError, ConnectionError, AttributeError):
        return False


def connect():
    global client, connected, username

    if connected:
        return

    username = username_textbox.get().strip()

    if not username:
        messagebox.showerror(
            "Invalid Username",
            "Please enter a username."
        )
        return

    try:
        new_client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        new_client.settimeout(5)
        new_client.connect((HOST, PORT))
        new_client.settimeout(None)

        client = new_client

        join_data = {
            "type": "join",
            "username": username
        }

        if not send_data(join_data):
            raise ConnectionError("Unable to send username.")

        connected = True

        username_textbox.config(state=tk.DISABLED)
        username_button.config(state=tk.DISABLED)
        message_button.config(state=tk.NORMAL)

        add_message("[CLIENT] Successfully connected to server.")

        threading.Thread(
            target=listen_for_messages,
            daemon=True
        ).start()

        message_textbox.focus_set()

    except (OSError, ConnectionError) as error:
        connected = False

        if client:
            client.close()
            client = None

        messagebox.showerror(
            "Connection Error",
            f"Unable to connect:\n{error}\n\n"
            "Make sure server.py is running."
        )


def listen_for_messages():
    global connected

    current_client = client

    try:
        reader = current_client.makefile(
            "r",
            encoding="utf-8"
        )

        for line in reader:
            if not line:
                break

            data = json.loads(line)
            message_type = data.get("type")

            if message_type == "system":
                display = f"[SERVER] {data.get('message', '')}"

            elif message_type == "chat":
                display = (
                    f"[{data.get('username', 'Unknown')}] "
                    f"{data.get('message', '')}"
                )

            elif message_type == "error":
                display = f"[ERROR] {data.get('message', '')}"

            else:
                continue

            root.after(0, add_message, display)

    except (OSError, ConnectionError, json.JSONDecodeError):
        pass

    finally:
        if current_client is client:
            connected = False
            root.after(0, connection_closed)


def connection_closed():
    if root.winfo_exists():
        username_textbox.config(state=tk.NORMAL)
        username_button.config(state=tk.NORMAL)
        message_button.config(state=tk.DISABLED)

        add_message("[SERVER] Connection closed.")


def send_message(event=None):
    message = message_textbox.get().strip()

    if not connected:
        messagebox.showerror(
            "Not Connected",
            "Please join the chat first."
        )
        return "break"

    if not message:
        return "break"

    success = send_data({
        "type": "message",
        "message": message
    })

    if success:
        message_textbox.delete(0, tk.END)
    else:
        messagebox.showerror(
            "Send Error",
            "Unable to send message. Check your connection."
        )

    return "break"


def close_application():
    global connected, client

    connected = False

    if client:
        try:
            client.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

        client.close()
        client = None

    root.destroy()


# ---------------- GUI SETUP ----------------

root = tk.Tk()
root.geometry("750x500")
root.title("Real-Time Chat Application")
root.resizable(False, False)
root.configure(bg=DARK_GREY)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=5)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

# Top frame
top_frame = tk.Frame(root, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky="nsew")

username_label = tk.Label(
    top_frame,
    text="Enter username:",
    font=FONT,
    bg=DARK_GREY,
    fg=WHITE
)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(
    top_frame,
    font=FONT,
    bg=MEDIUM_GREY,
    fg=WHITE,
    width=22
)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(
    top_frame,
    text="Join",
    font=BUTTON_FONT,
    bg=OCEAN_BLUE,
    fg=WHITE,
    command=connect
)
username_button.pack(side=tk.LEFT, padx=10)

# Middle frame
middle_frame = tk.Frame(root, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky="nsew")

message_box = scrolledtext.ScrolledText(
    middle_frame,
    font=SMALL_FONT,
    bg=MEDIUM_GREY,
    fg=WHITE,
    width=85,
    height=22,
    state=tk.DISABLED
)
message_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Bottom frame
bottom_frame = tk.Frame(root, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky="nsew")

message_textbox = tk.Entry(
    bottom_frame,
    font=FONT,
    bg=MEDIUM_GREY,
    fg=WHITE,
    width=48
)
message_textbox.pack(
    side=tk.LEFT,
    padx=10,
    pady=15,
    fill=tk.X,
    expand=True
)

# Press Enter to send
message_textbox.bind("<Return>", send_message)

# Visible Send button
message_button = tk.Button(
    bottom_frame,
    text="SEND",
    font=BUTTON_FONT,
    bg=OCEAN_BLUE,
    fg=WHITE,
    activebackground="#626BD6",
    activeforeground=WHITE,
    command=send_message,
    state=tk.DISABLED,
    width=9
)
message_button.pack(
    side=tk.RIGHT,
    padx=12,
    pady=15
)

root.protocol("WM_DELETE_WINDOW", close_application)

if __name__ == "__main__":
    root.mainloop()