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

class AgentLocationChoiceModelFromTemplateDialog(ModelFromTemplateDialogBase):
    def __init__(self, main_window, model_template_node, template_index, template_model):
        ModelFromTemplateDialogBase.__init__(self, main_window, model_template_node, \
                                             template_index, template_model)
        
        # setup additional ui that's specfic for this model template
        self.setup_alcm_ui()
        # self._setup_co_dataset_name()

    def setup_alcm_ui(self):
        '''create the additional gui components for the agent location choice model'''

        self.leLocationSet = QLineEdit()
        self.leFilter = QLineEdit()
        self.leSubModelString = QLineEdit()
        self.leLocationIdString = QLineEdit()
        self.leShortName = QLineEdit()
        
        self.leSpecification = QLineEdit()
        self.leAgentsForEstimationTbl = QLineEdit()
        self.leAgentSet = QLineEdit()
        
        # create the widgets
        ctrl_pairs = (
            ('Short Name', self.leShortName),            
            ('Agent Set', self.leAgentSet),
            ('Location Set', self.leLocationSet),
            ('Location ID String', self.leLocationIdString),            
            ('Filter', self.leFilter),
            ('Submodel String', self.leSubModelString),
#            ('Specification', self.leSpecification),
            ('Agents for Estimation Table', self.leAgentsForEstimationTbl)
        )

        for l,w in ctrl_pairs:
            self.add_widget_pair(QLabel(l), w)

    def setup_node(self):
        model_name = self.get_model_xml_name()
        self.set_model_name(model_name)
        
        # used multiple times; define once
        agent_set = self.leAgentSet.text()
        filter = self.leFilter.text()
        agents_for_est_tbl = self.leAgentsForEstimationTbl.text()
        location_id = self.leLocationIdString.text()

        self.set_xml_element_to_value('init/arguments/location_set', self.leLocationSet.text()),
        self.set_xml_element_to_value('init/arguments/filter', filter)
        self.set_xml_element_to_value('init/arguments/submodel_string', self.leSubModelString.text()),
        self.set_xml_element_to_value('init/arguments/location_id_string', location_id)
        self.set_xml_element_to_value('init/arguments/short_name', self.leShortName.text()),

        self.set_xml_element_to_value('run/arguments/agent_set', agent_set)

        self.set_xml_element_to_value('prepare_for_run/arguments/specification_table', model_name + '_specification') 
        self.set_xml_element_to_value('prepare_for_run/arguments/coefficients_table', model_name + '_coefficients_table')

        self.set_xml_element_to_value('estimate/arguments/agent_set', agent_set)

        self.set_xml_element_to_value('prepare_for_estimate/arguments/specification_table', model_name + '_specification')
        self.set_xml_element_to_value('prepare_for_estimate/arguments/agent_set', agent_set)
        self.set_xml_element_to_value('prepare_for_estimate/arguments/agents_for_estimation_table', agents_for_est_tbl)
        self.set_xml_element_to_value('prepare_for_estimate/arguments/filter', filter)
        self.set_xml_element_to_value('prepare_for_estimate/arguments/location_id_variable', location_id)
