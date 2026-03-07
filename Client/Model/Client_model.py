import socket
import json


class ClientModel:
    def __init__(self, host="127.0.0.1", port=4000):
        self.host = host
        self.port = port

        self.current_login = None


    def send_form(self, action, login, password, name=""):

        form = {"action": action,"login": login,"password": password,"name": name}
        data = json.dumps(form, ensure_ascii=False).encode("utf-8")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.host, self.port))
            s.sendall(data)

            resp = s.recv(1024).decode("utf-8", errors="replace")
            return resp.strip()
        finally:
            try:
                s.close()
            except:
                pass

    def send_file(self, login, path):

        import os

        if not os.path.exists(path):
            return "ERROR FILE NOT FOUND"

        if not os.path.isfile(path):
            return "ERROR NOT A FILE"

        filename = os.path.basename(path)
        name, ext = os.path.splitext(filename)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.connect((self.host, self.port))

            s.sendall("UPLOAD\n".encode())
            s.sendall((login + "\n").encode())
            s.sendall((name + "\n").encode())
            s.sendall((ext + "\n").encode())

            with open(path, "rb") as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    s.sendall(data)

            s.shutdown(socket.SHUT_WR)

            resp = s.recv(1024).decode("utf-8", errors="replace")
            return resp.strip()

        except Exception as e:
            return f"ERROR {e}"

        finally:
            try:
                s.close()
            except:
                pass