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
    def __init__(self, opusXMLAction_Model, model_template_node, template_index, template_model):
        ModelFromTemplateDialogBase.__init__(self, opusXMLAction_Model, model_template_node, \
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
        model_name = self._get_model_name()
                
        # update the tag name
        nodeElement = self.model_template_node.toElement()
        nodeElement.setTagName(model_name)
        
        # shorter and nicer name
        element_by_path = lambda x: self.xml_helper.get_sub_element_by_path(nodeElement, x)
        
        run_arguments = 'run/arguments/'

       # pair the elements with the corresponding text values
        element_text_pairs = (
            (element_by_path(run_arguments + 'dataset'), self.cboDataset.currentText()),
            (element_by_path(run_arguments + 'outcome_attribute'), self.leOutcome.text()),
            (element_by_path(run_arguments + 'weight_attribute'), self.leWeight.text()),
            (element_by_path(run_arguments + 'control_total_attribute'), self.leControlTotal.text()),
            (element_by_path(run_arguments + 'year_attribute'), self.leYearAttribute.text()),
            (element_by_path(run_arguments + 'capacity_attribute'), self.leCapacityAtr.text()),
            (element_by_path('prepare_for_run/arguments/control_totals_table_name'), self.leControlTblName.text())
        )

        # setup the node
        for element, text in element_text_pairs:
            if element and isinstance(element, QDomElement):
                self.xml_helper.set_text_child_value(element, text)
            else:
                print 'Invalid element provided in setup_node(). Text=:"%s"' %text
