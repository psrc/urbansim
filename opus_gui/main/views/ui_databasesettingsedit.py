# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/ckla/Documents/workspace/variable_library_rewrite/opus_gui/main/views/databasesettingsedit.ui'
#
# Created: Mon Apr 20 22:26:22 2009
#      by: PyQt5 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_DatabaseSettingsEditGui(object):
    def setupUi(self, DatabaseSettingsEditGui):
        DatabaseSettingsEditGui.setObjectName("DatabaseSettingsEditGui")
        DatabaseSettingsEditGui.resize(550, 582)
        self.vboxlayout = QtWidgets.QVBoxLayout(DatabaseSettingsEditGui)
        self.vboxlayout.setObjectName("vboxlayout")
        self.variableBox = QtWidgets.QGroupBox(DatabaseSettingsEditGui)
        self.variableBox.setObjectName("variableBox")
        self.gridlayout = QtWidgets.QGridLayout(self.variableBox)
        self.gridlayout.setObjectName("gridlayout")
        self.vboxlayout.addWidget(self.variableBox)
        self.description = QtWidgets.QLabel(DatabaseSettingsEditGui)
        self.description.setObjectName("description")
        self.vboxlayout.addWidget(self.description)
        self.buttonBox = QtWidgets.QDialogButtonBox(DatabaseSettingsEditGui)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(DatabaseSettingsEditGui)
        QtCore.QMetaObject.connectSlotsByName(DatabaseSettingsEditGui)

    def retranslateUi(self, DatabaseSettingsEditGui):
        DatabaseSettingsEditGui.setWindowTitle(QtWidgets.QApplication.translate("DatabaseSettingsEditGui", "Dialog", None, QtWidgets.QApplication.UnicodeUTF8))
        self.variableBox.setTitle(QtWidgets.QApplication.translate("DatabaseSettingsEditGui", "Database Settings", None, QtWidgets.QApplication.UnicodeUTF8))
