# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\Christoffer Klang\My Documents\workspace\opus_trunk\opus_gui\models_manager\views\submodel_editor.ui'
#
# Created: Mon Jun 08 14:59:52 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SubModelEditor(object):
    def setupUi(self, SubModelEditor):
        SubModelEditor.setObjectName("SubModelEditor")
        SubModelEditor.resize(728, 498)
        SubModelEditor.setModal(True)
        self.verticalLayout_2 = QtGui.QVBoxLayout(SubModelEditor)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.group_submodel_info = QtGui.QGroupBox(SubModelEditor)
        self.group_submodel_info.setObjectName("group_submodel_info")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.group_submodel_info)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtGui.QLabel(self.group_submodel_info)
        self.label.setMinimumSize(QtCore.QSize(100, 0))
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.le_name = QtGui.QLineEdit(self.group_submodel_info)
        self.le_name.setObjectName("le_name")
        self.horizontalLayout_3.addWidget(self.le_name)
        self.label_4 = QtGui.QLabel(self.group_submodel_info)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.spin_id = QtGui.QSpinBox(self.group_submodel_info)
        self.spin_id.setWrapping(False)
        self.spin_id.setFrame(False)
        self.spin_id.setButtonSymbols(QtGui.QAbstractSpinBox.PlusMinus)
        self.spin_id.setMinimum(-10000)
        self.spin_id.setMaximum(10000)
        self.spin_id.setProperty("value", QtCore.QVariant(-2))
        self.spin_id.setObjectName("spin_id")
        self.horizontalLayout_3.addWidget(self.spin_id)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.frame_name_warning = QtGui.QFrame(self.group_submodel_info)
        self.frame_name_warning.setFrameShape(QtGui.QFrame.Panel)
        self.frame_name_warning.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_name_warning.setObjectName("frame_name_warning")
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame_name_warning)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lbl_name_warning = QtGui.QLabel(self.frame_name_warning)
        self.lbl_name_warning.setObjectName("lbl_name_warning")
        self.horizontalLayout.addWidget(self.lbl_name_warning)
        self.verticalLayout_3.addWidget(self.frame_name_warning)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtGui.QLabel(self.group_submodel_info)
        self.label_2.setMinimumSize(QtCore.QSize(100, 0))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.le_description = QtGui.QLineEdit(self.group_submodel_info)
        self.le_description.setObjectName("le_description")
        self.horizontalLayout_4.addWidget(self.le_description)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addWidget(self.group_submodel_info)
        self.tab_widget = QtGui.QTabWidget(SubModelEditor)
        self.tab_widget.setAutoFillBackground(True)
        self.tab_widget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tab_widget.setObjectName("tab_widget")
        self.tab_variable_selector = QtGui.QWidget()
        self.tab_variable_selector.setAutoFillBackground(True)
        self.tab_variable_selector.setObjectName("tab_variable_selector")
        self.verticalLayout = QtGui.QVBoxLayout(self.tab_variable_selector)
        self.verticalLayout.setObjectName("verticalLayout")
        self.split_struct_variables = QtGui.QSplitter(self.tab_variable_selector)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.split_struct_variables.sizePolicy().hasHeightForWidth())
        self.split_struct_variables.setSizePolicy(sizePolicy)
        self.split_struct_variables.setOrientation(QtCore.Qt.Horizontal)
        self.split_struct_variables.setObjectName("split_struct_variables")
        self.tree_structure_selector = QtGui.QTreeWidget(self.split_struct_variables)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tree_structure_selector.sizePolicy().hasHeightForWidth())
        self.tree_structure_selector.setSizePolicy(sizePolicy)
        self.tree_structure_selector.setObjectName("tree_structure_selector")
        self.table_selected_variables = QtGui.QTableView(self.split_struct_variables)
        self.table_selected_variables.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.table_selected_variables.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table_selected_variables.setShowGrid(True)
        self.table_selected_variables.setWordWrap(False)
        self.table_selected_variables.setObjectName("table_selected_variables")
        self.verticalLayout.addWidget(self.split_struct_variables)
        self.frame_selection_buttons = QtGui.QFrame(self.tab_variable_selector)
        self.frame_selection_buttons.setObjectName("frame_selection_buttons")
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.frame_selection_buttons)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pb_add_variable = QtGui.QPushButton(self.frame_selection_buttons)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Images/Images/arrow_right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pb_add_variable.setIcon(icon)
        self.pb_add_variable.setObjectName("pb_add_variable")
        self.horizontalLayout_5.addWidget(self.pb_add_variable)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.pb_remove_variable = QtGui.QPushButton(self.frame_selection_buttons)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Images/Images/arrow_left_red.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pb_remove_variable.setIcon(icon1)
        self.pb_remove_variable.setObjectName("pb_remove_variable")
        self.horizontalLayout_5.addWidget(self.pb_remove_variable)
        self.verticalLayout.addWidget(self.frame_selection_buttons)
        self.tab_widget.addTab(self.tab_variable_selector, "")
        self.tab_structure_editor = QtGui.QWidget()
        self.tab_structure_editor.setAutoFillBackground(False)
        self.tab_structure_editor.setObjectName("tab_structure_editor")
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.tab_structure_editor)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.frame_structure_buttons = QtGui.QFrame(self.tab_structure_editor)
        self.frame_structure_buttons.setAutoFillBackground(False)
        self.frame_structure_buttons.setObjectName("frame_structure_buttons")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.frame_structure_buttons)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.pb_create_nest = QtGui.QPushButton(self.frame_structure_buttons)
        self.pb_create_nest.setObjectName("pb_create_nest")
        self.verticalLayout_5.addWidget(self.pb_create_nest)
        self.pb_create_equation = QtGui.QPushButton(self.frame_structure_buttons)
        self.pb_create_equation.setObjectName("pb_create_equation")
        self.verticalLayout_5.addWidget(self.pb_create_equation)
        spacerItem1 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_5.addItem(spacerItem1)
        self.pb_delete_struct = QtGui.QPushButton(self.frame_structure_buttons)
        self.pb_delete_struct.setObjectName("pb_delete_struct")
        self.verticalLayout_5.addWidget(self.pb_delete_struct)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem2)
        self.pb_update_model_structure = QtGui.QPushButton(self.frame_structure_buttons)
        self.pb_update_model_structure.setObjectName("pb_update_model_structure")
        self.verticalLayout_5.addWidget(self.pb_update_model_structure)
        self.horizontalLayout_6.addWidget(self.frame_structure_buttons)
        self.tree_structure_editor = SubmodelStructureEditorTree(self.tab_structure_editor)
        self.tree_structure_editor.setObjectName("tree_structure_editor")
        self.horizontalLayout_6.addWidget(self.tree_structure_editor)
        self.tab_widget.addTab(self.tab_structure_editor, "")
        self.verticalLayout_2.addWidget(self.tab_widget)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pb_help_on = QtGui.QPushButton(SubModelEditor)
        self.pb_help_on.setObjectName("pb_help_on")
        self.horizontalLayout_2.addWidget(self.pb_help_on)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.buttonBox = QtGui.QDialogButtonBox(SubModelEditor)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(SubModelEditor)
        self.tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SubModelEditor)

    def retranslateUi(self, SubModelEditor):
        SubModelEditor.setWindowTitle(QtGui.QApplication.translate("SubModelEditor", "Submodel Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.group_submodel_info.setTitle(QtGui.QApplication.translate("SubModelEditor", "Submodel Information", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SubModelEditor", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.le_name.setToolTip(QtGui.QApplication.translate("SubModelEditor", "The name of the submodel", None, QtGui.QApplication.UnicodeUTF8))
        self.le_name.setWhatsThis(QtGui.QApplication.translate("SubModelEditor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">The name of the submodel.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">This is primarliy used to make it easier for users to distinguish between submodels when working with them in the GUI.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Note that inheritance between Opus Projects always works on the name of the submodel, not the ID.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("SubModelEditor", "ID", None, QtGui.QApplication.UnicodeUTF8))
        self.spin_id.setToolTip(QtGui.QApplication.translate("SubModelEditor", "The submodel ID", None, QtGui.QApplication.UnicodeUTF8))
        self.spin_id.setWhatsThis(QtGui.QApplication.translate("SubModelEditor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">The submodel ID.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">The value -2 is special and can used when the ID does not matter.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Please refer to the Opus Manual for a full explanation of how the modeling systems handles submodels.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_name_warning.setText(QtGui.QApplication.translate("SubModelEditor", "<name warning here>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("SubModelEditor", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.le_description.setToolTip(QtGui.QApplication.translate("SubModelEditor", "A brief description of the submodel (optional)", None, QtGui.QApplication.UnicodeUTF8))
        self.le_description.setWhatsThis(QtGui.QApplication.translate("SubModelEditor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Can be used to give a brief description of the submodel.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tree_structure_selector.setWhatsThis(QtGui.QApplication.translate("SubModelEditor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Tahoma\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Select which equation (showed in <span style=\" font-weight:600;\">bold</span>) to assign variables to.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">The hiearchical structure, as well as the names of these nodes can be edited </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">under the tab \"Edit Nests and Equations\"</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tree_structure_selector.headerItem().setText(0, QtGui.QApplication.translate("SubModelEditor", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.tree_structure_selector.headerItem().setText(1, QtGui.QApplication.translate("SubModelEditor", "ID", None, QtGui.QApplication.UnicodeUTF8))
        self.table_selected_variables.setWhatsThis(QtGui.QApplication.translate("SubModelEditor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Tahoma\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">The list of currently selected variables.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">The variable can be exluded from the set of variables passed into the modeling system by checking the checbox in column \"ignore\" (think of it as \"commenting out\" the variable).</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">The variable name is showing in <span style=\" font-weight:600;\">bold</span> (unless the \"ignore\" checkbox is selected).</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">If a coefficient name as not been given, it defaults to the same name as the variable, and is then shown in <span style=\" color:#4f4f4f;\">gray</span><span style=\" color:#000000;\">. On the other hand, if a coefficient name has been given, then it shows up in black </span><span style=\" font-weight:600; color:#000000;\">bold.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Please refer to the Opus Manual for a description of \"starting values\" and \"fixed\" (described under Choice Models)</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">The last column shows the variable definition. Note that variables are defined by both the dataset and the name. The displayed definition <span style=\" font-style:italic;\">might</span> be for another variable than what is selected by the modeling system at run time. </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">This can only happen if you have multiple variables with the same name (but different datasets) in your expression library.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_add_variable.setToolTip(QtGui.QApplication.translate("SubModelEditor", "Add a variable from the expression librarry to the current list", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_add_variable.setText(QtGui.QApplication.translate("SubModelEditor", "Add variable from library...", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_remove_variable.setToolTip(QtGui.QApplication.translate("SubModelEditor", "Remove the selected variable", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_remove_variable.setWhatsThis(QtGui.QApplication.translate("SubModelEditor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Remove the variable.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Note that any extra information such as starting values or coefficient names are lost when removing the variable. To temporarly disable it you can click the \"ignore\" checkbox.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_remove_variable.setText(QtGui.QApplication.translate("SubModelEditor", "Remove selected variable", None, QtGui.QApplication.UnicodeUTF8))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_variable_selector), QtGui.QApplication.translate("SubModelEditor", "Variables", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_create_nest.setWhatsThis(QtGui.QApplication.translate("SubModelEditor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Creates a new &lt;nest&gt; node in the table to the right.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_create_nest.setText(QtGui.QApplication.translate("SubModelEditor", "Create Nest", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_create_equation.setWhatsThis(QtGui.QApplication.translate("SubModelEditor", "Create a new <equation>", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_create_equation.setText(QtGui.QApplication.translate("SubModelEditor", "Create Equation", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_delete_struct.setWhatsThis(QtGui.QApplication.translate("SubModelEditor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Delete the selected nest or equation.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Note that variable lists associated with a deleted equation will be cleared.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_delete_struct.setText(QtGui.QApplication.translate("SubModelEditor", "Delete Selected", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_update_model_structure.setWhatsThis(QtGui.QApplication.translate("SubModelEditor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">This functionality </span><span style=\" font-size:8pt; font-weight:600;\">only</span><span style=\" font-size:8pt;\"> applies to Nested Logit Models.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Update the model\'s structure with the information from this dialog.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">This must be done before the model is evaluated or run as part of a simulation. </p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_update_model_structure.setText(QtGui.QApplication.translate("SubModelEditor", "Update model structure", None, QtGui.QApplication.UnicodeUTF8))
        self.tree_structure_editor.setWhatsThis(QtGui.QApplication.translate("SubModelEditor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Tahoma\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Double click on the ID, name or number of samples to edit it\'s value.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Note that number of samples only applies to &lt;nest&gt;.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">To construct the hierarchical structure: drag the <span style=\" font-weight:600;\">equation </span>and drop it on a &lt;nest&gt;. You can drag and drop &lt;nest&gt;:s onto each other to construct nested structures with multiple levels.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">The new structure is automatically updated under the tab \"Assign Variables\".</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tree_structure_editor.headerItem().setText(0, QtGui.QApplication.translate("SubModelEditor", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.tree_structure_editor.headerItem().setText(1, QtGui.QApplication.translate("SubModelEditor", "ID", None, QtGui.QApplication.UnicodeUTF8))
        self.tree_structure_editor.headerItem().setText(2, QtGui.QApplication.translate("SubModelEditor", "# of samples", None, QtGui.QApplication.UnicodeUTF8))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_structure_editor), QtGui.QApplication.translate("SubModelEditor", "Nests and Equations", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_help_on.setToolTip(QtGui.QApplication.translate("SubModelEditor", "Click on this button and then click on any item you want a description for.", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_help_on.setText(QtGui.QApplication.translate("SubModelEditor", "Help on...", None, QtGui.QApplication.UnicodeUTF8))

from opus_gui.models_manager.controllers.submodel_structure_editor_tree import SubmodelStructureEditorTree
