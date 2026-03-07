from Client.View.Client_view import ClientView
from Client.Model.Client_model import ClientModel
from Client.Controller.Client_controller import ClientController


def main():
    view = ClientView()
    model = ClientModel(host="127.0.0.1", port=4000)
    ClientController(view, model)
    view.start()


if __name__ == "__main__":
    main()