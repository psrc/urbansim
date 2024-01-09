# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/ckla/Documents/workspace/opus_trunk/opus_gui/abstract_manager/views/renamedialog.ui'
#
# Created: Wed May 20 11:52:08 2009
#      by: PyQt5 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_RenameDialog(object):
    def setupUi(self, RenameDialog):
        RenameDialog.setObjectName("RenameDialog")
        RenameDialog.resize(494, 141)
        self.gridlayout = QtWidgets.QGridLayout(RenameDialog)
        self.gridlayout.setObjectName("gridlayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(RenameDialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.xmlBox = QtWidgets.QGroupBox(RenameDialog)
        self.xmlBox.setObjectName("xmlBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.xmlBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.xmlBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.leName = QtWidgets.QLineEdit(self.xmlBox)
        self.leName.setObjectName("leName")
        self.horizontalLayout.addWidget(self.leName)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.lbl_name_warning = QtWidgets.QLabel(self.xmlBox)
        self.lbl_name_warning.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lbl_name_warning.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lbl_name_warning.setObjectName("lbl_name_warning")
        self.verticalLayout.addWidget(self.lbl_name_warning)
        self.gridlayout.addWidget(self.xmlBox, 0, 0, 1, 1)

        self.retranslateUi(RenameDialog)
        QtCore.QMetaObject.connectSlotsByName(RenameDialog)

    def retranslateUi(self, RenameDialog):
        RenameDialog.setWindowTitle(QtWidgets.QApplication.translate("RenameDialog", "Dialog", None))
        self.label_2.setText(QtWidgets.QApplication.translate("RenameDialog", "Name", None))
        self.lbl_name_warning.setText(QtWidgets.QApplication.translate("RenameDialog", "name warning", None))

