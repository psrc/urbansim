# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'overwrite_dialog.ui'
#
# Created: Wed Jun 25 15:51:45 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_dlgOverwriteRun(object):
    def setupUi(self, dlgOverwriteRun):
        dlgOverwriteRun.setObjectName("dlgOverwriteRun")
        dlgOverwriteRun.resize(413, 133)
        self.buttonBox = QtGui.QDialogButtonBox(dlgOverwriteRun)
        self.buttonBox.setGeometry(QtCore.QRect(60, 90, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtGui.QLabel(dlgOverwriteRun)
        self.label.setGeometry(QtCore.QRect(50, 20, 331, 51))
        self.label.setWordWrap(True)
        self.label.setObjectName("label")

        self.retranslateUi(dlgOverwriteRun)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), dlgOverwriteRun.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), dlgOverwriteRun.reject)
        QtCore.QMetaObject.connectSlotsByName(dlgOverwriteRun)

    def retranslateUi(self, dlgOverwriteRun):
        dlgOverwriteRun.setWindowTitle(QtGui.QApplication.translate("dlgOverwriteRun", "Overwrite existing run?", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("dlgOverwriteRun", "A simulation run already has that name. Would you like to overwrite the existing simulation run?", None, QtGui.QApplication.UnicodeUTF8))

