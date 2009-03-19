# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from PyQt4.QtGui import QLabel, QLineEdit

from opus_gui.models_manager.controllers.dialogs.model_from_template_dialog_base import ModelFromTemplateDialogBase

class ChoiceModelFromTemplateDialog(ModelFromTemplateDialogBase):

    ''' Dialog for instantiating a Choice Model '''

    def __init__(self, model_node, project = None, callback = None,
                 parent_widget = None):

        ModelFromTemplateDialogBase.__init__(self, model_node, project,
                                             callback, parent_widget)

        # setup additional ui that's specific for this model template

        #TODO: Check which of these we can make comboboxes instead of line edits
        #TODO: where do we find the possible choice sets?
        self.leChoiceSet = QLineEdit('')
        self.leSubModelString = QLineEdit('')
        self.leChoiceAttributeName = QLineEdit('')
        self.leEstimationSizeAgents = QLineEdit('')
        self.leAgentSet = QLineEdit('')
        self.leAgentFilter = QLineEdit('')

        # create the widgets
        widget_pairs = (
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

        for l, w in widget_pairs:
            self._add_widget_pair(QLabel(l), w)

    def setup_node(self):
        self.model_node.tag = self._get_xml_friendly_name()

        # used multiple times; define once
        agent_set = self.leAgentSet.text()
        agent_set_filter = self.leAgentFilter.text()

        path_value_mappings = {
        'init/choice_set': self.leChoiceSet.text(),
        'init/submodel_string': self.leSubModelString.text(),
        'init/choice_attribute_name': self.leChoiceAttributeName.text(),
        'init/estimate_config/estimation_size_agents': self.leEstimationSizeAgents.text(),
        'run/agent_set': agent_set,
        'prepare_for_run/agent_set': agent_set,
        'prepare_for_run/specification_table': self.model_node.tag + '_specification',
        'prepare_for_run/coefficients_table': self.model_node.tag + '_coefficients_table',
        'estimate/agent_set': agent_set,
        'prepare_for_estimate/agent_set': agent_set,
        'prepare_for_estimate/agent_filter': agent_set_filter
        }

        # Apply changes
        for path, value in path_value_mappings.items():
            path = 'structure/' + path # All paths are relative to structure
            self.model_node.find(path).text = value
