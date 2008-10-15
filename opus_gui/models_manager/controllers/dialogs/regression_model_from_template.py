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

from PyQt4.QtCore import QString, QObject, SIGNAL, \
                         Qt, QTimer, QModelIndex
from PyQt4.QtGui import QMessageBox, QComboBox, QGridLayout, \
                        QTextEdit, QTabWidget, QWidget, QPushButton, \
                        QGroupBox, QVBoxLayout, QIcon, QLabel, QDialog
from PyQt4.QtXml import QDomText

from opus_gui.models_manager.controllers.dialogs.model_from_template_dialog_base import ModelFromTemplateDialogBase

#TODO: Rodo this one to have the same code formatting as the newer dialogs

class RegressionModelFromTemplateDialog(ModelFromTemplateDialogBase):
    def __init__(self, main_window, model_template_node, template_index, template_model):
        ModelFromTemplateDialogBase.__init__(self, main_window, model_template_node, \
                                             template_index, template_model)

        # setup additional ui that's specfic for this model template
        self.setup_regression_ui()
        self._setup_co_dataset_name()
        self._setup_model_variables()

    def setup_regression_ui(self):
        self.cboDataset = QComboBox()
        self.connect(self.cboDataset, SIGNAL('currentIndexChanged(int)'), self._refresh_model_variables)

        self.cboDependentVariable = QComboBox()
        
        self.add_widget_pair(QLabel('Dataset'), self.cboDataset)
        self.add_widget_pair(QLabel('Dependent variable'), self.cboDependentVariable)
        
    def _setup_model_variables(self):
        '''Collect the model variables and populate the combobox'''        
        model_variables = self.xml_helper.get_available_model_variables(attributes = ['dataset'])
        self.model_variables = {}
        
        #TODO: this does not return any model_vars for any data sets
        # except gridcell?
        
        # self.cboDependentVariable.clear()
        for indicator in model_variables:            
            name = indicator['name']
            dataset = indicator['dataset']
            self.model_variables[(dataset, name)] = indicator
            
            if self.cboDataset.currentText() == dataset:
                self.cboDependentVariable.addItem(QString(name))                

    def _setup_co_dataset_name(self):
        '''collect avaiable datasets and populate the combobox'''
        available_datasets = self.xml_helper.get_available_datasets()

        for dataset in available_datasets:
            self.cboDataset.addItem(QString(dataset))

    def _refresh_model_variables(self, index):
        self._setup_model_variables()

    def setup_node(self):
        
        model_name = self.get_model_xml_name()
        self.set_model_name(model_name)
        
        spc_tbl_name = model_name + '_specification'
        coef_tbl_name = model_name + '_coefficients_table'
        dataset = self.cboDataset.currentText()
        dep_var = self.cboDependentVariable.currentText()

        self.set_structure_element_to_value('run/dataset', dataset)
        self.set_structure_element_to_value('prepare_for_run/specification_table', spc_tbl_name)
        self.set_structure_element_to_value('prepare_for_run/coefficients_table', coef_tbl_name)
        self.set_structure_element_to_value('estimate/dataset', dataset)
        self.set_structure_element_to_value('estimate/dependent_variable', dep_var)
        self.set_structure_element_to_value('prepare_for_estimate/specification_table', spc_tbl_name)

