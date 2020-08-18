from PyQt5 import QtCore, QtWidgets


class Login(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal()

    def __init__(self, model):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Login')
        self._model = model
        layout = QtWidgets.QGridLayout()

        self.usr = QtWidgets.QLineEdit()
        self.pwd = QtWidgets.QLineEdit()

        self.button = QtWidgets.QPushButton('Login')
        self.button.clicked.connect(self.login)

        layout.addWidget(self.usr)
        layout.addWidget(self.pwd)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def login(self):
        self._model.set_username(self.usr.text())
        self._model.set_password(self.pwd.text())
        self.switch_window.emit()
