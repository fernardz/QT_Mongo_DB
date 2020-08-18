from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot
from resources.ui_DbView import Ui_DbView
from resources.ui_DbSub import Ui_DbSub
import logging

import mongoengine as mgd

log= logging.getLogger()
console=logging.StreamHandler()
format_str = '%(asctime)s\t%(levelname)s -- %(processName)s %(filename)s:%(lineno)s -- %(message)s'
console.setFormatter(logging.Formatter(format_str))
log.addHandler(console)
log.setLevel(logging.DEBUG)

class Items(mgd.Document):
    code=mgd.StringField(require=True, unique=True, max_length=10)
    desc=mgd.StringField(require=True, max_length=50)

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

class ItemsView(QtWidgets.QDialog):
    cellselected=QtCore.pyqtSignal('QString', name='cellselected')
    def __init__(self, model, config):
        QtWidgets.QDialog.__init__(self)
        self.ui=Ui_DbView()
        self.ui.setupUi(self)
        self.ui.dbView.installEventFilter(self)
        self._model = model
        self._config=config
        self.connect_to_Mongo()

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.ContextMenu and event.reason()==0 and source is self.ui.dbView):
            #print(source.model().index())

            indexes=source.selectedIndexes()
            if len(indexes)==1:
                if indexes[0].isValid():
                    index=indexes[0]
                    print(source.model().index(index.row(),0).data())
                    self.cellselected.emit(source.model().index(index.row(),0).data())

        return super(ItemsView,self).eventFilter(source,event)

    def switch(self):
        print(self._model.usr)
        self.switch_window.emit(self.line_edit.text())

    def connect_to_Mongo(self):

        self.mg=mgd.connect(self._config.DB,
        username=self._model.get_username(),
        password=self._model.get_password())

        data=[[x.code, x.desc] for x in Items.objects().all()]
        if len(data)>0:
            model = TableModel(data)
            self.ui.dbView.setModel(model)
        self.ui.dbView.horizontalHeader().setStretchLastSection(True)

        self.ui.dbView.setSortingEnabled(True)

class ItemForm(QtWidgets.QDialog):
    def __init__(self,parent, **kwargs):
        super().__init__(parent)
        self.ui=Ui_DbSub()
        self.ui.setupUi(self)
        if "ccode" in kwargs:
            #log.info("Kick off Comp Type Update")
            self.ui.CodeIn.setText(kwargs['ccode'])
            self.ui.CodeIn.setEnabled(False)
            self.res=Items.objects(code=kwargs['ccode']).first()
            self.old_value=self.res.desc
            self.ui.DescIn.setText(self.old_value)
            self.ui.FBtn.clicked.connect(self.btn_click)
        else:
            print(self.ui.FBtn.buttons(), 'YAAAAAAAAAAs')
            log.info("Kick off New")
            self.old_value='New'
            self.ui.FBtn.clicked.connect(self.btn_click)

    def btn_click(self, btn):
        print(self)
        role=self.sender().buttonRole(btn)
        if role==2:#DestructiveRole
            self.destroy()
        self.close()


    def destroy(self):
        self.res.delete()

    def accept(self):
        print(self)
        if self.old_value==self.ui.DescIn.text():
            log.warning('Tried to update same value')
        elif self.old_value=='New':
            try:
                ccode=self.ui.CodeIn.text()
                cdesc=self.ui.DescIn.text()
                if (len(ccode)>=3 and len(cdesc)>=3):
                    ccode="%s"%ccode
                    cdesc="%s"%cdesc
                    Items.objects(code=ccode).upsert_one(set_on_insert__desc=cdesc)
                    QtWidgets.QDialog.accept(self)
                else:
                    log.warning("COMP CODE and DESC LESS THAN 3 CHARACTERS")
            except:
                log.error('Could not insert value')
        else:
            try:
                self.res.desc="%s"%self.ui.DescIn.text()
                self.res.save()
                log.info("Updated Comp Desc to: %s"%self.ui.DescIn.text())
                QtWidgets.QDialog.accept(self)
            except:
                log.error('Could not update value')
