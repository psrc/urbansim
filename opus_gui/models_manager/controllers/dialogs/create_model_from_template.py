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

from PyQt4.QtCore import QString, SIGNAL, QModelIndex
from PyQt4.QtGui import QDialog
from PyQt4.QtXml import QDomText

from opus_gui.results_manager.xml_helper_methods import ResultsManagerXMLHelper

from opus_gui.models_manager.views.create_model_from_template_ui import Ui_CreateModelFromTemplate

class CreateModelFromTemplate(QDialog, Ui_CreateModelFromTemplate):
    def __init__(self, opusXMLAction_Model, flags, model_template_node, template_index, template_model):
        self.mainwindow = opusXMLAction_Model.mainwindow
        QDialog.__init__(self, self.mainwindow, flags)
        self.setupUi(self)
        self.opusXMLAction_Model = opusXMLAction_Model

        self.toolboxBase = self.mainwindow.toolboxBase

        self.xml_helper = ResultsManagerXMLHelper(toolboxBase = self.toolboxBase)
        self._setup_co_dataset_name()
        title = str(self.windowTitle())
        newtitle = '%s %s'%(title, str(model_template_node.toElement().tagName()))
        self.setWindowTitle(QString(newtitle))
        self.model_template_node = model_template_node
        self.template_index = template_index
        self.template_model = template_model
        
        
    def _setup_model_variables(self):
        
        model_variables = self.xml_helper.get_available_model_variables(attributes = ['dataset'])
                            
        self.model_variables = {}
        
        for indicator in model_variables:            
            name = indicator['name']
            dataset = indicator['dataset']
            self.model_variables[(dataset, name)] = indicator
            
            if self.cboDataset.currentText() == dataset:
                self.cboDependentVariable.addItem(QString(name))                
                      
    def _setup_co_dataset_name(self):
        available_datasets = self.xml_helper.get_available_datasets()

        for dataset in available_datasets:
            self.cboDataset.addItem(QString(dataset))

    def on_cboDataset_currentIndexChanged(self, param):

        if isinstance(param, int):
            return #qt sends two signals for the same event; only process one
        
        self._setup_model_variables()
        
    def on_saveChanges_released(self):
        
        model_name = self.cbModelName.text().replace(QString(" "),QString("_"))
        
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

        # Swap in the new name and drop in the node...
        self.template_model.insertRow(self.template_model.rowCount(self.template_index),
                             self.template_index,
                             self.model_template_node)
        self.template_model.emit(SIGNAL("layoutChanged()"))
        
        mt_node, _ = self.xml_helper.get_element_attributes(node_name = 'model_template', node_type = 'model_estimation')
        cloned_mt = mt_node.cloneNode()
        node_element = cloned_mt.toElement()
        node_element.setTagName(model_name)
        model = self.toolboxBase.modelManagerTree.model
        # Find the parent node index to append to
        parentIndex = model.index(0,0,QModelIndex()).parent()
        current_index = model.findElementIndexByName('estimation', parentIndex)[0]

        # Now insert the head_node
        model.insertRow(model.rowCount(current_index),
                        current_index,
                        cloned_mt)

        model.emit(SIGNAL("layoutChanged()"))        
        self.close()
    
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
                
    def on_cancelWindow_released(self):
        self.close()