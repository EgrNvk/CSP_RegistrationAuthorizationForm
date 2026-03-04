import socket
import threading
import json
import os
import hashlib


class Server:
    def init(self, host="127.0.0.1", port=4000):
        self.host = host
        self.port = port
        self.users_file = "users.json"
        self.lock = threading.Lock()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def load_users(self):
        if not os.path.exists(self.users_file):
            return {}

        with open(self.users_file, "r") as f:
            return json.load(f)

    def save_users(self, users):
        with open(self.users_file, "w") as f:
            json.dump(users, f)

    def client_service(self, conn, addr):
        print("Connected:", addr)
        try:
            data = conn.recv(1024).decode()
            form = json.loads(data)

            action = form["action"]
            login = form["login"]
            password = form["password"]

            with self.lock:
                users = self.load_users()

                if action == "register":
                    if login in users:
                        conn.send("ERROR USER EXISTS".encode())
                    else:
                        users[login] = self.hash_password(password)
                        self.save_users(users)
                        conn.send("OK REGISTER".encode())

                elif action == "login":
                    if login not in users:
                        conn.send("ERROR USER NOT FOUND".encode())
                    elif users[login] != self.hash_password(password):
                        conn.send("ERROR WRONG PASSWORD".encode())
                    else:
                        conn.send("OK LOGIN".encode())
        except:
            pass
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