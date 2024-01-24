# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/ckla/Documents/workspace/variable_library_rewrite/opus_gui/models_manager/views/model_from_template_dialog_base.ui'
#
# Created: Sat Apr 25 17:48:22 2009
#      by: PyQt5 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_DynamicTemplateDialog(object):
    def setupUi(self, DynamicTemplateDialog):
        DynamicTemplateDialog.setObjectName("DynamicTemplateDialog")
        DynamicTemplateDialog.setWindowModality(QtCore.Qt.WindowModal)
        DynamicTemplateDialog.resize(637, 273)
        self.verticalLayout = QtWidgets.QVBoxLayout(DynamicTemplateDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_header = QtWidgets.QLabel(DynamicTemplateDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_header.sizePolicy().hasHeightForWidth())
        self.lbl_header.setSizePolicy(sizePolicy)
        font = QtWidgets.QFont()
        font.setPointSize(14)
        self.lbl_header.setFont(font)
        self.lbl_header.setObjectName("lbl_header")
        self.verticalLayout.addWidget(self.lbl_header)
        self.frame = QtWidgets.QFrame(DynamicTemplateDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(100, 0))
        self.label.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.le_model_name = QtWidgets.QLineEdit(self.frame)
        self.le_model_name.setObjectName("le_model_name")
        self.horizontalLayout_2.addWidget(self.le_model_name)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.lbl_name_warning = QtWidgets.QLabel(self.frame)
        font = QtWidgets.QFont()
        font.setWeight(50)
        font.setItalic(False)
        font.setBold(False)
        self.lbl_name_warning.setFont(font)
        self.lbl_name_warning.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lbl_name_warning.setContentsMargins(5, 5, 5, 5)
        self.lbl_name_warning.setObjectName("lbl_name_warning")
        self.verticalLayout_2.addWidget(self.lbl_name_warning)
        self.verticalLayout.addWidget(self.frame)
        self.dynamic_widgets = QtWidgets.QGridLayout()
        self.dynamic_widgets.setObjectName("dynamic_widgets")
        self.verticalLayout.addLayout(self.dynamic_widgets)
        self.buttonBox = QtWidgets.QDialogButtonBox(DynamicTemplateDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DynamicTemplateDialog)
        QtCore.QMetaObject.connectSlotsByName(DynamicTemplateDialog)

    def retranslateUi(self, DynamicTemplateDialog):
        DynamicTemplateDialog.setWindowTitle(QtWidgets.QApplication.translate("DynamicTemplateDialog", "Dialog", None))
        self.lbl_header.setText(QtWidgets.QApplication.translate("DynamicTemplateDialog", "Creating model from template X", None))
        self.label.setText(QtWidgets.QApplication.translate("DynamicTemplateDialog", "Model name:", None))
        self.lbl_name_warning.setText(QtWidgets.QApplication.translate("DynamicTemplateDialog", "There is already a model \"X\", please enter another name.", None))

