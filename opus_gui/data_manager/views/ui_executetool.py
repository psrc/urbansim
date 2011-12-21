# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'executetool.ui'
#
# Created: Thu Nov 06 11:36:23 2008
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ExecuteToolGui(object):
    def setupUi(self, ExecuteToolGui):
        ExecuteToolGui.setObjectName("ExecuteToolGui")
        ExecuteToolGui.resize(QtCore.QSize(QtCore.QRect(0,0,629,737).size()).expandedTo(ExecuteToolGui.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(ExecuteToolGui)
        self.vboxlayout.setObjectName("vboxlayout")

        self.tabWidget = QtGui.QTabWidget(ExecuteToolGui)
        self.tabWidget.setObjectName("tabWidget")

        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.tab_3)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.variableBox = QtGui.QGroupBox(self.tab_3)
        self.variableBox.setObjectName("variableBox")
        self.vboxlayout1.addWidget(self.variableBox)

        self.executionBox = QtGui.QGroupBox(self.tab_3)
        self.executionBox.setObjectName("executionBox")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.executionBox)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.progressBar = QtGui.QProgressBar(self.executionBox)
        self.progressBar.setProperty("value",QtCore.QVariant(0))
        self.progressBar.setObjectName("progressBar")
        self.vboxlayout2.addWidget(self.progressBar)

        self.textEdit = QtGui.QTextEdit(self.executionBox)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setReadOnly(True)
        self.vboxlayout2.addWidget(self.textEdit)
        self.vboxlayout1.addWidget(self.executionBox)
        self.tabWidget.addTab(self.tab_3,"")

        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")

        self.vboxlayout3 = QtGui.QVBoxLayout(self.tab_4)
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.toolhelpEdit = QtGui.QTextEdit(self.tab_4)
        self.toolhelpEdit.setObjectName("toolhelpEdit")
        self.toolhelpEdit.setReadOnly(True)
        self.vboxlayout3.addWidget(self.toolhelpEdit)
        self.tabWidget.addTab(self.tab_4,"")
        self.vboxlayout.addWidget(self.tabWidget)

        self.widget = QtGui.QWidget(ExecuteToolGui)
        self.widget.setMaximumSize(QtCore.QSize(16777215,45))
        self.widget.setObjectName("widget")

        self.gridlayout = QtGui.QGridLayout(self.widget)
        self.gridlayout.setObjectName("gridlayout")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,0,0,1,1)
        
        self.saveBack = QtGui.QPushButton(self.widget)
        self.saveBack.setObjectName("saveBack")
        self.gridlayout.addWidget(self.saveBack,0,1,1,1)

        self.execTool = QtGui.QPushButton(self.widget)
        self.execTool.setObjectName("execTool")
        self.execTool.setDefault(True)
        self.gridlayout.addWidget(self.execTool,0,2,1,1)

        self.cancelExec = QtGui.QPushButton(self.widget)
        self.cancelExec.setObjectName("cancelExec")
        self.gridlayout.addWidget(self.cancelExec,0,3,1,1)
        self.vboxlayout.addWidget(self.widget)

        self.retranslateUi(ExecuteToolGui)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ExecuteToolGui)

    def retranslateUi(self, ExecuteToolGui):
        ExecuteToolGui.setWindowTitle(QtGui.QApplication.translate("ExecuteToolGui", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.variableBox.setTitle(QtGui.QApplication.translate("ExecuteToolGui", "Variables", None, QtGui.QApplication.UnicodeUTF8))
        self.executionBox.setTitle(QtGui.QApplication.translate("ExecuteToolGui", "Log/Status", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("ExecuteToolGui", "Tool Setup", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("ExecuteToolGui", "Tool Help", None, QtGui.QApplication.UnicodeUTF8))
        self.saveBack.setText(QtGui.QApplication.translate("ExecuteToolGui", "Save Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.execTool.setText(QtGui.QApplication.translate("ExecuteToolGui", "Execute Tool", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelExec.setText(QtGui.QApplication.translate("ExecuteToolGui", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

