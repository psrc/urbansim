# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'all_variables.ui'
#
# Created: Mon Jun 23 21:56:40 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AllVariablesGui(object):
    def setupUi(self, AllVariablesGui):
        AllVariablesGui.setObjectName("AllVariablesGui")
        AllVariablesGui.resize(QtCore.QSize(QtCore.QRect(0,0,931,625).size()).expandedTo(AllVariablesGui.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(AllVariablesGui)
        self.vboxlayout.setObjectName("vboxlayout")

        self.variableBox = QtGui.QGroupBox(AllVariablesGui)
        self.variableBox.setObjectName("variableBox")

        self.gridlayout = QtGui.QGridLayout(self.variableBox)
        self.gridlayout.setObjectName("gridlayout")
        self.vboxlayout.addWidget(self.variableBox)

        self.widget = QtGui.QWidget(AllVariablesGui)
        self.widget.setMaximumSize(QtCore.QSize(16777215,45))
        self.widget.setObjectName("widget")

        self.gridlayout1 = QtGui.QGridLayout(self.widget)
        self.gridlayout1.setObjectName("gridlayout1")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem,0,0,1,1)

        self.saveChanges = QtGui.QPushButton(self.widget)
        self.saveChanges.setObjectName("saveChanges")
        self.gridlayout1.addWidget(self.saveChanges,0,1,1,1)

        self.cancelWindow = QtGui.QPushButton(self.widget)
        self.cancelWindow.setObjectName("cancelWindow")
        self.gridlayout1.addWidget(self.cancelWindow,0,2,1,1)
        self.vboxlayout.addWidget(self.widget)

        self.retranslateUi(AllVariablesGui)
        QtCore.QMetaObject.connectSlotsByName(AllVariablesGui)

    def retranslateUi(self, AllVariablesGui):
        AllVariablesGui.setWindowTitle(QtGui.QApplication.translate("AllVariablesGui", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.variableBox.setTitle(QtGui.QApplication.translate("AllVariablesGui", "all_variables", None, QtGui.QApplication.UnicodeUTF8))
        self.saveChanges.setText(QtGui.QApplication.translate("AllVariablesGui", "Save Changes", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelWindow.setText(QtGui.QApplication.translate("AllVariablesGui", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

