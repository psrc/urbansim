# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\Christoffer Klang\My Documents\workspace\opus_trunk\opus_gui\general_manager\views\variable_editor.ui'
#
# Created: Thu May 28 12:41:29 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_VariableEditor(object):
    def setupUi(self, VariableEditor):
        VariableEditor.setObjectName("VariableEditor")
        VariableEditor.resize(688, 483)
        self.verticalLayout = QtGui.QVBoxLayout(VariableEditor)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(VariableEditor)
        self.label.setMinimumSize(QtCore.QSize(100, 0))
        self.label.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.leVarName = QtGui.QLineEdit(VariableEditor)
        self.leVarName.setObjectName("leVarName")
        self.verticalLayout.addWidget(self.leVarName)
        self.frame_name_warning = QtGui.QFrame(VariableEditor)
        self.frame_name_warning.setFrameShape(QtGui.QFrame.Panel)
        self.frame_name_warning.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_name_warning.setObjectName("frame_name_warning")
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.frame_name_warning)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lbl_name_warning = QtGui.QLabel(self.frame_name_warning)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.lbl_name_warning.setFont(font)
        self.lbl_name_warning.setObjectName("lbl_name_warning")
        self.horizontalLayout_5.addWidget(self.lbl_name_warning)
        self.verticalLayout.addWidget(self.frame_name_warning)
        self.label_3 = QtGui.QLabel(VariableEditor)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.le_var_def = QtGui.QPlainTextEdit(VariableEditor)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.le_var_def.setFont(font)
        self.le_var_def.setTabChangesFocus(True)
        self.le_var_def.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.le_var_def.setObjectName("le_var_def")
        self.verticalLayout.addWidget(self.le_var_def)
        self.line_2 = QtGui.QFrame(VariableEditor)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lbl_info = QtGui.QLabel(VariableEditor)
        self.lbl_info.setObjectName("lbl_info")
        self.horizontalLayout_4.addWidget(self.lbl_info)
        self.pb_change = QtGui.QToolButton(VariableEditor)
        self.pb_change.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.pb_change.setObjectName("pb_change")
        self.horizontalLayout_4.addWidget(self.pb_change)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.group_settings = QtGui.QGroupBox(VariableEditor)
        self.group_settings.setEnabled(True)
        self.group_settings.setObjectName("group_settings")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.group_settings)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.rbUseModel = QtGui.QRadioButton(self.group_settings)
        self.rbUseModel.setObjectName("rbUseModel")
        self.verticalLayout_3.addWidget(self.rbUseModel)
        self.rbUseIndicator = QtGui.QRadioButton(self.group_settings)
        self.rbUseIndicator.setObjectName("rbUseIndicator")
        self.verticalLayout_3.addWidget(self.rbUseIndicator)
        self.rbUseBoth = QtGui.QRadioButton(self.group_settings)
        self.rbUseBoth.setObjectName("rbUseBoth")
        self.verticalLayout_3.addWidget(self.rbUseBoth)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.line_3 = QtGui.QFrame(self.group_settings)
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout_2.addWidget(self.line_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtGui.QLabel(self.group_settings)
        self.label_4.setMinimumSize(QtCore.QSize(100, 0))
        self.label_4.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.cboVarType = QtGui.QComboBox(self.group_settings)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cboVarType.sizePolicy().hasHeightForWidth())
        self.cboVarType.setSizePolicy(sizePolicy)
        self.cboVarType.setObjectName("cboVarType")
        self.cboVarType.addItem(QtCore.QString())
        self.cboVarType.addItem(QtCore.QString())
        self.cboVarType.addItem(QtCore.QString())
        self.horizontalLayout.addWidget(self.cboVarType)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addWidget(self.group_settings)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btnCheckSyntax = QtGui.QPushButton(VariableEditor)
        self.btnCheckSyntax.setObjectName("btnCheckSyntax")
        self.horizontalLayout_3.addWidget(self.btnCheckSyntax)
        self.btnCheckData = QtGui.QPushButton(VariableEditor)
        self.btnCheckData.setObjectName("btnCheckData")
        self.horizontalLayout_3.addWidget(self.btnCheckData)
        spacerItem1 = QtGui.QSpacerItem(441, 24, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.buttonBox = QtGui.QDialogButtonBox(VariableEditor)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_3.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(VariableEditor)
        QtCore.QMetaObject.connectSlotsByName(VariableEditor)

    def retranslateUi(self, VariableEditor):
        VariableEditor.setWindowTitle(QtGui.QApplication.translate("VariableEditor", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setToolTip(QtGui.QApplication.translate("VariableEditor", "A name for this variable. Use only alphanumeric characters", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("VariableEditor", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_name_warning.setText(QtGui.QApplication.translate("VariableEditor", "_name warning_", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("VariableEditor", "Definition:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_info.setText(QtGui.QApplication.translate("VariableEditor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This variable is an <span style=\" font-weight:600;\">expression</span> that will be used as a <span style=\" font-weight:600;\">Model Variable</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_change.setText(QtGui.QApplication.translate("VariableEditor", "Hide Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.group_settings.setTitle(QtGui.QApplication.translate("VariableEditor", "Variable settings", None, QtGui.QApplication.UnicodeUTF8))
        self.rbUseModel.setToolTip(QtGui.QApplication.translate("VariableEditor", "The variable will be used as a Model Variable", None, QtGui.QApplication.UnicodeUTF8))
        self.rbUseModel.setText(QtGui.QApplication.translate("VariableEditor", "Use as a Model Variable", None, QtGui.QApplication.UnicodeUTF8))
        self.rbUseIndicator.setToolTip(QtGui.QApplication.translate("VariableEditor", "The variable will be used as an Indicator", None, QtGui.QApplication.UnicodeUTF8))
        self.rbUseIndicator.setText(QtGui.QApplication.translate("VariableEditor", "Use as an Indicator", None, QtGui.QApplication.UnicodeUTF8))
        self.rbUseBoth.setToolTip(QtGui.QApplication.translate("VariableEditor", "The variable will be used as both a Model Variable and an Indicator", None, QtGui.QApplication.UnicodeUTF8))
        self.rbUseBoth.setText(QtGui.QApplication.translate("VariableEditor", "Use as as both Model Variable and Indicator", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setToolTip(QtGui.QApplication.translate("VariableEditor", "Where the variable definition derives from. \n"
"An \"expression\" uses the Tekoa domain-specific language, \n"
"\"python class\" is a path to a variable defined in a python module (e.g. urbansim.gridcell.population), \n"
"and \"primary attribute\" refers to a primary attribute of the given dataset. ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("VariableEditor", "Variable type:", None, QtGui.QApplication.UnicodeUTF8))
        self.cboVarType.setItemText(0, QtGui.QApplication.translate("VariableEditor", "expression", None, QtGui.QApplication.UnicodeUTF8))
        self.cboVarType.setItemText(1, QtGui.QApplication.translate("VariableEditor", "primary attribute", None, QtGui.QApplication.UnicodeUTF8))
        self.cboVarType.setItemText(2, QtGui.QApplication.translate("VariableEditor", "Python class", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCheckSyntax.setToolTip(QtGui.QApplication.translate("VariableEditor", "Verify that the syntax of variable definition parses correctly.", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCheckSyntax.setText(QtGui.QApplication.translate("VariableEditor", "Check syntax", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCheckData.setToolTip(QtGui.QApplication.translate("VariableEditor", "Verify that the variable can be computed against the baseyear data for this project.", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCheckData.setText(QtGui.QApplication.translate("VariableEditor", "Check against data", None, QtGui.QApplication.UnicodeUTF8))

