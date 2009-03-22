# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt4.QtCore import QString
from PyQt4.QtGui import QLabel, QLineEdit, QComboBox

from opus_gui.models_manager.controllers.dialogs.model_from_template_dialog_base import ModelFromTemplateDialogBase
from opus_gui.general_manager.general_manager import get_available_dataset_names

class AllocationModelFromTemplateDialog(ModelFromTemplateDialogBase):

    ''' Dialog for instantiating an Allocation Model '''

    def __init__(self, model_node, project = None, callback = None,
                 parent_widget = None):

        ModelFromTemplateDialogBase.__init__(self, model_node, project,
                                             callback, parent_widget)

        # allocation models do not have estimation components
        self.create_estimation_component = False

        #TODO: Check which of these we can make comboboxes instead of line edits
        self.cboDataset = QComboBox()
        self.leOutcome = QLineEdit('')
        self.leWeight = QLineEdit('')
        self.leControlTotal = QLineEdit('')
        self.leYearAttribute = QLineEdit('year')
        self.leCapacityAtr = QLineEdit('')
        self.leControlTblName = QLineEdit('control_totals')

        widget_pairs = ( # use tuple to preserve order
            ('Dataset', self.cboDataset),
            ('Outcome Variable', self.leOutcome),
            ('Weight Attribute', self.leWeight),
            ('Control Totals Table Name', self.leControlTblName),
            ('Control Total Attribute', self.leControlTotal),
            ('Year Attribute', self.leYearAttribute),
            ('Capacity Attribute', self.leCapacityAtr)
        )
        for l, w in widget_pairs:
            self._add_widget_pair(QLabel(l), w)

        for dataset_name in get_available_dataset_names(project):
            self.cboDataset.addItem(QString(dataset_name))

    def setup_node(self):
        self.model_node.tag = self._get_xml_friendly_name()

        path_value_mappings = {
        'run/dataset': self.cboDataset.currentText(),
        'run/outcome_attribute': self.leOutcome.text(),
        'run/weight_attribute': self.leWeight.text(),
        'run/control_total_attribute': self.leControlTotal.text(),
        'run/year_attribute': self.leYearAttribute.text(),
        'run/capacity_attribute': self.leCapacityAtr.text(),
        'prepare_for_run/control_totals_table_name': self.leControlTblName.text()
        }

        # Apply changes
        for path, value in path_value_mappings.items():
            path = 'structure/' + path # All paths are relative to structure
            self.model_node.find(path).text = value
