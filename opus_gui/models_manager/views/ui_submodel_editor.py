# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\Christoffer Klang\My Documents\workspace\opus_trunk\opus_gui\models_manager\views\submodel_editor.ui'
#
# Created: Fri Jun 12 10:52:52 2009
#      by: PyQt5 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_SubModelEditor(object):
    def setupUi(self, SubModelEditor):
        SubModelEditor.setObjectName("SubModelEditor")
        SubModelEditor.resize(716, 520)
        SubModelEditor.setModal(True)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(SubModelEditor)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.group_submodel_info = QtWidgets.QGroupBox(SubModelEditor)
        self.group_submodel_info.setObjectName("group_submodel_info")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.group_submodel_info)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.group_submodel_info)
        self.label.setMinimumSize(QtCore.QSize(100, 0))
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.le_name = QtWidgets.QLineEdit(self.group_submodel_info)
        self.le_name.setObjectName("le_name")
        self.horizontalLayout_3.addWidget(self.le_name)
        self.label_4 = QtWidgets.QLabel(self.group_submodel_info)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.spin_id = QtWidgets.QSpinBox(self.group_submodel_info)
        self.spin_id.setWrapping(False)
        self.spin_id.setFrame(False)
        self.spin_id.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.spin_id.setMinimum(-10000)
        self.spin_id.setMaximum(10000)
        self.spin_id.setProperty("value", QtCore.QVariant(-2))
        self.spin_id.setObjectName("spin_id")
        self.horizontalLayout_3.addWidget(self.spin_id)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.frame_name_warning = QtWidgets.QFrame(self.group_submodel_info)
        self.frame_name_warning.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame_name_warning.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_name_warning.setObjectName("frame_name_warning")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_name_warning)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lbl_name_warning = QtWidgets.QLabel(self.frame_name_warning)
        self.lbl_name_warning.setObjectName("lbl_name_warning")
        self.horizontalLayout.addWidget(self.lbl_name_warning)
        self.verticalLayout_3.addWidget(self.frame_name_warning)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.group_submodel_info)
        self.label_2.setMinimumSize(QtCore.QSize(100, 0))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.le_description = QtWidgets.QLineEdit(self.group_submodel_info)
        self.le_description.setObjectName("le_description")
        self.horizontalLayout_4.addWidget(self.le_description)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addWidget(self.group_submodel_info)
        self.tab_widget = QtWidgets.QTabWidget(SubModelEditor)
        self.tab_widget.setAutoFillBackground(True)
        self.tab_widget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tab_widget.setObjectName("tab_widget")
        self.tab_variable_selector = QtWidgets.QWidget()
        self.tab_variable_selector.setAutoFillBackground(False)
        self.tab_variable_selector.setObjectName("tab_variable_selector")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_variable_selector)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.split_struct_variables = QtWidgets.QSplitter(self.tab_variable_selector)
        self.split_struct_variables.setOrientation(QtCore.Qt.Horizontal)
        self.split_struct_variables.setObjectName("split_struct_variables")
        self.stack_struct_picker = QtWidgets.QStackedWidget(self.split_struct_variables)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stack_struct_picker.sizePolicy().hasHeightForWidth())
        self.stack_struct_picker.setSizePolicy(sizePolicy)
        self.stack_struct_picker.setObjectName("stack_struct_picker")
        self.picker = QtWidgets.QWidget()
        self.picker.setObjectName("picker")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.picker)
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_3 = QtWidgets.QLabel(self.picker)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_8.addWidget(self.label_3)
        self.cbo_dataset_filter = QtWidgets.QComboBox(self.picker)
        self.cbo_dataset_filter.setObjectName("cbo_dataset_filter")
        self.horizontalLayout_8.addWidget(self.cbo_dataset_filter)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.lst_available_variables = QtWidgets.QListWidget(self.picker)
        self.lst_available_variables.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lst_available_variables.setObjectName("lst_available_variables")
        self.verticalLayout_4.addWidget(self.lst_available_variables)
        self.pb_add_variable = QtWidgets.QPushButton(self.picker)
        self.pb_add_variable.setObjectName("pb_add_variable")
        self.verticalLayout_4.addWidget(self.pb_add_variable)
        self.stack_struct_picker.addWidget(self.picker)
        self.structure = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.structure.sizePolicy().hasHeightForWidth())
        self.structure.setSizePolicy(sizePolicy)
        self.structure.setObjectName("structure")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.structure)
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_7.setMargin(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.tree_structure_selector = QtWidgets.QTreeWidget(self.structure)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tree_structure_selector.sizePolicy().hasHeightForWidth())
        self.tree_structure_selector.setSizePolicy(sizePolicy)
        self.tree_structure_selector.setObjectName("tree_structure_selector")
        self.verticalLayout_7.addWidget(self.tree_structure_selector)
        self.stack_struct_picker.addWidget(self.structure)
        self.frame = QtWidgets.QFrame(self.split_struct_variables)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.table_selected_variables = QtWidgets.QTableView(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_selected_variables.sizePolicy().hasHeightForWidth())
        self.table_selected_variables.setSizePolicy(sizePolicy)
        self.table_selected_variables.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.table_selected_variables.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_selected_variables.setShowGrid(True)
        self.table_selected_variables.setWordWrap(False)
        self.table_selected_variables.setObjectName("table_selected_variables")
        self.verticalLayout.addWidget(self.table_selected_variables)
        self.pb_remove_variable = QtWidgets.QPushButton(self.frame)
        self.pb_remove_variable.setObjectName("pb_remove_variable")
        self.verticalLayout.addWidget(self.pb_remove_variable)
        self.verticalLayout_6.addWidget(self.split_struct_variables)
        self.frame_selection_buttons = QtWidgets.QFrame(self.tab_variable_selector)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_selection_buttons.sizePolicy().hasHeightForWidth())
        self.frame_selection_buttons.setSizePolicy(sizePolicy)
        self.frame_selection_buttons.setObjectName("frame_selection_buttons")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_selection_buttons)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pb_show_picker = QtWidgets.QPushButton(self.frame_selection_buttons)
        self.pb_show_picker.setCheckable(True)
        self.pb_show_picker.setObjectName("pb_show_picker")
        self.horizontalLayout_5.addWidget(self.pb_show_picker)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.cb_show_advanced_parameters = QtWidgets.QCheckBox(self.frame_selection_buttons)
        self.cb_show_advanced_parameters.setObjectName("cb_show_advanced_parameters")
        self.horizontalLayout_5.addWidget(self.cb_show_advanced_parameters)
        self.verticalLayout_6.addWidget(self.frame_selection_buttons)
        self.tab_widget.addTab(self.tab_variable_selector, "")
        self.tab_structure_editor = QtWidgets.QWidget()
        self.tab_structure_editor.setAutoFillBackground(False)
        self.tab_structure_editor.setObjectName("tab_structure_editor")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.tab_structure_editor)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.frame_structure_buttons = QtWidgets.QFrame(self.tab_structure_editor)
        self.frame_structure_buttons.setAutoFillBackground(False)
        self.frame_structure_buttons.setObjectName("frame_structure_buttons")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_structure_buttons)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.pb_create_nest = QtWidgets.QPushButton(self.frame_structure_buttons)
        self.pb_create_nest.setObjectName("pb_create_nest")
        self.verticalLayout_5.addWidget(self.pb_create_nest)
        self.pb_create_equation = QtWidgets.QPushButton(self.frame_structure_buttons)
        self.pb_create_equation.setObjectName("pb_create_equation")
        self.verticalLayout_5.addWidget(self.pb_create_equation)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_5.addItem(spacerItem1)
        self.pb_delete_struct = QtWidgets.QPushButton(self.frame_structure_buttons)
        self.pb_delete_struct.setObjectName("pb_delete_struct")
        self.verticalLayout_5.addWidget(self.pb_delete_struct)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem2)
        self.pb_update_model_structure = QtWidgets.QPushButton(self.frame_structure_buttons)
        self.pb_update_model_structure.setObjectName("pb_update_model_structure")
        self.verticalLayout_5.addWidget(self.pb_update_model_structure)
        self.horizontalLayout_6.addWidget(self.frame_structure_buttons)
        self.tree_structure_editor = SubmodelStructureEditorTree(self.tab_structure_editor)
        self.tree_structure_editor.setObjectName("tree_structure_editor")
        self.horizontalLayout_6.addWidget(self.tree_structure_editor)
        self.tab_widget.addTab(self.tab_structure_editor, "")
        self.verticalLayout_2.addWidget(self.tab_widget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pb_help_on = QtWidgets.QPushButton(SubModelEditor)
        self.pb_help_on.setObjectName("pb_help_on")
        self.horizontalLayout_2.addWidget(self.pb_help_on)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.buttonBox = QtWidgets.QDialogButtonBox(SubModelEditor)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(SubModelEditor)
        self.tab_widget.setCurrentIndex(0)
        self.stack_struct_picker.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SubModelEditor)

    def retranslateUi(self, SubModelEditor):
        SubModelEditor.setWindowTitle(QtWidgets.QApplication.translate("SubModelEditor", "Submodel Editor", None, QtWidgets.QApplication.UnicodeUTF8))
        self.group_submodel_info.setTitle(QtWidgets.QApplication.translate("SubModelEditor", "Submodel Information", None, QtWidgets.QApplication.UnicodeUTF8))
        self.label.setText(QtWidgets.QApplication.translate("SubModelEditor", "Name", None, QtWidgets.QApplication.UnicodeUTF8))
        self.le_name.setToolTip(QtWidgets.QApplication.translate("SubModelEditor", "The name of the submodel", None, QtWidgets.QApplication.UnicodeUTF8))
        self.le_name.setWhatsThis(QtWidgets.QApplication.translate("SubModelEditor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">The name of the submodel.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">This is primarliy used to make it easier for users to distinguish between submodels when working with them in the GUI.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Note that inheritance between Opus Projects always works on the name of the submodel, not the ID.</p></body></html>", None, QtWidgets.QApplication.UnicodeUTF8))
        self.label_4.setText(QtWidgets.QApplication.translate("SubModelEditor", "ID", None, QtWidgets.QApplication.UnicodeUTF8))
        self.spin_id.setToolTip(QtWidgets.QApplication.translate("SubModelEditor", "The submodel ID", None, QtWidgets.QApplication.UnicodeUTF8))
        self.spin_id.setWhatsThis(QtWidgets.QApplication.translate("SubModelEditor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">The submodel ID.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">The value -2 is special and can used when the ID does not matter.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Please refer to the Opus Manual for a full explanation of how the modeling systems handles submodels.</p></body></html>", None, QtWidgets.QApplication.UnicodeUTF8))
        self.lbl_name_warning.setText(QtWidgets.QApplication.translate("SubModelEditor", "<name warning here>", None, QtWidgets.QApplication.UnicodeUTF8))
        self.label_2.setText(QtWidgets.QApplication.translate("SubModelEditor", "Description", None, QtWidgets.QApplication.UnicodeUTF8))
        self.le_description.setToolTip(QtWidgets.QApplication.translate("SubModelEditor", "A brief description of the submodel (optional)", None, QtWidgets.QApplication.UnicodeUTF8))
        self.le_description.setWhatsThis(QtWidgets.QApplication.translate("SubModelEditor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Can be used to give a brief description of the submodel.</span></p></body></html>", None, QtWidgets.QApplication.UnicodeUTF8))
        self.label_3.setText(QtWidgets.QApplication.translate("SubModelEditor", "Show variables from:", None, QtWidgets.QApplication.UnicodeUTF8))
        self.cbo_dataset_filter.setWhatsThis(QtWidgets.QApplication.translate("SubModelEditor", "Filter what variables to display for adding by dataset.\n"
"The list of variables is not filtered if [All datasets] is selected.", None, QtWidgets.QApplication.UnicodeUTF8))
        self.lst_available_variables.setWhatsThis(QtWidgets.QApplication.translate("SubModelEditor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Tahoma\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The list of available model variables that can be added to the the right side list.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This list only shows variables that are not already selected and that belong the selected dataset.</p></body></html>", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_add_variable.setWhatsThis(QtWidgets.QApplication.translate("SubModelEditor", "Add the selected variable(s) to the right side list.", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_add_variable.setText(QtWidgets.QApplication.translate("SubModelEditor", "Add >>", None, QtWidgets.QApplication.UnicodeUTF8))
        self.tree_structure_selector.setWhatsThis(QtWidgets.QApplication.translate("SubModelEditor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Tahoma\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Select which equation (showed in <span style=\" font-weight:600;\">bold</span>) to assign variables to.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">The hiearchical structure, as well as the names of these nodes can be edited </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">under the tab \"Edit Nests and Equations\"</p></body></html>", None, QtWidgets.QApplication.UnicodeUTF8))
        self.tree_structure_selector.headerItem().setText(0, QtWidgets.QApplication.translate("SubModelEditor", "Name", None, QtWidgets.QApplication.UnicodeUTF8))
        self.tree_structure_selector.headerItem().setText(1, QtWidgets.QApplication.translate("SubModelEditor", "ID", None, QtWidgets.QApplication.UnicodeUTF8))
        self.table_selected_variables.setWhatsThis(QtWidgets.QApplication.translate("SubModelEditor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
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
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">This can only happen if you have multiple variables with the same name (but different datasets) in your expression library.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">You can remove a variable from the list by <span style=\" font-weight:600;\">right clicking </span>and selecting<span style=\" font-weight:600;\"> \"Remove &lt;name&gt;\" </span>(the name of the variable under the cursor will be shown instead of &lt;name&gt;). To remove more than one variable: click the Add/Remove variables button, select which variables you want to delete and click <span style=\" font-weight:600;\">\"&lt;&lt; Remove selected\"</span></p></body></html>", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_remove_variable.setToolTip(QtWidgets.QApplication.translate("SubModelEditor", "Remove the selected variable", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_remove_variable.setWhatsThis(QtWidgets.QApplication.translate("SubModelEditor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Remove the selected variables from the equation / submodel.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Note that any extra information such as starting values or coefficient names are lost when removing the variable. To temporarly disable a variable you can click the \"<span style=\" font-weight:600;\">ignore</span>\" checkbox on the far left side of the list.</p></body></html>", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_remove_variable.setText(QtWidgets.QApplication.translate("SubModelEditor", "<< Remove selected", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_show_picker.setToolTip(QtWidgets.QApplication.translate("SubModelEditor", "Add a variable from the expression librarry to the current list", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_show_picker.setWhatsThis(QtWidgets.QApplication.translate("SubModelEditor", "Toggles the list of available variable models that can be added to the submodel.", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_show_picker.setText(QtWidgets.QApplication.translate("SubModelEditor", "Add/Remove variables...", None, QtWidgets.QApplication.UnicodeUTF8))
        self.cb_show_advanced_parameters.setText(QtWidgets.QApplication.translate("SubModelEditor", "Show advanced variable parameters", None, QtWidgets.QApplication.UnicodeUTF8))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_variable_selector), QtWidgets.QApplication.translate("SubModelEditor", "Variables", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_create_nest.setWhatsThis(QtWidgets.QApplication.translate("SubModelEditor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Creates a new &lt;nest&gt; node in the table to the right.</span></p></body></html>", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_create_nest.setText(QtWidgets.QApplication.translate("SubModelEditor", "Create Nest", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_create_equation.setWhatsThis(QtWidgets.QApplication.translate("SubModelEditor", "Create a new <equation>", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_create_equation.setText(QtWidgets.QApplication.translate("SubModelEditor", "Create Equation", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_delete_struct.setWhatsThis(QtWidgets.QApplication.translate("SubModelEditor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Delete the selected nest or equation.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Note that variable lists associated with a deleted equation will be cleared.</p></body></html>", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_delete_struct.setText(QtWidgets.QApplication.translate("SubModelEditor", "Delete Selected", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_update_model_structure.setWhatsThis(QtWidgets.QApplication.translate("SubModelEditor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">This functionality </span><span style=\" font-size:8pt; font-weight:600;\">only</span><span style=\" font-size:8pt;\"> applies to Nested Logit Models.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Update the model\'s structure with the information from this dialog.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">This must be done before the model is evaluated or run as part of a simulation. </p></body></html>", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_update_model_structure.setText(QtWidgets.QApplication.translate("SubModelEditor", "Update model structure", None, QtWidgets.QApplication.UnicodeUTF8))
        self.tree_structure_editor.setWhatsThis(QtWidgets.QApplication.translate("SubModelEditor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Tahoma\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Double click on the ID, name or number of samples to edit it\'s value.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Note that number of samples only applies to &lt;nest&gt;.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">To construct the hierarchical structure: drag the <span style=\" font-weight:600;\">equation </span>and drop it on a &lt;nest&gt;. You can drag and drop &lt;nest&gt;:s onto each other to construct nested structures with multiple levels.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">The new structure is automatically updated under the tab \"Assign Variables\".</p></body></html>", None, QtWidgets.QApplication.UnicodeUTF8))
        self.tree_structure_editor.headerItem().setText(0, QtWidgets.QApplication.translate("SubModelEditor", "Name", None, QtWidgets.QApplication.UnicodeUTF8))
        self.tree_structure_editor.headerItem().setText(1, QtWidgets.QApplication.translate("SubModelEditor", "ID", None, QtWidgets.QApplication.UnicodeUTF8))
        self.tree_structure_editor.headerItem().setText(2, QtWidgets.QApplication.translate("SubModelEditor", "# of samples", None, QtWidgets.QApplication.UnicodeUTF8))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_structure_editor), QtWidgets.QApplication.translate("SubModelEditor", "Nests and Equations", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_help_on.setToolTip(QtWidgets.QApplication.translate("SubModelEditor", "Click on this button and then click on any item you want a description for.", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_help_on.setText(QtWidgets.QApplication.translate("SubModelEditor", "Help on...", None, QtWidgets.QApplication.UnicodeUTF8))

from opus_gui.models_manager.controllers.submodel_structure_editor_tree import SubmodelStructureEditorTree
