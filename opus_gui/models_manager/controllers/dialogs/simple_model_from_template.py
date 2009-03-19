# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from PyQt4.QtGui import QLineEdit, QComboBox, QLabel

from opus_gui.models_manager.controllers.dialogs.model_from_template_dialog_base import ModelFromTemplateDialogBase
from opus_gui.general_manager.general_manager import get_available_dataset_names

class SimpleModelFromTemplateDialog(ModelFromTemplateDialogBase):

    ''' Dialog for instantiating a SimpleModel '''

    def __init__(self, model_node, project = None, callback = None,
                 parent_widget = None):

        ModelFromTemplateDialogBase.__init__(self, model_node, project,
                                             callback, parent_widget)

        self.cboDataset = QComboBox()
        self.leExpression = QLineEdit('expression')
        self.leOutcome = QLineEdit('outcome variable')

        self._add_widget_pair(QLabel('Dataset'), self.cboDataset)
        self._add_widget_pair(QLabel('expression'), self.leExpression)
        self._add_widget_pair(QLabel('Outcome variable'), self.leOutcome)

        for dataset_name in get_available_dataset_names(project):
            self.cboDataset.addItem(dataset_name)

    def setup_node(self):
        self.model_node.tag = self._get_xml_friendly_name()

        path_value_mappings = {
        'run/dataset': self.cboDataset.currentText(),
        'run/expression': self.leExpression.text(),
        'run/outcome_attribute': self.leOutcome.text()
        }

        # Apply changes
        for path, value in path_value_mappings.items():
            path = 'structure/' + path # All paths are relative to structure
            self.model_node.find(path).text = value
