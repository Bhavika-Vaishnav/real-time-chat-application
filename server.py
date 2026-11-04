
import socket
import threading
import json

HOST = "127.0.0.1"
PORT = 1234
LISTENER_LIMIT = 10

active_clients = {}
clients_lock = threading.Lock()


def send_message(client, data):
    try:
        message = json.dumps(data) + "\n"
        client.sendall(message.encode("utf-8"))
        return True
    except (OSError, ConnectionError):
        return False


def broadcast(data):
    with clients_lock:
        clients = list(active_clients.keys())

    disconnected = []

    for client in clients:
        if not send_message(client, data):
            disconnected.append(client)

    for client in disconnected:
        remove_client(client)


def remove_client(client):
    with clients_lock:
        username = active_clients.pop(client, None)

    try:
        client.close()
    except OSError:
        pass

    if username:
        print(f"{username} disconnected.")

        broadcast({
            "type": "system",
            "message": f"{username} left the chat."
        })


def client_handler(client, address):
    username = None

    try:
        reader = client.makefile("r", encoding="utf-8")

        join_data = reader.readline()

        if not join_data:
            return

        data = json.loads(join_data)

        if data.get("type") != "join":
            return

        username = data.get("username", "").strip()

        if not username:
            send_message(client, {
                "type": "error",
                "message": "Username cannot be empty."
            })
            return

        with clients_lock:
            active_clients[client] = username

        print(f"{username} joined from {address}")

        broadcast({
            "type": "system",
            "message": f"{username} joined the chat."
        })

        for line in reader:
            if not line:
                break

            data = json.loads(line)

            if data.get("type") == "message":
                message = data.get("message", "").strip()

                if message:
                    print(f"{username}: {message}")

                    broadcast({
                        "type": "chat",
                        "username": username,
                        "message": message
                    })

    except (OSError, ConnectionError, json.JSONDecodeError) as error:
        print(f"Client error: {error}")

    finally:
        remove_client(client)


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((HOST, PORT))
        server.listen(LISTENER_LIMIT)

        print(f"Server running on {HOST}:{PORT}")
        print("Waiting for clients to connect...")

        while True:
            client, address = server.accept()

            print(f"New connection: {address}")

            thread = threading.Thread(
                target=client_handler,
                args=(client, address),
                daemon=True
            )
            thread.start()

    except OSError as error:
        print(f"Server error: {error}")

    finally:
        server.close()


if __name__ == "__main__":
    main()