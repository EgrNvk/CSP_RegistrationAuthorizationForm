import tkinter as tk


class ClientView:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Client")
        self.root.geometry("300x300")

        self.start_frame = tk.Frame(self.root)
        self.start_frame.pack(padx=10, pady=10)

        tk.Label(self.start_frame, text="Choose action").pack(pady=5)

        self.btn_choose_login = tk.Button(self.start_frame, text="Login")
        self.btn_choose_login.pack(pady=5)

        self.btn_choose_register = tk.Button(self.start_frame, text="Register")
        self.btn_choose_register.pack(pady=5)

        self.btn_choose_back = tk.Button(self.start_frame, text="Back")
        self.btn_choose_back.pack(pady=5)

        self.login_frame = tk.Frame(self.root)

        tk.Label(self.login_frame, text="Login").grid(row=0, column=0)
        self.login_entry = tk.Entry(self.login_frame)
        self.login_entry.grid(row=0, column=1)

        tk.Label(self.login_frame, text="Password").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.btn_login = tk.Button(self.login_frame, text="Login")
        self.btn_login.grid(row=2, column=0, columnspan=2, pady=5)

        self.register_frame = tk.Frame(self.root)

        tk.Label(self.register_frame, text="ПІБ").grid(row=0, column=0)
        self.reg_name = tk.Entry(self.register_frame)
        self.reg_name.grid(row=0, column=1)

        tk.Label(self.register_frame, text="Login").grid(row=1, column=0)
        self.reg_login = tk.Entry(self.register_frame)
        self.reg_login.grid(row=1, column=1)

        tk.Label(self.register_frame, text="Password").grid(row=2, column=0)
        self.reg_password = tk.Entry(self.register_frame, show="*")
        self.reg_password.grid(row=2, column=1)

        self.btn_register = tk.Button(self.register_frame, text="Register")
        self.btn_register.grid(row=3, column=0, columnspan=2, pady=5)

        self.label_response = tk.Label(self.root, text="", fg="blue")
        self.label_response.pack(pady=5)


    def get_login(self):
        return self.login_entry.get()

    def get_password(self):
        return self.password_entry.get()

    def get_reg_login(self):
        return self.reg_login.get()

    def get_reg_password(self):
        return self.reg_password.get()

    def get_reg_name(self):
        return self.reg_name.get()


    def set_response(self, text):
        self.label_response.config(text=text)

    def show_login(self):
        self.start_frame.pack_forget()
        self.register_frame.pack_forget()
        self.login_frame.pack(padx=10, pady=10)

    def show_register(self):
        self.start_frame.pack_forget()
        self.login_frame.pack_forget()
        self.register_frame.pack(padx=10, pady=10)

    def start(self):
        self.root.mainloop()