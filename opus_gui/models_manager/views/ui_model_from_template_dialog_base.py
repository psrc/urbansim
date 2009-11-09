# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/ckla/Documents/workspace/variable_library_rewrite/opus_gui/models_manager/views/model_from_template_dialog_base.ui'
#
# Created: Sat Apr 25 17:48:22 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DynamicTemplateDialog(object):
    def setupUi(self, DynamicTemplateDialog):
        DynamicTemplateDialog.setObjectName("DynamicTemplateDialog")
        DynamicTemplateDialog.setWindowModality(QtCore.Qt.WindowModal)
        DynamicTemplateDialog.resize(637, 273)
        self.verticalLayout = QtGui.QVBoxLayout(DynamicTemplateDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_header = QtGui.QLabel(DynamicTemplateDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_header.sizePolicy().hasHeightForWidth())
        self.lbl_header.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lbl_header.setFont(font)
        self.lbl_header.setObjectName("lbl_header")
        self.verticalLayout.addWidget(self.lbl_header)
        self.frame = QtGui.QFrame(DynamicTemplateDialog)
        self.frame.setFrameShape(QtGui.QFrame.Panel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(100, 0))
        self.label.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.le_model_name = QtGui.QLineEdit(self.frame)
        self.le_model_name.setObjectName("le_model_name")
        self.horizontalLayout_2.addWidget(self.le_model_name)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.lbl_name_warning = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setItalic(False)
        font.setBold(False)
        self.lbl_name_warning.setFont(font)
        self.lbl_name_warning.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lbl_name_warning.setMargin(5)
        self.lbl_name_warning.setObjectName("lbl_name_warning")
        self.verticalLayout_2.addWidget(self.lbl_name_warning)
        self.verticalLayout.addWidget(self.frame)
        self.dynamic_widgets = QtGui.QGridLayout()
        self.dynamic_widgets.setObjectName("dynamic_widgets")
        self.verticalLayout.addLayout(self.dynamic_widgets)
        self.buttonBox = QtGui.QDialogButtonBox(DynamicTemplateDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DynamicTemplateDialog)
        QtCore.QMetaObject.connectSlotsByName(DynamicTemplateDialog)

    def retranslateUi(self, DynamicTemplateDialog):
        DynamicTemplateDialog.setWindowTitle(QtGui.QApplication.translate("DynamicTemplateDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_header.setText(QtGui.QApplication.translate("DynamicTemplateDialog", "Creating model from template X", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DynamicTemplateDialog", "Model name:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_name_warning.setText(QtGui.QApplication.translate("DynamicTemplateDialog", "There is already a model \"X\", please enter another name.", None, QtGui.QApplication.UnicodeUTF8))

