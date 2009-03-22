# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt4.QtGui import QLabel, QLineEdit

from opus_gui.models_manager.controllers.dialogs.model_from_template_dialog_base import ModelFromTemplateDialogBase

class AgentLocationChoiceModelFromTemplateDialog(ModelFromTemplateDialogBase):

    ''' Dialog for instantiating an Agent Location Choice Model '''

    def __init__(self, model_node, project = None, callback = None,
                 parent_widget = None):

        ModelFromTemplateDialogBase.__init__(self, model_node, project,
                                             callback, parent_widget)

        self.leLocationSet = QLineEdit()
        self.leFilter = QLineEdit()
        self.leSubModelString = QLineEdit()
        self.leLocationIdString = QLineEdit()
        self.leShortName = QLineEdit()

        self.leSpecification = QLineEdit()
        self.leAgentsForEstimationTbl = QLineEdit()
        self.leAgentSet = QLineEdit()

        # create the widget pairs
        widget_pairs = (
            ('Short Name', self.leShortName),
            ('Agent Set', self.leAgentSet),
            ('Location Set', self.leLocationSet),
            ('Location ID String', self.leLocationIdString),
            ('Filter', self.leFilter),
            ('Submodel String', self.leSubModelString),
    #            ('Specification', self.leSpecification),
            ('Agents for Estimation Table', self.leAgentsForEstimationTbl)
        )

        for l, w in widget_pairs:
            self._add_widget_pair(QLabel(l), w)

    def setup_node(self):
        self.model_node.tag = self._get_xml_friendly_name()

        agent_set = self.leAgentSet.text()
        filter_ = self.leFilter.text()
        agents_for_est_tbl = self.leAgentsForEstimationTbl.text()
        location_id = self.leLocationIdString.text()

        # Build the list of changed node values
        path_value_mappings = {
        'init/location_set': self.leLocationSet.text(),
        'init/filter': filter_,
        'init/submodel_string': self.leSubModelString.text(),
        'init/location_id_string': location_id,
        'init/short_name': self.leShortName.text(),

        'run/agent_set': agent_set,

        'prepare_for_run/specification_table': self.model_node.tag + '_specification',
        'prepare_for_run/coefficients_table': self.model_node.tag + '_coefficients_table',

        'estimate/agent_set': agent_set,

        'prepare_for_estimate/specification_table': self.model_node.tag + '_specification',
        'prepare_for_estimate/agent_set': agent_set,
        'prepare_for_estimate/agents_for_estimation_table': agents_for_est_tbl,
        'prepare_for_estimate/filter': filter_,
        'prepare_for_estimate/location_id_variable': location_id
        }

        # Apply changes
        for path, value in path_value_mappings.items():
            # All paths are relative to structure
            path = 'structure/' + path
            self.model_node.find(path).text = value
