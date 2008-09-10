# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'all_variables_select.ui'
#
# Created: Wed Aug 27 12:47:14 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AllVariablesSelectGui(object):
    def setupUi(self, AllVariablesSelectGui):
        AllVariablesSelectGui.setObjectName("AllVariablesSelectGui")
        AllVariablesSelectGui.resize(QtCore.QSize(QtCore.QRect(0,0,1000,600).size()).expandedTo(AllVariablesSelectGui.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(AllVariablesSelectGui)
        self.vboxlayout.setObjectName("vboxlayout")

        self.variableBox = QtGui.QGroupBox(AllVariablesSelectGui)
        self.variableBox.setObjectName("variableBox")

        self.gridlayout = QtGui.QGridLayout(self.variableBox)
        self.gridlayout.setObjectName("gridlayout")
        self.vboxlayout.addWidget(self.variableBox)

        self.widget = QtGui.QWidget(AllVariablesSelectGui)
        self.widget.setMaximumSize(QtCore.QSize(16777215,45))
        self.widget.setObjectName("widget")

        self.hboxlayout = QtGui.QHBoxLayout(self.widget)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtGui.QSpacerItem(441,24,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.line = QtGui.QFrame(self.widget)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.hboxlayout.addWidget(self.line)

        self.saveSelections = QtGui.QPushButton(self.widget)
        self.saveSelections.setEnabled(True)
        self.saveSelections.setObjectName("saveSelections")
        self.hboxlayout.addWidget(self.saveSelections)

        self.cancelWindow = QtGui.QPushButton(self.widget)
        self.cancelWindow.setObjectName("cancelWindow")
        self.hboxlayout.addWidget(self.cancelWindow)
        self.vboxlayout.addWidget(self.widget)

        self.retranslateUi(AllVariablesSelectGui)
        QtCore.QMetaObject.connectSlotsByName(AllVariablesSelectGui)

    def retranslateUi(self, AllVariablesSelectGui):
        AllVariablesSelectGui.setWindowTitle(QtGui.QApplication.translate("AllVariablesSelectGui", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.variableBox.setTitle(QtGui.QApplication.translate("AllVariablesSelectGui", "Variable Library", None, QtGui.QApplication.UnicodeUTF8))
        self.saveSelections.setText(QtGui.QApplication.translate("AllVariablesSelectGui", "Accept Selections", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelWindow.setText(QtGui.QApplication.translate("AllVariablesSelectGui", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

