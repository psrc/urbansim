# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/ckla/Documents/workspace/opus_trunk/opus_gui/abstract_manager/views/renamedialog.ui'
#
# Created: Wed May 20 11:52:08 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_RenameDialog(object):
    def setupUi(self, RenameDialog):
        RenameDialog.setObjectName("RenameDialog")
        RenameDialog.resize(494, 141)
        self.gridlayout = QtGui.QGridLayout(RenameDialog)
        self.gridlayout.setObjectName("gridlayout")
        self.buttonBox = QtGui.QDialogButtonBox(RenameDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.xmlBox = QtGui.QGroupBox(RenameDialog)
        self.xmlBox.setObjectName("xmlBox")
        self.verticalLayout = QtGui.QVBoxLayout(self.xmlBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtGui.QLabel(self.xmlBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.leName = QtGui.QLineEdit(self.xmlBox)
        self.leName.setObjectName("leName")
        self.horizontalLayout.addWidget(self.leName)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.lbl_name_warning = QtGui.QLabel(self.xmlBox)
        self.lbl_name_warning.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lbl_name_warning.setFrameShadow(QtGui.QFrame.Raised)
        self.lbl_name_warning.setObjectName("lbl_name_warning")
        self.verticalLayout.addWidget(self.lbl_name_warning)
        self.gridlayout.addWidget(self.xmlBox, 0, 0, 1, 1)

        self.retranslateUi(RenameDialog)
        QtCore.QMetaObject.connectSlotsByName(RenameDialog)

    def retranslateUi(self, RenameDialog):
        RenameDialog.setWindowTitle(QtGui.QApplication.translate("RenameDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("RenameDialog", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_name_warning.setText(QtGui.QApplication.translate("RenameDialog", "name warning", None, QtGui.QApplication.UnicodeUTF8))

