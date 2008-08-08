# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'all_variables_edit.ui'
#
# Created: Fri Aug  8 11:37:26 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AllVariablesEditGui(object):
    def setupUi(self, AllVariablesEditGui):
        AllVariablesEditGui.setObjectName("AllVariablesEditGui")
        AllVariablesEditGui.resize(QtCore.QSize(QtCore.QRect(0,0,1000,600).size()).expandedTo(AllVariablesEditGui.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(AllVariablesEditGui)
        self.vboxlayout.setObjectName("vboxlayout")

        self.variableBox = QtGui.QGroupBox(AllVariablesEditGui)
        self.variableBox.setObjectName("variableBox")

        self.gridlayout = QtGui.QGridLayout(self.variableBox)
        self.gridlayout.setObjectName("gridlayout")
        self.vboxlayout.addWidget(self.variableBox)

        self.widget = QtGui.QWidget(AllVariablesEditGui)
        self.widget.setMaximumSize(QtCore.QSize(16777215,45))
        self.widget.setObjectName("widget")

        self.hboxlayout = QtGui.QHBoxLayout(self.widget)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtGui.QSpacerItem(441,24,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.addNewVariable = QtGui.QPushButton(self.widget)
        self.addNewVariable.setEnabled(True)
        self.addNewVariable.setObjectName("addNewVariable")
        self.hboxlayout.addWidget(self.addNewVariable)

        self.deleteVariables = QtGui.QPushButton(self.widget)
        self.deleteVariables.setEnabled(False)
        self.deleteVariables.setObjectName("deleteVariables")
        self.hboxlayout.addWidget(self.deleteVariables)

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

        self.retranslateUi(AllVariablesEditGui)
        QtCore.QMetaObject.connectSlotsByName(AllVariablesEditGui)

    def retranslateUi(self, AllVariablesEditGui):
        AllVariablesEditGui.setWindowTitle(QtGui.QApplication.translate("AllVariablesEditGui", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.variableBox.setTitle(QtGui.QApplication.translate("AllVariablesEditGui", "all_variables", None, QtGui.QApplication.UnicodeUTF8))
        self.addNewVariable.setText(QtGui.QApplication.translate("AllVariablesEditGui", "Add New Variable", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteVariables.setText(QtGui.QApplication.translate("AllVariablesEditGui", "Delete Selected Variables", None, QtGui.QApplication.UnicodeUTF8))
        self.saveChanges.setText(QtGui.QApplication.translate("AllVariablesEditGui", "Save Changes", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelWindow.setText(QtGui.QApplication.translate("AllVariablesEditGui", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

