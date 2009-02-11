# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'variable_selector.ui'
#
# Created: Sun Feb 08 16:38:30 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_VariableSelector(object):
    def setupUi(self, VariableSelector):
        VariableSelector.setObjectName("VariableSelector")
        VariableSelector.resize(656, 486)
        self.verticalLayout = QtGui.QVBoxLayout(VariableSelector)
        self.verticalLayout.setObjectName("verticalLayout")
        self.table_container = QtGui.QWidget(VariableSelector)
        self.table_container.setObjectName("table_container")
        self.gridLayout = QtGui.QGridLayout(self.table_container)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout.addWidget(self.table_container)
        self.buttonBox = QtGui.QDialogButtonBox(VariableSelector)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(VariableSelector)
        QtCore.QMetaObject.connectSlotsByName(VariableSelector)

    def retranslateUi(self, VariableSelector):
        VariableSelector.setWindowTitle(QtGui.QApplication.translate("VariableSelector", "Model variable selection", None, QtGui.QApplication.UnicodeUTF8))

