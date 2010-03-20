# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'load_project_template_dialog.ui'
#
# Created: Sat Mar 20 11:10:35 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_LoadProjectTemplateDialog(object):
    def setupUi(self, LoadProjectTemplateDialog):
        LoadProjectTemplateDialog.setObjectName("LoadProjectTemplateDialog")
        LoadProjectTemplateDialog.setWindowModality(QtCore.Qt.WindowModal)
        LoadProjectTemplateDialog.resize(637, 280)
        self.verticalLayout = QtGui.QVBoxLayout(LoadProjectTemplateDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_header = QtGui.QLabel(LoadProjectTemplateDialog)
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
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lbl_error = QtGui.QLabel(LoadProjectTemplateDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_error.sizePolicy().hasHeightForWidth())
        self.lbl_error.setSizePolicy(sizePolicy)
        self.lbl_error.setFrameShape(QtGui.QFrame.Panel)
        self.lbl_error.setFrameShadow(QtGui.QFrame.Raised)
        self.lbl_error.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.lbl_error.setObjectName("lbl_error")
        self.horizontalLayout.addWidget(self.lbl_error)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.frame = QtGui.QFrame(LoadProjectTemplateDialog)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.rb_use_builtin = QtGui.QRadioButton(self.frame)
        self.rb_use_builtin.setChecked(True)
        self.rb_use_builtin.setObjectName("rb_use_builtin")
        self.verticalLayout_3.addWidget(self.rb_use_builtin)
        self.lst_builtin_templates = QtGui.QListWidget(self.frame)
        self.lst_builtin_templates.setObjectName("lst_builtin_templates")
        self.verticalLayout_3.addWidget(self.lst_builtin_templates)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.rb_use_custom = QtGui.QRadioButton(self.frame)
        self.rb_use_custom.setObjectName("rb_use_custom")
        self.horizontalLayout_4.addWidget(self.rb_use_custom)
        self.le_custom_filename = QtGui.QLineEdit(self.frame)
        self.le_custom_filename.setObjectName("le_custom_filename")
        self.horizontalLayout_4.addWidget(self.le_custom_filename)
        self.tb_custom_browse = QtGui.QToolButton(self.frame)
        self.tb_custom_browse.setObjectName("tb_custom_browse")
        self.horizontalLayout_4.addWidget(self.tb_custom_browse)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.verticalLayout.addWidget(self.frame)
        self.buttonBox = QtGui.QDialogButtonBox(LoadProjectTemplateDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(LoadProjectTemplateDialog)
        QtCore.QMetaObject.connectSlotsByName(LoadProjectTemplateDialog)

    def retranslateUi(self, LoadProjectTemplateDialog):
        LoadProjectTemplateDialog.setWindowTitle(QtGui.QApplication.translate("LoadProjectTemplateDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_header.setText(QtGui.QApplication.translate("LoadProjectTemplateDialog", "Step 1 of 2: Load project template", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_error.setText(QtGui.QApplication.translate("LoadProjectTemplateDialog", "<error message>", None, QtGui.QApplication.UnicodeUTF8))
        self.rb_use_builtin.setText(QtGui.QApplication.translate("LoadProjectTemplateDialog", "Use builtin project template", None, QtGui.QApplication.UnicodeUTF8))
        self.rb_use_custom.setText(QtGui.QApplication.translate("LoadProjectTemplateDialog", "Use custom template", None, QtGui.QApplication.UnicodeUTF8))
        self.tb_custom_browse.setText(QtGui.QApplication.translate("LoadProjectTemplateDialog", "...", None, QtGui.QApplication.UnicodeUTF8))

