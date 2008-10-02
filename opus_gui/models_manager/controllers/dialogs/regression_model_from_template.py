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
                        QGroupBox, QVBoxLayout, QIcon, QLabel, QDialog
from PyQt4.QtXml import QDomText

from opus_gui.models_manager.controllers.dialogs.model_from_template_dialog_base import ModelFromTemplateDialogBase

#TODO: Rodo this one to have the same code formatting as the newer dialogs

class RegressionModelFromTemplateDialog(ModelFromTemplateDialogBase):
    def __init__(self, opusXMLAction_Model, model_template_node, template_index, template_model):
        ModelFromTemplateDialogBase.__init__(self, opusXMLAction_Model, model_template_node, \
                                             template_index, template_model)

        # setup additional ui that's specfic for this model template
        self.setup_regression_ui()
        self._setup_co_dataset_name()
        self._setup_model_variables()

    def setup_regression_ui(self):
        self.cboDataset = QComboBox()
        self.connect(self.cboDataset, SIGNAL('currentIndexChanged(int)'), self._refresh_model_variables)

        self.cboDependentVariable = QComboBox()
        
        self.add_widget_pair(QLabel('Dataset'), self.cboDataset)
        self.add_widget_pair(QLabel('Dependent variable'), self.cboDependentVariable)
        
    def _setup_model_variables(self):
        '''Collect the model variables and populate the combobox'''        
        model_variables = self.xml_helper.get_available_model_variables(attributes = ['dataset'])
        self.model_variables = {}
        
        #TODO: this does not return any model_vars for any data sets
        # except gridcell?
        
        # self.cboDependentVariable.clear()
        for indicator in model_variables:            
            name = indicator['name']
            dataset = indicator['dataset']
            self.model_variables[(dataset, name)] = indicator
            
            if self.cboDataset.currentText() == dataset:
                self.cboDependentVariable.addItem(QString(name))                

    def _setup_co_dataset_name(self):
        '''collect avaiable datasets and populate the combobox'''
        available_datasets = self.xml_helper.get_available_datasets()

        for dataset in available_datasets:
            self.cboDataset.addItem(QString(dataset))

    def _refresh_model_variables(self, index):

        # you can specify what signals to catch with this slot
        # by connect(SIGNAL(currentIndexChanged(int)) vs. 
        # connect(SIGNAL(currentIndexChanged(QString))
        # // christoffer
        
#        if isinstance(index, int):
#            return #qt sends two signals for the same event; only process one
#        
        self._setup_model_variables()

    def setup_node(self):
        
        model_name = self.get_model_name()
        
        nodeElement = self.model_template_node.toElement()
        if not nodeElement.isNull():
            nodeElement.setTagName(model_name)

        run_node = None
        prepare_for_run_node = None
        estimate_node = None
        prepare_for_estimate_node = None
        
        node = self.model_template_node.firstChild()
        # Only march on if we have non-null nodes
        while not node.isNull():
            # We only want to check out this node if it is of type "element"
            if node.isElement():
                domElement = node.toElement()
                if not domElement.isNull():
                    # Now we check to see if the tagname is the one we are looking for
                    name = str(domElement.tagName())
                    if name == 'run':
                        run_node = node
                    elif name == 'prepare_for_run':
                        prepare_for_run_node = node
                    elif name == 'estimate':
                        estimate_node = node
                    elif name == 'prepare_for_estimate':
                        prepare_for_estimate_node = node
            node = node.nextSibling()

        dataset_name = self.cboDataset.currentText()
        for node in [run_node, prepare_for_run_node, estimate_node, prepare_for_estimate_node]:    
#            print '%s'%node.toElement().tagName()
            sub_node = node.firstChild()                
            while not sub_node.isNull():
                if sub_node.isElement():
                    domElement = sub_node.toElement()
                    name = str(domElement.tagName())
#                    print '\tsub: %s'%name
                    if name == 'arguments':
                        sub_sub_node = sub_node.firstChild()
                        while not sub_sub_node.isNull():
                            if sub_sub_node.isElement():
                                domElement = sub_sub_node.toElement()
                                name = str(domElement.tagName())
#                                print '\t\tsubsub: %s'%name
                                if name == 'dataset':
                                    self.update_node(domElement, dataset_name)
                                elif name in ['specification_table', 'coefficients_table', 'specification_table']:
                                    self.update_node(domElement, replace = ('regression_model_template', model_name))
                                elif name == 'dependent_variable':
                                    self.update_node(domElement, value = self.cboDependentVariable.currentText())
                            sub_sub_node = sub_sub_node.nextSibling()
                sub_node = sub_node.nextSibling()
    
    def update_node(self, domElement, value = None, replace = None):
        elementText = str(domElement.text())

        if replace is None:
            value = str(value)
        else:
            value = elementText.replace(replace[0], replace[1])

        found = False
        if elementText != value:
            if domElement.hasChildNodes():
                children = domElement.childNodes()
                for x in xrange(0,children.count(),1):
                    if children.item(x).isText():
                        textNode = children.item(x).toText()
                        textNode.setData(QString(value))
                        found = True
        if not found:
            new_node = QDomText()
            new_node.setData(QString(value))
            domElement.appendChild(new_node)