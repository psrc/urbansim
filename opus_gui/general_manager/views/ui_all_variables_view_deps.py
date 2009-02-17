# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'all_variables_view_deps.ui'
#
# Created: Sun Feb 15 17:00:16 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AllVariablesViewDepsGui(object):
    def setupUi(self, AllVariablesViewDepsGui):
        AllVariablesViewDepsGui.setObjectName("AllVariablesViewDepsGui")
        AllVariablesViewDepsGui.resize(508, 163)
        AllVariablesViewDepsGui.setMinimumSize(QtCore.QSize(0, 0))
        self.verticalLayout = QtGui.QVBoxLayout(AllVariablesViewDepsGui)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtGui.QScrollArea(AllVariablesViewDepsGui)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtGui.QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 486, 90))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.label = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName("label")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.widget = QtGui.QWidget(AllVariablesViewDepsGui)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 45))
        self.widget.setObjectName("widget")
        self.hboxlayout = QtGui.QHBoxLayout(self.widget)
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem = QtGui.QSpacerItem(441, 24, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.closeWindow = QtGui.QPushButton(self.widget)
        self.closeWindow.setObjectName("closeWindow")
        self.hboxlayout.addWidget(self.closeWindow)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(AllVariablesViewDepsGui)
        QtCore.QMetaObject.connectSlotsByName(AllVariablesViewDepsGui)

    def retranslateUi(self, AllVariablesViewDepsGui):
        AllVariablesViewDepsGui.setWindowTitle(QtGui.QApplication.translate("AllVariablesViewDepsGui", "Variable editor", None, QtGui.QApplication.UnicodeUTF8))
        self.closeWindow.setText(QtGui.QApplication.translate("AllVariablesViewDepsGui", "Close", None, QtGui.QApplication.UnicodeUTF8))

