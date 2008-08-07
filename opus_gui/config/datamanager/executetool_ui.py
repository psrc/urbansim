# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'executetool.ui'
#
# Created: Thu Aug  7 16:14:55 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ExecuteToolGui(object):
    def setupUi(self, ExecuteToolGui):
        ExecuteToolGui.setObjectName("ExecuteToolGui")
        ExecuteToolGui.resize(QtCore.QSize(QtCore.QRect(0,0,412,408).size()).expandedTo(ExecuteToolGui.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(ExecuteToolGui)
        self.vboxlayout.setObjectName("vboxlayout")

        self.variableBox = QtGui.QGroupBox(ExecuteToolGui)
        self.variableBox.setObjectName("variableBox")
        self.vboxlayout.addWidget(self.variableBox)

        self.widget = QtGui.QWidget(ExecuteToolGui)
        self.widget.setMaximumSize(QtCore.QSize(16777215,45))
        self.widget.setObjectName("widget")

        self.gridlayout = QtGui.QGridLayout(self.widget)
        self.gridlayout.setObjectName("gridlayout")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,0,0,1,1)

        self.execTool = QtGui.QPushButton(self.widget)
        self.execTool.setObjectName("execTool")
        self.gridlayout.addWidget(self.execTool,0,1,1,1)

        self.cancelExec = QtGui.QPushButton(self.widget)
        self.cancelExec.setObjectName("cancelExec")
        self.gridlayout.addWidget(self.cancelExec,0,2,1,1)
        self.vboxlayout.addWidget(self.widget)

        self.retranslateUi(ExecuteToolGui)
        QtCore.QMetaObject.connectSlotsByName(ExecuteToolGui)

    def retranslateUi(self, ExecuteToolGui):
        ExecuteToolGui.setWindowTitle(QtGui.QApplication.translate("ExecuteToolGui", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.variableBox.setTitle(QtGui.QApplication.translate("ExecuteToolGui", "Tool Variables", None, QtGui.QApplication.UnicodeUTF8))
        self.execTool.setText(QtGui.QApplication.translate("ExecuteToolGui", "Execute Tool", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelExec.setText(QtGui.QApplication.translate("ExecuteToolGui", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

