# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/travis/Documents/workspace/opus/opus_gui/config/generalmanager/all_variables_select.ui'
#
# Created: Wed Sep 24 15:22:35 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AllVariablesSelectGui(object):
    def setupUi(self, AllVariablesSelectGui):
        AllVariablesSelectGui.setObjectName("AllVariablesSelectGui")
        AllVariablesSelectGui.resize(1000, 600)
        self.verticalLayout = QtGui.QVBoxLayout(AllVariablesSelectGui)
        self.verticalLayout.setObjectName("verticalLayout")
        self.variableBox = QtGui.QWidget(AllVariablesSelectGui)
        self.variableBox.setObjectName("variableBox")
        self.gridLayout = QtGui.QGridLayout(self.variableBox)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout.addWidget(self.variableBox)
        self.widget = QtGui.QWidget(AllVariablesSelectGui)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 45))
        self.widget.setObjectName("widget")
        self.hboxlayout = QtGui.QHBoxLayout(self.widget)
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem = QtGui.QSpacerItem(441, 24, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
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
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(AllVariablesSelectGui)
        QtCore.QMetaObject.connectSlotsByName(AllVariablesSelectGui)

    def retranslateUi(self, AllVariablesSelectGui):
        AllVariablesSelectGui.setWindowTitle(QtGui.QApplication.translate("AllVariablesSelectGui", "Model variable selection", None, QtGui.QApplication.UnicodeUTF8))
        self.saveSelections.setText(QtGui.QApplication.translate("AllVariablesSelectGui", "Accept Selections", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelWindow.setText(QtGui.QApplication.translate("AllVariablesSelectGui", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

