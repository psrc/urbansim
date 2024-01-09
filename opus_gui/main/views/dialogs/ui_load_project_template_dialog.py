# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'load_project_template_dialog.ui'
#
# Created: Sat Mar 20 11:10:35 2010
#      by: PyQt5 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_LoadProjectTemplateDialog(object):
    def setupUi(self, LoadProjectTemplateDialog):
        LoadProjectTemplateDialog.setObjectName("LoadProjectTemplateDialog")
        LoadProjectTemplateDialog.setWindowModality(QtCore.Qt.WindowModal)
        LoadProjectTemplateDialog.resize(637, 280)
        self.verticalLayout = QtWidgets.QVBoxLayout(LoadProjectTemplateDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_header = QtWidgets.QLabel(LoadProjectTemplateDialog)
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
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lbl_error = QtWidgets.QLabel(LoadProjectTemplateDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_error.sizePolicy().hasHeightForWidth())
        self.lbl_error.setSizePolicy(sizePolicy)
        self.lbl_error.setFrameShape(QtWidgets.QFrame.Panel)
        self.lbl_error.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lbl_error.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.lbl_error.setObjectName("lbl_error")
        self.horizontalLayout.addWidget(self.lbl_error)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.frame = QtWidgets.QFrame(LoadProjectTemplateDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.rb_use_builtin = QtWidgets.QRadioButton(self.frame)
        self.rb_use_builtin.setChecked(True)
        self.rb_use_builtin.setObjectName("rb_use_builtin")
        self.verticalLayout_3.addWidget(self.rb_use_builtin)
        self.lst_builtin_templates = QtWidgets.QListWidget(self.frame)
        self.lst_builtin_templates.setObjectName("lst_builtin_templates")
        self.verticalLayout_3.addWidget(self.lst_builtin_templates)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.rb_use_custom = QtWidgets.QRadioButton(self.frame)
        self.rb_use_custom.setObjectName("rb_use_custom")
        self.horizontalLayout_4.addWidget(self.rb_use_custom)
        self.le_custom_filename = QtWidgets.QLineEdit(self.frame)
        self.le_custom_filename.setObjectName("le_custom_filename")
        self.horizontalLayout_4.addWidget(self.le_custom_filename)
        self.tb_custom_browse = QtWidgets.QToolButton(self.frame)
        self.tb_custom_browse.setObjectName("tb_custom_browse")
        self.horizontalLayout_4.addWidget(self.tb_custom_browse)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.verticalLayout.addWidget(self.frame)
        self.buttonBox = QtWidgets.QDialogButtonBox(LoadProjectTemplateDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(LoadProjectTemplateDialog)
        QtCore.QMetaObject.connectSlotsByName(LoadProjectTemplateDialog)

    def retranslateUi(self, LoadProjectTemplateDialog):
        LoadProjectTemplateDialog.setWindowTitle(QtWidgets.QApplication.translate("LoadProjectTemplateDialog", "Dialog", None, QtWidgets.QApplication.UnicodeUTF8))
        self.lbl_header.setText(QtWidgets.QApplication.translate("LoadProjectTemplateDialog", "Step 1 of 2: Load project template", None, QtWidgets.QApplication.UnicodeUTF8))
        self.lbl_error.setText(QtWidgets.QApplication.translate("LoadProjectTemplateDialog", "<error message>", None, QtWidgets.QApplication.UnicodeUTF8))
        self.rb_use_builtin.setText(QtWidgets.QApplication.translate("LoadProjectTemplateDialog", "Use builtin project template", None, QtWidgets.QApplication.UnicodeUTF8))
        self.rb_use_custom.setText(QtWidgets.QApplication.translate("LoadProjectTemplateDialog", "Use custom template", None, QtWidgets.QApplication.UnicodeUTF8))
        self.tb_custom_browse.setText(QtWidgets.QApplication.translate("LoadProjectTemplateDialog", "...", None, QtWidgets.QApplication.UnicodeUTF8))

