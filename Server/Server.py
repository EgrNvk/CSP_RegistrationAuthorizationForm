import socket
import threading
import json
import os
import hashlib


class Server:

    def __init__(self, host="127.0.0.1", port=4000):
        self.host = host
        self.port = port
        self.users_file = "users.json"
        self.lock = threading.Lock()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def load_users(self):
        if not os.path.exists(self.users_file):
            return {}

        with open(self.users_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_users(self, users):
        with open(self.users_file, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)

    def client_service(self, conn, addr):

        print("Connected:", addr)

        try:
            data = conn.recv(1024).decode()
            form = json.loads(data)

            action = form["action"]
            login = form["login"]
            password = form["password"]
            name = form.get("name", "")

            with self.lock:

                users = self.load_users()

                if action == "register":

                    if login in users:
                        conn.send("ERROR USER EXISTS".encode())

                    else:
                        users[login] = {
                            "password": self.hash_password(password),
                            "name": name
                        }

                        self.save_users(users)

                        conn.send("OK REGISTER".encode())

                elif action == "login":

                    if login not in users:
                        conn.send("ERROR USER NOT FOUND".encode())

                    elif users[login]["password"] != self.hash_password(password):
                        conn.send("ERROR WRONG PASSWORD".encode())

                    else:
                        conn.send("OK LOGIN".encode())

        except Exception as e:
            print("Error:", e)

        conn.close()
        print("Disconnected:", addr)

    def start(self):

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server.bind((self.host, self.port))
        server.listen()

        print("Server started")

        while True:

            conn, addr = server.accept()

            thread = threading.Thread(
                target=self.client_service,
                args=(conn, addr)
            )

            thread.start()

Server().start()