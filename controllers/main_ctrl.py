from views.login import Login
from views.dbs import ItemsView
from views.dbs import ItemForm


class Controller:

    def __init__(self, model, config):
        self._model=model
        self._config=config
        pass

    def show_login(self):
        self.login = Login(self._model)
        #self.login.switch_window.connect(self.show_main)
        self.login.switch_window.connect(self.show_comp_type)
        self.login.show()

    def show_comp_type(self):
        self.itemsview=ItemsView(self._model, self._config)
        self.itemsview.cellselected.connect(self.show_item_sub)
        self.itemsview.ui.CreateItem.clicked.connect(lambda: self.show_item_sub())
        self.login.close()
        self.itemsview.show()

    def show_item_sub(self,*args):
        print(dir(self))
        if len(args)==1:
            selected=args[0]
            dialog=ItemForm(self.itemsview,ccode="%s"%selected)
            dialog.setWindowTitle('Modify Record')
        else:
            print('simple select')
            print('SENDERSSSSS')
            dialog=ItemForm(self.itemsview)
            dialog.setWindowTitle('New Record')
        dialog.finished.connect(lambda: self.update_item_view())
        dialog.open()

    def update_item_view(self):
        self.itemsview.connect_to_Mongo()
        self.itemsview.show()
