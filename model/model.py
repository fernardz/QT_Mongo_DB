from PyQt5.QtCore import QObject

class Model(QObject):
    def __init__(self):
        super().__init__()
        self.__username = "us"
        self.__password = "ps"

    def set_username(self, username):
        self.__username = username

    def get_username(self):
        return self.__username

    def set_password(self, password):
        self.__password = password

    def get_password(self):
        return self.__password
