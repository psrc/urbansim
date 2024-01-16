# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/travis/Documents/workspace/opus/opus_gui/run/overwrite_dialog.ui'
#
# Created: Thu Sep 25 11:39:25 2008
#      by: PyQt5 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_dlgOverwriteRun(object):
    def setupUi(self, dlgOverwriteRun):
        dlgOverwriteRun.setObjectName("dlgOverwriteRun")
        dlgOverwriteRun.resize(413, 133)
        self.buttonBox = QtWidgets.QDialogButtonBox(dlgOverwriteRun)
        self.buttonBox.setGeometry(QtCore.QRect(60, 90, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(dlgOverwriteRun)
        self.label.setGeometry(QtCore.QRect(50, 20, 331, 51))
        self.label.setWordWrap(True)
        self.label.setObjectName("label")

        self.retranslateUi(dlgOverwriteRun)
        QtCore.QObject.connect(self.buttonBox, QtCore.pyqtSignal("accepted()"), dlgOverwriteRun.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.pyqtSignal("rejected()"), dlgOverwriteRun.reject)
        QtCore.QMetaObject.connectSlotsByName(dlgOverwriteRun)

    def retranslateUi(self, dlgOverwriteRun):
        dlgOverwriteRun.setWindowTitle(QtWidgets.QApplication.translate("dlgOverwriteRun", "Overwrite existing run?", None))
        self.label.setText(QtWidgets.QApplication.translate("dlgOverwriteRun", "A simulation run already has that name. Would you like to overwrite the existing simulation run?", None))

