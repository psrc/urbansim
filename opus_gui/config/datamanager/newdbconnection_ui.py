# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newdbconnection.ui'
#
# Created: Mon Mar 24 22:34:36 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_NewDbConnectionGui(object):
    def setupUi(self, NewDbConnectionGui):
        NewDbConnectionGui.setObjectName("NewDbConnectionGui")
        NewDbConnectionGui.resize(QtCore.QSize(QtCore.QRect(0,0,412,312).size()).expandedTo(NewDbConnectionGui.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(NewDbConnectionGui)
        self.vboxlayout.setObjectName("vboxlayout")

        self.comboBox = QtGui.QComboBox(NewDbConnectionGui)
        self.comboBox.setObjectName("comboBox")
        self.vboxlayout.addWidget(self.comboBox)

        self.variableBox = QtGui.QGroupBox(NewDbConnectionGui)
        self.variableBox.setObjectName("variableBox")
        self.vboxlayout.addWidget(self.variableBox)

        self.widget = QtGui.QWidget(NewDbConnectionGui)
        self.widget.setMaximumSize(QtCore.QSize(16777215,45))
        self.widget.setObjectName("widget")

        self.gridlayout = QtGui.QGridLayout(self.widget)
        self.gridlayout.setObjectName("gridlayout")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,0,0,1,1)

        self.createConfig = QtGui.QPushButton(self.widget)
        self.createConfig.setObjectName("createConfig")
        self.gridlayout.addWidget(self.createConfig,0,1,1,1)

        self.cancelConfig = QtGui.QPushButton(self.widget)
        self.cancelConfig.setObjectName("cancelConfig")
        self.gridlayout.addWidget(self.cancelConfig,0,2,1,1)
        self.vboxlayout.addWidget(self.widget)

        self.retranslateUi(NewDbConnectionGui)
        QtCore.QMetaObject.connectSlotsByName(NewDbConnectionGui)

    def retranslateUi(self, NewDbConnectionGui):
        NewDbConnectionGui.setWindowTitle(QtGui.QApplication.translate("NewDbConnectionGui", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(QtGui.QApplication.translate("NewDbConnectionGui", "Select Connection Type", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(QtGui.QApplication.translate("NewDbConnectionGui", "Server Database Connection", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(QtGui.QApplication.translate("NewDbConnectionGui", "ESRI File Database Connection", None, QtGui.QApplication.UnicodeUTF8))
        self.variableBox.setTitle(QtGui.QApplication.translate("NewDbConnectionGui", "New Database Connection", None, QtGui.QApplication.UnicodeUTF8))
        self.createConfig.setText(QtGui.QApplication.translate("NewDbConnectionGui", "Create Db Connection", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelConfig.setText(QtGui.QApplication.translate("NewDbConnectionGui", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

