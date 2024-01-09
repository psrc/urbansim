# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newtoolbatch.ui'
#
# Created: Thu Nov 06 11:36:22 2008
#      by: PyQt5 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,400,300).size()).expandedTo(Dialog.minimumSizeHint()))

        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30,240,341,32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.NoButton|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox,QtCore.pyqtSignal("accepted()"),Dialog.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.pyqtSignal("rejected()"),Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, QtWidgets.QApplication.UnicodeUTF8))

