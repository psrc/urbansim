# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addparam.ui'
#
# Created: Sat Sep 12 09:37:03 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AddParamGui(object):
    def setupUi(self, AddParamGui):
        AddParamGui.setObjectName("AddParamGui")
        AddParamGui.resize(297, 266)
        self.vboxlayout = QtGui.QVBoxLayout(AddParamGui)
        self.vboxlayout.setObjectName("vboxlayout")
        self.tabWidget = QtGui.QTabWidget(AddParamGui)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.vboxlayout1 = QtGui.QVBoxLayout(self.tab_3)
        self.vboxlayout1.setObjectName("vboxlayout1")
        self.attributesBox = QtGui.QGroupBox(self.tab_3)
        self.attributesBox.setObjectName("attributesBox")
        self.nameEdit = QtGui.QLineEdit(self.attributesBox)
        self.nameEdit.setGeometry(QtCore.QRect(60, 30, 181, 20))
        self.nameEdit.setObjectName("nameEdit")
        self.label = QtGui.QLabel(self.attributesBox)
        self.label.setGeometry(QtCore.QRect(20, 30, 46, 14))
        self.label.setObjectName("label")
        self.typeComboBox = QtGui.QComboBox(self.attributesBox)
        self.typeComboBox.setGeometry(QtCore.QRect(60, 60, 115, 22))
        self.typeComboBox.setObjectName("typeComboBox")
        self.typeComboBox.addItem(QtCore.QString())
        self.typeComboBox.addItem(QtCore.QString())
        self.typeComboBox.addItem(QtCore.QString())
        self.typeComboBox.addItem(QtCore.QString())
        self.label_2 = QtGui.QLabel(self.attributesBox)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 46, 14))
        self.label_2.setObjectName("label_2")
        self.defaultEdit = QtGui.QLineEdit(self.attributesBox)
        self.defaultEdit.setGeometry(QtCore.QRect(60, 90, 181, 20))
        self.defaultEdit.setObjectName("defaultEdit")
        self.label_3 = QtGui.QLabel(self.attributesBox)
        self.label_3.setGeometry(QtCore.QRect(10, 90, 46, 14))
        self.label_3.setObjectName("label_3")
        self.requiredComboBox = QtGui.QComboBox(self.attributesBox)
        self.requiredComboBox.setGeometry(QtCore.QRect(60, 120, 69, 22))
        self.requiredComboBox.setObjectName("requiredComboBox")
        self.requiredComboBox.addItem(QtCore.QString())
        self.requiredComboBox.addItem(QtCore.QString())
        self.label_4 = QtGui.QLabel(self.attributesBox)
        self.label_4.setGeometry(QtCore.QRect(10, 120, 46, 14))
        self.label_4.setObjectName("label_4")
        self.vboxlayout1.addWidget(self.attributesBox)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.vboxlayout2 = QtGui.QVBoxLayout(self.tab_4)
        self.vboxlayout2.setObjectName("vboxlayout2")
        self.toolhelpEdit = QtGui.QTextEdit(self.tab_4)
        self.toolhelpEdit.setObjectName("toolhelpEdit")
        self.vboxlayout2.addWidget(self.toolhelpEdit)
        self.tabWidget.addTab(self.tab_4, "")
        self.vboxlayout.addWidget(self.tabWidget)
        self.widget = QtGui.QWidget(AddParamGui)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 45))
        self.widget.setObjectName("widget")
        self.gridlayout = QtGui.QGridLayout(self.widget)
        self.gridlayout.setObjectName("gridlayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 0, 0, 1, 1)
        self.addParam = QtGui.QPushButton(self.widget)
        self.addParam.setObjectName("addParam")
        self.gridlayout.addWidget(self.addParam, 0, 1, 1, 1)
        self.cancelAddParam = QtGui.QPushButton(self.widget)
        self.cancelAddParam.setObjectName("cancelAddParam")
        self.gridlayout.addWidget(self.cancelAddParam, 0, 2, 1, 1)
        self.vboxlayout.addWidget(self.widget)

        self.retranslateUi(AddParamGui)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(AddParamGui)

    def retranslateUi(self, AddParamGui):
        AddParamGui.setWindowTitle(QtGui.QApplication.translate("AddParamGui", "Add New Parameter", None, QtGui.QApplication.UnicodeUTF8))
        self.attributesBox.setTitle(QtGui.QApplication.translate("AddParamGui", "Parameter Attributes", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("AddParamGui", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.typeComboBox.setItemText(0, QtGui.QApplication.translate("AddParamGui", "string", None, QtGui.QApplication.UnicodeUTF8))
        self.typeComboBox.setItemText(1, QtGui.QApplication.translate("AddParamGui", "dir_path", None, QtGui.QApplication.UnicodeUTF8))
        self.typeComboBox.setItemText(2, QtGui.QApplication.translate("AddParamGui", "file_path", None, QtGui.QApplication.UnicodeUTF8))
        self.typeComboBox.setItemText(3, QtGui.QApplication.translate("AddParamGui", "db_connection_hook", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("AddParamGui", "Type", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("AddParamGui", "Default", None, QtGui.QApplication.UnicodeUTF8))
        self.requiredComboBox.setItemText(0, QtGui.QApplication.translate("AddParamGui", "True", None, QtGui.QApplication.UnicodeUTF8))
        self.requiredComboBox.setItemText(1, QtGui.QApplication.translate("AddParamGui", "False", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("AddParamGui", "Required", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("AddParamGui", "Tool Setup", None, QtGui.QApplication.UnicodeUTF8))
        self.toolhelpEdit.setHtml(QtGui.QApplication.translate("AddParamGui", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Use this dialog to create a new parameter which will be passed to your python tool module.  Parameters created here will be accessible in the GUI when you run the tool.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("AddParamGui", "Tool Help", None, QtGui.QApplication.UnicodeUTF8))
        self.addParam.setText(QtGui.QApplication.translate("AddParamGui", "Create New Param", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelAddParam.setText(QtGui.QApplication.translate("AddParamGui", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

