# Real-Time Chat Application

A real-time chat application built using **Python, Socket Programming, Multithreading, and Tkinter**. It allows multiple users to connect to a central server and exchange messages instantly through a graphical user interface.

## Features

- Real-time messaging between multiple clients.
- Client-server communication using TCP sockets.
- Graphical user interface built with Tkinter.
- Multiple users can join the chat using unique usernames.
- Instant message broadcasting to connected clients.
- Notifications when users join or leave the chat.
- Send messages using the **Send button** or **Enter key**.
- Separate server and client programs.
- JSON-based message communication.

## Technologies Used

- **Programming Language:** Python
- **GUI:** Tkinter
- **Networking:** Socket Programming (TCP)
- **Concurrency:** Python Threading
- **Data Format:** JSON

## Project Structure

```text
real-time-chat-application/
│
├── server.py
├── client.py
└── README.md
```

## How It Works

1. The server starts and listens for incoming client connections.
2. A client connects to the server using its IP address and port number.
3. The user enters a username and joins the chat.
4. Users send messages through the graphical interface.
5. Messages are transmitted to the server using TCP sockets.
6. The server broadcasts received messages to all connected clients.
7. Each client displays incoming messages in its chat window.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Bhavika-Vaishnav/real-time-chat-application.git
```

### 2. Navigate to the Project Folder

```bash
cd real-time-chat-application
```

### 3. Start the Server

Open a terminal and run:

```bash
python server.py
```

The server will start listening for client connections.

### 4. Start the Client

Open another terminal and run:

```bash
python client.py
```

To connect multiple users, run the client program in separate terminals or launch multiple client windows.

### 5. Join the Chat

- Enter a username.
- Click the **Join** button.
- Type your message in the message box.
- Click **SEND** or press **Enter** to send it.

## Learning Outcomes

Through this project, I gained practical experience in:

- Python socket programming and TCP communication.
- Client-server architecture.
- Multithreading for handling multiple client connections.
- Developing graphical interfaces using Tkinter.
- Sending and receiving structured JSON messages.
- Handling client connections and disconnections.

## Author

**Bhavika Vaishnav**
