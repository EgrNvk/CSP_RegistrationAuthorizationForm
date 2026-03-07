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

        self.images_dir = "images"

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
            first = conn.recv(1)

            if not first:
                conn.close()
                return

            if first == b"{":
                data = first + conn.recv(1023)
                form = json.loads(data.decode("utf-8"))

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
                                "name": name,
                                "image": ""
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

            else:
                command = first.decode("utf-8") + self.recv_line(conn)

                if command == "UPLOAD":
                    login = self.recv_line(conn)
                    name = self.recv_line(conn)
                    ext = self.recv_line(conn)

                    os.makedirs(self.images_dir, exist_ok=True)

                    filename = f"{login}_{name}{ext}"
                    filepath = os.path.join(self.images_dir, filename)

                    with open(filepath, "wb") as f:
                        while True:
                            data = conn.recv(1024)
                            if not data:
                                break
                            f.write(data)

                    with self.lock:
                        users = self.load_users()

                        if login in users:
                            users[login]["image"] = filename
                            self.save_users(users)
                            conn.send("OK FILE UPLOADED".encode())
                        else:
                            conn.send("ERROR USER NOT FOUND".encode())

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

    def recv_line(self, conn):
        data = b""
        while True:
            b = conn.recv(1)
            if not b:
                break
            if b == b"\n":
                break
            data += b
        return data.decode("utf-8", errors="replace")

Server().start()