# UrbanSim software. Copyright (C) 2005-2008 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

from PyQt4.QtGui import QLineEdit, QComboBox, QLabel

from opus_gui.models_manager.controllers.dialogs.model_from_template_dialog_base import \
    ModelFromTemplateDialogBase

class SimpleModelFromTemplateDialog(ModelFromTemplateDialogBase):
    def __init__(self, main_window, model_template_node, model_manager_model):
        ModelFromTemplateDialogBase.__init__(self, main_window, 
                                             model_template_node,
                                             model_manager_model)
        
        self.cboDataset = QComboBox()
        self.leExpression = QLineEdit('expression')
        self.leOutcome = QLineEdit('outcome variable')
        
        self.add_widget_pair(QLabel('Dataset'), self.cboDataset)
        self.add_widget_pair(QLabel('expression'), self.leExpression)
        self.add_widget_pair(QLabel('Outcome variable'), self.leOutcome)
        
        self._setup_co_dataset_name()

    def _setup_co_dataset_name(self):
        '''collect avaiable datasets and populate the combobox'''
        available_datasets = self.xml_helper.get_available_datasets()
        self.cboDataset.clear()

        for dataset in available_datasets:
            self.cboDataset.addItem(dataset)

    def setup_node(self):
        self.set_model_name()
        self.set_structure_element_to_value('run/dataset', self.cboDataset.currentText())
        self.set_structure_element_to_value('run/expression', self.leExpression.text())
        self.set_structure_element_to_value('run/outcome_attribute', self.leOutcome.text())
        