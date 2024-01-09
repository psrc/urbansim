# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'executetoolset.ui'
#
# Created: Thu Nov 06 11:36:23 2008
#      by: PyQt5 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_ExecuteToolSetGui(object):
    def setupUi(self, ExecuteToolSetGui):
        ExecuteToolSetGui.setObjectName("ExecuteToolSetGui")
        ExecuteToolSetGui.resize(QtCore.QSize(QtCore.QRect(0,0,629,737).size()).expandedTo(ExecuteToolSetGui.minimumSizeHint()))

        self.gridlayout = QtWidgets.QGridLayout(ExecuteToolSetGui)
        self.gridlayout.setObjectName("gridlayout")

        self.executionBox = QtWidgets.QGroupBox(ExecuteToolSetGui)
        self.executionBox.setObjectName("executionBox")

        self.vboxlayout = QtWidgets.QVBoxLayout(self.executionBox)
        self.vboxlayout.setObjectName("vboxlayout")

        self.progressBar_2 = QtWidgets.QProgressBar(self.executionBox)
        self.progressBar_2.setProperty("value",QtCore.QVariant(0))
        self.progressBar_2.setObjectName("progressBar_2")
        self.vboxlayout.addWidget(self.progressBar_2)

        self.textEdit_2 = QtWidgets.QTextEdit(self.executionBox)
        self.textEdit_2.setObjectName("textEdit_2")
        self.vboxlayout.addWidget(self.textEdit_2)
        self.gridlayout.addWidget(self.executionBox,0,0,1,1)

        self.widget = QtWidgets.QWidget(ExecuteToolSetGui)
        self.widget.setMaximumSize(QtCore.QSize(16777215,45))
        self.widget.setObjectName("widget")

        self.gridlayout1 = QtWidgets.QGridLayout(self.widget)
        self.gridlayout1.setObjectName("gridlayout1")

        spacerItem = QtWidgets.QSpacerItem(40,20,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem,0,0,1,1)

        self.execToolSet = QtWidgets.QPushButton(self.widget)
        self.execToolSet.setObjectName("execToolSet")
        self.gridlayout1.addWidget(self.execToolSet,0,1,1,1)

        self.cancelExec = QtWidgets.QPushButton(self.widget)
        self.cancelExec.setObjectName("cancelExec")
        self.gridlayout1.addWidget(self.cancelExec,0,2,1,1)
        self.gridlayout.addWidget(self.widget,1,0,1,1)

        self.retranslateUi(ExecuteToolSetGui)
        QtCore.QMetaObject.connectSlotsByName(ExecuteToolSetGui)

    def retranslateUi(self, ExecuteToolSetGui):
        ExecuteToolSetGui.setWindowTitle(QtWidgets.QApplication.translate("ExecuteToolSetGui", "Dialog", None, QtWidgets.QApplication.UnicodeUTF8))
        self.executionBox.setTitle(QtWidgets.QApplication.translate("ExecuteToolSetGui", "Log/Status", None, QtWidgets.QApplication.UnicodeUTF8))
        self.execToolSet.setText(QtWidgets.QApplication.translate("ExecuteToolSetGui", "Execute Tool Set", None, QtWidgets.QApplication.UnicodeUTF8))
        self.cancelExec.setText(QtWidgets.QApplication.translate("ExecuteToolSetGui", "Cancel", None, QtWidgets.QApplication.UnicodeUTF8))

