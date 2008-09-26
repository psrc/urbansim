# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'databasesettingsedit.ui'
#
# Created: Mon Sep 22 11:27:21 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DatabaseSettingsEditGui(object):
    def setupUi(self, DatabaseSettingsEditGui):
        DatabaseSettingsEditGui.setObjectName("DatabaseSettingsEditGui")
        DatabaseSettingsEditGui.resize(576, 730)
        self.vboxlayout = QtGui.QVBoxLayout(DatabaseSettingsEditGui)
        self.vboxlayout.setObjectName("vboxlayout")
        self.variableBox = QtGui.QGroupBox(DatabaseSettingsEditGui)
        self.variableBox.setObjectName("variableBox")
        self.gridlayout = QtGui.QGridLayout(self.variableBox)
        self.gridlayout.setObjectName("gridlayout")
        self.vboxlayout.addWidget(self.variableBox)
        self.widget = QtGui.QWidget(DatabaseSettingsEditGui)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 45))
        self.widget.setObjectName("widget")
        self.hboxlayout = QtGui.QHBoxLayout(self.widget)
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem = QtGui.QSpacerItem(441, 24, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.saveChanges = QtGui.QPushButton(self.widget)
        self.saveChanges.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveChanges.sizePolicy().hasHeightForWidth())
        self.saveChanges.setSizePolicy(sizePolicy)
        self.saveChanges.setObjectName("saveChanges")
        self.hboxlayout.addWidget(self.saveChanges)
        self.cancelWindow = QtGui.QPushButton(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelWindow.sizePolicy().hasHeightForWidth())
        self.cancelWindow.setSizePolicy(sizePolicy)
        self.cancelWindow.setObjectName("cancelWindow")
        self.hboxlayout.addWidget(self.cancelWindow)
        self.vboxlayout.addWidget(self.widget)

        self.retranslateUi(DatabaseSettingsEditGui)
        QtCore.QMetaObject.connectSlotsByName(DatabaseSettingsEditGui)

    def retranslateUi(self, DatabaseSettingsEditGui):
        DatabaseSettingsEditGui.setWindowTitle(QtGui.QApplication.translate("DatabaseSettingsEditGui", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.variableBox.setTitle(QtGui.QApplication.translate("DatabaseSettingsEditGui", "Database Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.saveChanges.setText(QtGui.QApplication.translate("DatabaseSettingsEditGui", "Accept Changes", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelWindow.setText(QtGui.QApplication.translate("DatabaseSettingsEditGui", "Close", None, QtGui.QApplication.UnicodeUTF8))

