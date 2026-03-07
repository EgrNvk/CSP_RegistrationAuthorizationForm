import socket
import json


class ClientModel:
    def __init__(self, host="127.0.0.1", port=4000):
        self.host = host
        self.port = port

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