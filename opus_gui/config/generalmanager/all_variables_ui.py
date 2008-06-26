# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'all_variables.ui'
#
# Created: Thu Jun 26 01:11:55 2008
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

        self.hboxlayout = QtGui.QHBoxLayout(self.widget)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtGui.QSpacerItem(441,24,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.addNew = QtGui.QPushButton(self.widget)
        self.addNew.setEnabled(True)
        self.addNew.setObjectName("addNew")
        self.hboxlayout.addWidget(self.addNew)

        self.deleteRow = QtGui.QPushButton(self.widget)
        self.deleteRow.setEnabled(False)
        self.deleteRow.setObjectName("deleteRow")
        self.hboxlayout.addWidget(self.deleteRow)

        self.line = QtGui.QFrame(self.widget)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.hboxlayout.addWidget(self.line)

        self.saveChanges = QtGui.QPushButton(self.widget)
        self.saveChanges.setEnabled(False)
        self.saveChanges.setObjectName("saveChanges")
        self.hboxlayout.addWidget(self.saveChanges)

        self.cancelWindow = QtGui.QPushButton(self.widget)
        self.cancelWindow.setObjectName("cancelWindow")
        self.hboxlayout.addWidget(self.cancelWindow)
        self.vboxlayout.addWidget(self.widget)

        self.retranslateUi(AllVariablesGui)
        QtCore.QMetaObject.connectSlotsByName(AllVariablesGui)

    def retranslateUi(self, AllVariablesGui):
        AllVariablesGui.setWindowTitle(QtGui.QApplication.translate("AllVariablesGui", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.variableBox.setTitle(QtGui.QApplication.translate("AllVariablesGui", "all_variables", None, QtGui.QApplication.UnicodeUTF8))
        self.addNew.setText(QtGui.QApplication.translate("AllVariablesGui", "Add New Row", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteRow.setText(QtGui.QApplication.translate("AllVariablesGui", "Delete Selected Rows", None, QtGui.QApplication.UnicodeUTF8))
        self.saveChanges.setText(QtGui.QApplication.translate("AllVariablesGui", "Save Changes", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelWindow.setText(QtGui.QApplication.translate("AllVariablesGui", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

