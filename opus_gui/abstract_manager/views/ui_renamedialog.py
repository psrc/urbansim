# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'renamedialog.ui'
#
# Created: Tue Dec 30 15:22:33 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_RenameDialog(object):
    def setupUi(self, RenameDialog):
        RenameDialog.setObjectName("RenameDialog")
        RenameDialog.resize(494, 108)
        self.gridlayout = QtGui.QGridLayout(RenameDialog)
        self.gridlayout.setObjectName("gridlayout")
        self.xmlBox = QtGui.QGroupBox(RenameDialog)
        self.xmlBox.setObjectName("xmlBox")
        self.hboxlayout = QtGui.QHBoxLayout(self.xmlBox)
        self.hboxlayout.setObjectName("hboxlayout")
        self.label_2 = QtGui.QLabel(self.xmlBox)
        self.label_2.setObjectName("label_2")
        self.hboxlayout.addWidget(self.label_2)
        self.leName = QtGui.QLineEdit(self.xmlBox)
        self.leName.setObjectName("leName")
        self.hboxlayout.addWidget(self.leName)
        self.gridlayout.addWidget(self.xmlBox, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RenameDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(RenameDialog)
        QtCore.QMetaObject.connectSlotsByName(RenameDialog)

    def retranslateUi(self, RenameDialog):
        RenameDialog.setWindowTitle(QtGui.QApplication.translate("RenameDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("RenameDialog", "Name", None, QtGui.QApplication.UnicodeUTF8))

