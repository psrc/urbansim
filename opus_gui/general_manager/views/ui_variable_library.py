# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'variable_library.ui'
#
# Created: Mon Feb 09 14:09:36 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_VariableLibrary(object):
    def setupUi(self, VariableLibrary):
        VariableLibrary.setObjectName("VariableLibrary")
        VariableLibrary.resize(594, 600)
        self.vboxlayout = QtGui.QVBoxLayout(VariableLibrary)
        self.vboxlayout.setObjectName("vboxlayout")
        self.table_container = QtGui.QWidget(VariableLibrary)
        self.table_container.setObjectName("table_container")
        self.layout = QtGui.QGridLayout(self.table_container)
        self.layout.setObjectName("layout")
        self.vboxlayout.addWidget(self.table_container)
        self.widget = QtGui.QWidget(VariableLibrary)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 45))
        self.widget.setObjectName("widget")
        self.hboxlayout = QtGui.QHBoxLayout(self.widget)
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem = QtGui.QSpacerItem(441, 24, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.pbNewVariable = QtGui.QPushButton(self.widget)
        self.pbNewVariable.setEnabled(True)
        self.pbNewVariable.setObjectName("pbNewVariable")
        self.hboxlayout.addWidget(self.pbNewVariable)
        self.pbValidateSelected = QtGui.QPushButton(self.widget)
        self.pbValidateSelected.setObjectName("pbValidateSelected")
        self.hboxlayout.addWidget(self.pbValidateSelected)
        self.line = QtGui.QFrame(self.widget)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.hboxlayout.addWidget(self.line)
        self.pbSave = QtGui.QPushButton(self.widget)
        self.pbSave.setEnabled(False)
        self.pbSave.setObjectName("pbSave")
        self.hboxlayout.addWidget(self.pbSave)
        self.pbClose = QtGui.QPushButton(self.widget)
        self.pbClose.setObjectName("pbClose")
        self.hboxlayout.addWidget(self.pbClose)
        self.vboxlayout.addWidget(self.widget)
        self.pbDEBUG = QtGui.QPushButton(VariableLibrary)
        self.pbDEBUG.setObjectName("pbDEBUG")
        self.vboxlayout.addWidget(self.pbDEBUG)

        self.retranslateUi(VariableLibrary)
        QtCore.QMetaObject.connectSlotsByName(VariableLibrary)

    def retranslateUi(self, VariableLibrary):
        VariableLibrary.setWindowTitle(QtGui.QApplication.translate("VariableLibrary", "Variable Library", None, QtGui.QApplication.UnicodeUTF8))
        self.pbNewVariable.setText(QtGui.QApplication.translate("VariableLibrary", "Add New Variable", None, QtGui.QApplication.UnicodeUTF8))
        self.pbValidateSelected.setToolTip(QtGui.QApplication.translate("VariableLibrary", "Checks all variable syntax and makes sure that it can be computed on the baseyear data.", None, QtGui.QApplication.UnicodeUTF8))
        self.pbValidateSelected.setText(QtGui.QApplication.translate("VariableLibrary", "Validate Selected", None, QtGui.QApplication.UnicodeUTF8))
        self.pbSave.setText(QtGui.QApplication.translate("VariableLibrary", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.pbClose.setText(QtGui.QApplication.translate("VariableLibrary", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.pbDEBUG.setText(QtGui.QApplication.translate("VariableLibrary", "DELETE ME!!!", None, QtGui.QApplication.UnicodeUTF8))

