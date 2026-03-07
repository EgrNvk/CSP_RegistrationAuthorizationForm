class ClientController:

    def __init__(self, view, model):

        self.view = view
        self.model = model

        self.view.btn_choose_login.config(command=self.view.show_login)
        self.view.btn_choose_register.config(command=self.view.show_register)

        self.view.btn_login.config(command=self.login)
        self.view.btn_register.config(command=self.register)

    def login(self):

        login = self.view.get_login()
        password = self.view.get_password()

        response = self.model.send_form("login", login, password)

        self.view.set_response(response)

    def register(self):

        name = self.view.get_reg_name()
        login = self.view.get_reg_login()
        password = self.view.get_reg_password()

        response = self.model.send_form("register", login, password, name)

        self.view.set_response(response)