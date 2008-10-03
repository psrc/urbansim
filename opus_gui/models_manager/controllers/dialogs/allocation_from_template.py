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

from PyQt4.QtCore import QString, SIGNAL
from PyQt4.QtGui import QLabel, QLineEdit, QComboBox
from PyQt4.QtXml import QDomText, QDomDocument, QDomElement

from opus_gui.models_manager.controllers.dialogs.model_from_template_dialog_base import \
    ModelFromTemplateDialogBase

class AllocationModelFromTemplateDialog(ModelFromTemplateDialogBase):
    def __init__(self, main_window, model_template_node, template_index, template_model):
        ModelFromTemplateDialogBase.__init__(self, main_window, model_template_node, \
                                             template_index, template_model)
        
        # allocation models do not have estimation components
        self.create_estimation_component = False
        
        # setup additional ui that's specfic for this model template
        self.setup_allocation_ui()
        self._setup_co_dataset_name()

    def setup_allocation_ui(self):
        '''create the additional gui components for the allocation model'''
        
        #TODO: Check which of these we can make comboboxes instead of line edits
        self.cboDataset = QComboBox()
        self.leOutcome = QLineEdit('')
        self.leWeight = QLineEdit('')
        self.leControlTotal = QLineEdit('')
        self.leYearAttribute = QLineEdit('year')
        self.leCapacityAtr = QLineEdit('')
        self.leControlTblName = QLineEdit('control_totals')
        
        ctrl_pairs = ( # use tuple to preserve order
            ('Dataset', self.cboDataset),
            ('Outcome Variable', self.leOutcome),
            ('Weight Attribute', self.leWeight),
            ('Control Totals Table Name', self.leControlTblName),
            ('Control Total Attribute', self.leControlTotal),
            ('Year Attribute', self.leYearAttribute),
            ('Capacity Attribute', self.leCapacityAtr)           
        )
        for l,w in ctrl_pairs:
            self.add_widget_pair(QLabel(l), w)

    def _setup_co_dataset_name(self):
        '''collect avaiable datasets and populate a combobox'''
        available_datasets = self.xml_helper.get_available_datasets()
        self.cboDataset.clear()
        
        for dataset in available_datasets:
            self.cboDataset.addItem(QString(dataset))

    def setup_node(self):
        self.set_model_name()
        self.set_xml_element_to_value('run/arguments/dataset', self.cboDataset.currentText()),
        self.set_xml_element_to_value('run/arguments/outcome_attribute', self.leOutcome.text()),
        self.set_xml_element_to_value('run/arguments/weight_attribute', self.leWeight.text()),
        self.set_xml_element_to_value('run/arguments/control_total_attribute', self.leControlTotal.text()),
        self.set_xml_element_to_value('run/arguments/year_attribute', self.leYearAttribute.text()),
        self.set_xml_element_to_value('run/arguments/capacity_attribute', self.leCapacityAtr.text()),
        self.set_xml_element_to_value('prepare_for_run/arguments/control_totals_table_name', self.leControlTblName.text())

