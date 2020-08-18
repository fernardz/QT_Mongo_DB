from PyQt5 import QtCore, QtWidgets
import mongoengine as mgd


class Login(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal()

    def __init__(self, model, config):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Login')
        self._model = model
        self._config = config
        layout = QtWidgets.QGridLayout()

        self.usr = QtWidgets.QLineEdit()
        self.pwd = QtWidgets.QLineEdit()

        self.button = QtWidgets.QPushButton('Login')

        self.button.setEnabled(False)
        self.usr.textChanged.connect(self.disableButton)
        self.pwd.textChanged.connect(self.disableButton)

        self.button.clicked.connect(self.login)

        layout.addWidget(self.usr)
        layout.addWidget(self.pwd)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def disableButton(self):
        if len(self.pwd.text()) > 0 & len(self.usr.text()):
            self.button.setEnabled(True)

    def login(self):
        self._model.set_username(self.usr.text())
        self._model.set_password(self.pwd.text())
        self.connect_to_Mongo()
        print(self._model.get_username())
        print(self.mg)
        try:
            mgd.get_db()
            self.switch_window.emit()
        except Exception as e:
            if e.code==18:
                QtWidgets.QMessageBox.critical(self,'Auth Error','Could not authorize')
            mgd.disconnect()
        #self.switch_window.emit()

    def connect_to_Mongo(self):

        self.mg=mgd.connect(self._config.DB,
        username=self._model.get_username(),
        password=self._model.get_password())
