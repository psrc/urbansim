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
        model_name = self._get_model_name()
                
        # update the tag name
        nodeElement = self.model_template_node.toElement()
        nodeElement.setTagName(model_name)
        
        #TODO: traverse function for xml helper
        #xmlhelper.getelement(root, 'run/arguments/dataset')        
        dataset_element = nodeElement.\
            firstChildElement('run').firstChildElement('arguments').firstChildElement('dataset')
        expression_element = nodeElement.\
            firstChildElement('run').firstChildElement('arguments').firstChildElement('expression')
        outcome_attribute_element = nodeElement.\
            firstChildElement('run').firstChildElement('arguments').firstChildElement('outcome_attribute')
        
        #TODO: warning if any of them is null
        self._set_text_child(dataset_element, self.cboDataset.currentText())
        self._set_text_child(expression_element, self.leExpression.text())
        self._set_text_child(outcome_attribute_element, self.leOutcome.text())

    def _set_text_child(self, element, text):
        #TODO: Could this be useful in Travis' xml helper thing?
        '''set (or create) a text node as a child of a given element'''
        #TODO: some checking might be good that the xml tree is not a complete
        # mess (e.g has an entire subtree under the arguments/dataset)
        if(element.firstChild().isText()): # element has text child
            element.firstChild().setNodeValue(QString(text))
        else: # we have to create the text node
            text_node = self.mainwindow.toolboxBase.doc.createTextNode(text)
            element.insertBefore(text_node, element.firstChild())