# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'executetoolset.ui'
#
# Created: Thu Nov 06 11:36:23 2008
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ExecuteToolSetGui(object):
    def setupUi(self, ExecuteToolSetGui):
        ExecuteToolSetGui.setObjectName("ExecuteToolSetGui")
        ExecuteToolSetGui.resize(QtCore.QSize(QtCore.QRect(0,0,629,737).size()).expandedTo(ExecuteToolSetGui.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(ExecuteToolSetGui)
        self.gridlayout.setObjectName("gridlayout")

        self.executionBox = QtGui.QGroupBox(ExecuteToolSetGui)
        self.executionBox.setObjectName("executionBox")

        self.vboxlayout = QtGui.QVBoxLayout(self.executionBox)
        self.vboxlayout.setObjectName("vboxlayout")

        self.progressBar_2 = QtGui.QProgressBar(self.executionBox)
        self.progressBar_2.setProperty("value",QtCore.QVariant(0))
        self.progressBar_2.setObjectName("progressBar_2")
        self.vboxlayout.addWidget(self.progressBar_2)

        self.textEdit_2 = QtGui.QTextEdit(self.executionBox)
        self.textEdit_2.setObjectName("textEdit_2")
        self.vboxlayout.addWidget(self.textEdit_2)
        self.gridlayout.addWidget(self.executionBox,0,0,1,1)

        self.widget = QtGui.QWidget(ExecuteToolSetGui)
        self.widget.setMaximumSize(QtCore.QSize(16777215,45))
        self.widget.setObjectName("widget")

        self.gridlayout1 = QtGui.QGridLayout(self.widget)
        self.gridlayout1.setObjectName("gridlayout1")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem,0,0,1,1)

        self.execToolSet = QtGui.QPushButton(self.widget)
        self.execToolSet.setObjectName("execToolSet")
        self.gridlayout1.addWidget(self.execToolSet,0,1,1,1)

        self.cancelExec = QtGui.QPushButton(self.widget)
        self.cancelExec.setObjectName("cancelExec")
        self.gridlayout1.addWidget(self.cancelExec,0,2,1,1)
        self.gridlayout.addWidget(self.widget,1,0,1,1)

        self.retranslateUi(ExecuteToolSetGui)
        QtCore.QMetaObject.connectSlotsByName(ExecuteToolSetGui)

    def retranslateUi(self, ExecuteToolSetGui):
        ExecuteToolSetGui.setWindowTitle(QtGui.QApplication.translate("ExecuteToolSetGui", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.executionBox.setTitle(QtGui.QApplication.translate("ExecuteToolSetGui", "Log/Status", None, QtGui.QApplication.UnicodeUTF8))
        self.execToolSet.setText(QtGui.QApplication.translate("ExecuteToolSetGui", "Execute Tool Set", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelExec.setText(QtGui.QApplication.translate("ExecuteToolSetGui", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

