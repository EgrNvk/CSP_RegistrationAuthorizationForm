class ClientController:

    def __init__(self, view, model):

        self.view = view
        self.model = model

        self.view.btn_choose_login.config(command=self.view.show_login)
        self.view.btn_choose_register.config(command=self.view.show_register)

        self.view.btn_login.config(command=self.login)
        self.view.btn_register.config(command=self.register)
        self.view.btn_back_login.config(command=self.back)
        self.view.btn_back_register.config(command=self.back)


        self.view.btn_back_upload.config(command=self.back)
        self.view.btn_upload.config(command=self.upload)

    def login(self):

        login = self.view.get_login()
        password = self.view.get_password()

        response = self.model.send_form("login", login, password)

        if response == "OK LOGIN":
            self.current_login = login
            self.view.set_response("")
            self.view.show_upload()
        else:
            self.view.set_response(response)

    def register(self):

        name = self.view.get_reg_name()
        login = self.view.get_reg_login()
        password = self.view.get_reg_password()

        response = self.model.send_form("register", login, password, name)

        self.view.set_response(response)

    def back(self):
        self.view.show_start()

    def upload(self):

        if not self.current_login:
            self.view.set_response("ERROR NOT LOGGED IN")
            return

        path = self.view.get_upload_path()

        response = self.model.send_file(self.current_login, path)
        self.view.set_response(response)