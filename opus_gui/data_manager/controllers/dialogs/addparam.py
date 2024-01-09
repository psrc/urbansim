# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt5.QtCore  import  Qt, QRegExp, QObject, pyqtSignal, QSize, pyqtSlot
from  PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QLabel, QWidget, QLineEdit, QVBoxLayout, QFileDialog, QDialog, QHBoxLayout, QPushButton, QComboBox, QMessageBox
from opus_gui.data_manager.views.ui_addparam import Ui_AddParamGui
from opus_gui.data_manager.run.run_tool import OpusTool, RunToolThread

class addParamGui(QDialog, Ui_AddParamGui):
    def __init__(self, mainwindow, node):
        QDialog.__init__(self, mainwindow)
        self.setupUi(self)
        self.mainwindow = mainwindow
        self.node = node
        if node is not None:
            self.nameEdit.setText(node.get('name') if node.get('name') is not None else '')
            self.defaultEdit.setText(node.text if node.text is not None else '')
            type = node.get('param_type')
            self.typeComboBox.setCurrentIndex(self.typeComboBox.findText(type))
            required = node.get('required')
            self.requiredComboBox.setCurrentIndex(self.requiredComboBox.findText(required))
            self.setWindowTitle('Edit Parameter')
            help = self.toolhelpEdit.toPlainText()
            import string
            help.replace('create a new','edit a')
            self.toolhelpEdit.clear()
            self.toolhelpEdit.insertPlainText(help)

    @pyqtSlot()
    def on_cancelAddParam_clicked(self):
        self.reject()

    @pyqtSlot()
    def on_addParam_clicked(self):
        if(len(self.nameEdit.text()) == 0):
            self.nameEdit.setText('must specify name')
            self.nameEdit.selectAll()
            self.nameEdit.setFocus()
            return
        self.accept()
