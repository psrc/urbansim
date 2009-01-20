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

from PyQt4.QtCore import SIGNAL

from PyQt4.QtGui import QLabel, QComboBox

from opus_gui.models_manager.controllers.dialogs.model_from_template_dialog_base import ModelFromTemplateDialogBase
from opus_gui.general_manager.general_manager import \
    get_available_dataset_names, get_variable_nodes_per_dataset

#TODO: Redo this one to have the same code formatting as the newer dialogs

class RegressionModelFromTemplateDialog(ModelFromTemplateDialogBase):

    ''' Dialog for instantiating a Regression Model '''

    def __init__(self, model_node, project = None, callback = None,
                 parent_widget = None):

        ModelFromTemplateDialogBase.__init__(self, model_node, project,
                                             callback, parent_widget)

        self.cboDataset = QComboBox()
        self.connect(self.cboDataset, SIGNAL('currentIndexChanged(int)'),
                     self._setup_model_variables)
        self.cboDependentVariable = QComboBox()

        self._add_widget_pair(QLabel('Dataset'), self.cboDataset)
        self._add_widget_pair(QLabel('Dependent variable'),
                             self.cboDependentVariable)

        # setup combo boxes
        for dataset_name in get_available_dataset_names(project):
            self.cboDataset.addItem(dataset_name)

        self._setup_model_variables()

    def _setup_model_variables(self, index = None):
        '''
        Filter the list of available variables based on the currently
        selected dataset.
        '''
        self.cboDependentVariable.clear()
        variable_nodes = get_variable_nodes_per_dataset(self.project)

        # Filter on the selected dataset
        selected_dataset_name = str(self.cboDataset.currentText())
        if not selected_dataset_name in variable_nodes:
            variable_nodes = []
        else:
            variable_nodes = variable_nodes[selected_dataset_name]

        for var_node in variable_nodes:
            if not var_node.get('use') in ('model variable', 'both'):
                continue
            var_name = var_node.tag
            self.cboDependentVariable.addItem(var_name)

        self.cboDependentVariable.setEnabled(len(variable_nodes) > 0)

    def setup_node(self):
        model_name = self._get_xml_friendly_name()
        self.model_node.tag = model_name

        spc_tbl_name = model_name + '_specification'
        coef_tbl_name = model_name + '_coefficients'
        dataset = self.cboDataset.currentText()
        dep_var = self.cboDependentVariable.currentText()

        path_value_mappings = {
        'run/dataset': dataset,
        'prepare_for_run/specification_table': spc_tbl_name,
        'prepare_for_run/coefficients_table': coef_tbl_name,
        'estimate/dataset': dataset,
        'estimate/dependent_variable': dep_var,
        'prepare_for_estimate/specification_table': spc_tbl_name
        }

        # Apply changes
        for path, value in path_value_mappings.items():
            path = 'structure/' + path # All paths are relative to structure
            self.model_node.find(path).text = value
