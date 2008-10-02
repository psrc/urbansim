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
                        QGroupBox, QVBoxLayout, QIcon, QLabel, QDialog, \
                        QLineEdit
from PyQt4.QtXml import QDomText, QDomDocument

from opus_gui.models_manager.controllers.dialogs.model_from_template_dialog_base import \
    ModelFromTemplateDialogBase

class SimpleModelFromTemplateDialog(ModelFromTemplateDialogBase):
    def __init__(self, opusXMLAction_Model, model_template_node, template_index, template_model):
        ModelFromTemplateDialogBase.__init__(self, opusXMLAction_Model, model_template_node, \
                                             template_index, template_model)
        
        # simple models do not have estimation components
        self.create_estimation_component = False
        
        # setup additional ui that's specfic for this model template
        self.setup_simple_ui()
        self._setup_co_dataset_name()

    def setup_simple_ui(self):
        self.cboDataset = QComboBox()
        self.leExpression = QLineEdit('expression')
        self.leOutcome = QLineEdit('outcome variable')
        
        self.add_widget_pair(QLabel('Dataset'), self.cboDataset)
        self.add_widget_pair(QLabel('expression'), self.leExpression)
        self.add_widget_pair(QLabel('Outcome variable'), self.leOutcome)
        
    def _setup_co_dataset_name(self):
        '''collect avaiable datasets and populate the combobox'''
        available_datasets = self.xml_helper.get_available_datasets()
        self.cboDataset.clear()

        for dataset in available_datasets:
            self.cboDataset.addItem(QString(dataset))

    def setup_node(self):
        model_name = self.get_model_name()

        # update the tag name
        nodeElement = self.model_template_node.toElement()
        nodeElement.setTagName(model_name)
        
        dataset_e = self.xml_helper.get_sub_element_by_path(nodeElement, 'run/arguments/dataset')
        expression_e = self.xml_helper.get_sub_element_by_path(nodeElement, 'run/arguments/expression')
        outcome_attribute_e = self.xml_helper.get_sub_element_by_path(nodeElement, 'run/arguments/outcome_attribute')
        
        #TODO: warning if any of them is null?
        self.xml_helper.set_text_child_value(dataset_e, self.cboDataset.currentText())
        self.xml_helper.set_text_child_value(expression_e, self.leExpression.text())
        self.xml_helper.set_text_child_value(outcome_attribute_e, self.leOutcome.text())