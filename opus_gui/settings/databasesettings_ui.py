# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'databasesettings.ui'
#
# Created: Wed Aug 13 15:06:52 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_databaseConfigEditor(object):
    def setupUi(self, databaseConfigEditor):
        databaseConfigEditor.setObjectName("databaseConfigEditor")
        databaseConfigEditor.resize(400,300)
        self.buttonBox = QtGui.QDialogButtonBox(databaseConfigEditor)
        self.buttonBox.setGeometry(QtCore.QRect(30,240,341,32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(databaseConfigEditor)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),databaseConfigEditor.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),databaseConfigEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(databaseConfigEditor)

    def retranslateUi(self, databaseConfigEditor):
        databaseConfigEditor.setWindowTitle(QtGui.QApplication.translate("databaseConfigEditor", "Database Settings Editor", None, QtGui.QApplication.UnicodeUTF8))

