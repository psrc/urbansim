# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'databasesettingsedit.ui'
#
# Created: Sat Jan 31 13:08:45 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DatabaseSettingsEditGui(object):
    def setupUi(self, DatabaseSettingsEditGui):
        DatabaseSettingsEditGui.setObjectName("DatabaseSettingsEditGui")
        DatabaseSettingsEditGui.resize(550, 582)
        self.vboxlayout = QtGui.QVBoxLayout(DatabaseSettingsEditGui)
        self.vboxlayout.setObjectName("vboxlayout")
        self.variableBox = QtGui.QGroupBox(DatabaseSettingsEditGui)
        self.variableBox.setObjectName("variableBox")
        self.gridlayout = QtGui.QGridLayout(self.variableBox)
        self.gridlayout.setObjectName("gridlayout")
        self.vboxlayout.addWidget(self.variableBox)
        self.buttonBox = QtGui.QDialogButtonBox(DatabaseSettingsEditGui)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(DatabaseSettingsEditGui)
        QtCore.QMetaObject.connectSlotsByName(DatabaseSettingsEditGui)

    def retranslateUi(self, DatabaseSettingsEditGui):
        DatabaseSettingsEditGui.setWindowTitle(QtGui.QApplication.translate("DatabaseSettingsEditGui", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.variableBox.setTitle(QtGui.QApplication.translate("DatabaseSettingsEditGui", "Database Settings", None, QtGui.QApplication.UnicodeUTF8))

