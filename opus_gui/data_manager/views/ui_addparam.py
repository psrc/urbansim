# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addparam.ui'
#
# Created: Sat Sep 12 09:37:03 2009
#      by: PyQt5 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_AddParamGui(object):
    def setupUi(self, AddParamGui):
        AddParamGui.setObjectName("AddParamGui")
        AddParamGui.resize(297, 266)
        self.vboxlayout = QtWidgets.QVBoxLayout(AddParamGui)
        self.vboxlayout.setObjectName("vboxlayout")
        self.tabWidget = QtWidgets.QTabWidget(AddParamGui)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.vboxlayout1 = QtWidgets.QVBoxLayout(self.tab_3)
        self.vboxlayout1.setObjectName("vboxlayout1")
        self.attributesBox = QtWidgets.QGroupBox(self.tab_3)
        self.attributesBox.setObjectName("attributesBox")
        self.nameEdit = QtWidgets.QLineEdit(self.attributesBox)
        self.nameEdit.setGeometry(QtCore.QRect(60, 30, 181, 20))
        self.nameEdit.setObjectName("nameEdit")
        self.label = QtWidgets.QLabel(self.attributesBox)
        self.label.setGeometry(QtCore.QRect(20, 30, 46, 14))
        self.label.setObjectName("label")
        self.typeComboBox = QtWidgets.QComboBox(self.attributesBox)
        self.typeComboBox.setGeometry(QtCore.QRect(60, 60, 115, 22))
        self.typeComboBox.setObjectName("typeComboBox")
        self.typeComboBox.addItem("")
        self.typeComboBox.addItem("")
        self.typeComboBox.addItem("")
        self.typeComboBox.addItem("")
        self.typeComboBox.addItem("")
        self.label_2 = QtWidgets.QLabel(self.attributesBox)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 46, 14))
        self.label_2.setObjectName("label_2")
        self.defaultEdit = QtWidgets.QLineEdit(self.attributesBox)
        self.defaultEdit.setGeometry(QtCore.QRect(60, 90, 181, 20))
        self.defaultEdit.setObjectName("defaultEdit")
        self.label_3 = QtWidgets.QLabel(self.attributesBox)
        self.label_3.setGeometry(QtCore.QRect(10, 90, 46, 14))
        self.label_3.setObjectName("label_3")
        self.requiredComboBox = QtWidgets.QComboBox(self.attributesBox)
        self.requiredComboBox.setGeometry(QtCore.QRect(60, 120, 69, 22))
        self.requiredComboBox.setObjectName("requiredComboBox")
        self.requiredComboBox.addItem("")
        self.requiredComboBox.addItem("")
        self.label_4 = QtWidgets.QLabel(self.attributesBox)
        self.label_4.setGeometry(QtCore.QRect(10, 120, 46, 14))
        self.label_4.setObjectName("label_4")
        self.vboxlayout1.addWidget(self.attributesBox)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.vboxlayout2 = QtWidgets.QVBoxLayout(self.tab_4)
        self.vboxlayout2.setObjectName("vboxlayout2")
        self.toolhelpEdit = QtWidgets.QTextEdit(self.tab_4)
        self.toolhelpEdit.setObjectName("toolhelpEdit")
        self.vboxlayout2.addWidget(self.toolhelpEdit)
        self.tabWidget.addTab(self.tab_4, "")
        self.vboxlayout.addWidget(self.tabWidget)
        self.widget = QtWidgets.QWidget(AddParamGui)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 45))
        self.widget.setObjectName("widget")
        self.gridlayout = QtWidgets.QGridLayout(self.widget)
        self.gridlayout.setObjectName("gridlayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 0, 0, 1, 1)
        self.addParam = QtWidgets.QPushButton(self.widget)
        self.addParam.setObjectName("addParam")
        self.gridlayout.addWidget(self.addParam, 0, 1, 1, 1)
        self.cancelAddParam = QtWidgets.QPushButton(self.widget)
        self.cancelAddParam.setObjectName("cancelAddParam")
        self.gridlayout.addWidget(self.cancelAddParam, 0, 2, 1, 1)
        self.vboxlayout.addWidget(self.widget)

        self.retranslateUi(AddParamGui)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(AddParamGui)

    def retranslateUi(self, AddParamGui):
        AddParamGui.setWindowTitle(QtWidgets.QApplication.translate("AddParamGui", "Add New Parameter", None, QtWidgets.QApplication.UnicodeUTF8))
        self.attributesBox.setTitle(QtWidgets.QApplication.translate("AddParamGui", "Parameter Attributes", None, QtWidgets.QApplication.UnicodeUTF8))
        self.label.setText(QtWidgets.QApplication.translate("AddParamGui", "Name", None, QtWidgets.QApplication.UnicodeUTF8))
        self.typeComboBox.setItemText(0, QtWidgets.QApplication.translate("AddParamGui", "string", None, QtWidgets.QApplication.UnicodeUTF8))
        self.typeComboBox.setItemText(1, QtWidgets.QApplication.translate("AddParamGui", "dir_path", None, QtWidgets.QApplication.UnicodeUTF8))
        self.typeComboBox.setItemText(2, QtWidgets.QApplication.translate("AddParamGui", "file_path", None, QtWidgets.QApplication.UnicodeUTF8))
        self.typeComboBox.setItemText(3, QtWidgets.QApplication.translate("AddParamGui", "db_connection_hook", None, QtWidgets.QApplication.UnicodeUTF8))
        self.typeComboBox.setItemText(4, QtWidgets.QApplication.translate("AddParamGui", "boolean", None, QtWidgets.QApplication.UnicodeUTF8))
        self.label_2.setText(QtWidgets.QApplication.translate("AddParamGui", "Type", None, QtWidgets.QApplication.UnicodeUTF8))
        self.label_3.setText(QtWidgets.QApplication.translate("AddParamGui", "Default", None, QtWidgets.QApplication.UnicodeUTF8))
        self.requiredComboBox.setItemText(0, QtWidgets.QApplication.translate("AddParamGui", "True", None, QtWidgets.QApplication.UnicodeUTF8))
        self.requiredComboBox.setItemText(1, QtWidgets.QApplication.translate("AddParamGui", "False", None, QtWidgets.QApplication.UnicodeUTF8))
        self.label_4.setText(QtWidgets.QApplication.translate("AddParamGui", "Required", None, QtWidgets.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtWidgets.QApplication.translate("AddParamGui", "Tool Setup", None, QtWidgets.QApplication.UnicodeUTF8))
        self.toolhelpEdit.setHtml(QtWidgets.QApplication.translate("AddParamGui", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Use this dialog to create a new parameter which will be passed to your python tool module.  Parameters created here will be accessible in the GUI when you run the tool.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p></body></html>", None, QtWidgets.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtWidgets.QApplication.translate("AddParamGui", "Tool Help", None, QtWidgets.QApplication.UnicodeUTF8))
        self.addParam.setText(QtWidgets.QApplication.translate("AddParamGui", "Create New Param", None, QtWidgets.QApplication.UnicodeUTF8))
        self.cancelAddParam.setText(QtWidgets.QApplication.translate("AddParamGui", "Cancel", None, QtWidgets.QApplication.UnicodeUTF8))

