import sys
from PyQt5.QtWidgets import QApplication
from model.model import Model
from controllers.main_ctrl import Controller
import config

class App(QApplication):
    def __init__(self,sys_argv):
        super(App, self).__init__(sys_argv)
        self.model=Model()
        self.config=config.test()
        self.main_controller=Controller(self.model,self.config)
        self.main_controller.show_login()

if __name__ == '__main__':
    app=App(sys.argv)
    sys.exit(app.exec_())
