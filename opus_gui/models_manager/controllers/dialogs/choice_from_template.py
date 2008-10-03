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
                         
from PyQt4.QtGui import QComboBox, QLabel, QLineEdit

from PyQt4.QtXml import QDomElement, QDomText, QDomDocument

from opus_gui.models_manager.controllers.dialogs.model_from_template_dialog_base import \
    ModelFromTemplateDialogBase

class ChoiceModelFromTemplateDialog(ModelFromTemplateDialogBase):
    def __init__(self, main_window, model_template_node, template_index, template_model):
        ModelFromTemplateDialogBase.__init__(self, main_window, model_template_node, \
                                             template_index, template_model)
        
        # setup additional ui that's specfic for this model template
        self.setup_choice_ui()
        # self._setup_co_dataset_name()

    def setup_choice_ui(self):
        '''create the additional gui components for the choice model'''
        
        #TODO: Check which of these we can make comboboxes instead of line edits

        #TODO: where do we find the possible choice sets?
        self.leChoiceSet = QLineEdit('')
        self.leSubModelString = QLineEdit('')
        self.leChoiceAttributeName = QLineEdit('')
        self.leEstimationSizeAgents = QLineEdit('')
        self.leAgentSet = QLineEdit('')
        self.leAgentFilter = QLineEdit('')
        
        # create the widgets
        ctrl_pairs = (
            #TODO: replace with cbo
            ('Choice set', self.leChoiceSet),
            #TODO: replace with cbo
            ('Submodel String', self.leSubModelString),
            #TODO replace with cbo
            ('Choice Attribute Set', self.leChoiceAttributeName),
            
            ('Fraction of Agents for Estimation', self.leEstimationSizeAgents),
            ('Agent Set', self.leAgentSet),
            #TODO: check what filters do
            ('Agent Set Filter', self.leAgentFilter)           
        )
        
        for l,w in ctrl_pairs:
            self.add_widget_pair(QLabel(l), w)

    def setup_node(self):
        
        model_name = self.get_model_xml_name()
        self.set_model_name()
        
        # used multiple times; define once
        agent_set = self.leAgentSet.text()
        agent_set_filter = self.leAgentFilter.text()

        self.set_xml_element_to_value('init/arguments/choice_set', self.leChoiceSet.text())
        self.set_xml_element_to_value('init/arguments/submodel_string', self.leSubModelString.text())
        self.set_xml_element_to_value('init/arguments/choice_attribute_name', self.leChoiceAttributeName.text())
        self.set_xml_element_to_value('init/arguments/estimate_config/estimation_size_agents', self.leEstimationSizeAgents.text())
        self.set_xml_element_to_value('run/arguments/agent_set', agent_set)
        self.set_xml_element_to_value('prepare_for_run/arguments/agent_set', agent_set)
        self.set_xml_element_to_value('prepare_for_run/arguments/specification_table', model_name + '_specification')
        self.set_xml_element_to_value('prepare_for_run/arguments/coefficients_table', model_name + '_coefficients_table')
        self.set_xml_element_to_value('estimate/arguments/agent_set', agent_set)
        self.set_xml_element_to_value('prepare_for_estimate/arguments/agent_set', agent_set)
        self.set_xml_element_to_value('prepare_for_estimate/arguments/agent_filter', agent_set_filter)
