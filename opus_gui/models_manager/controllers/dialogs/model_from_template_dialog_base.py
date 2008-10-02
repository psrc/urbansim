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

from PyQt4.QtCore import QString, SIGNAL, QModelIndex, QSize, Qt
from PyQt4.QtGui import QHBoxLayout, QSizePolicy, QDialog
from PyQt4.QtXml import QDomText

from opus_gui.results_manager.xml_helper_methods import ResultsManagerXMLHelper

from opus_gui.models_manager.views.ui_model_from_template_dialog_base import Ui_ModelFromTemplateDialogBase

class ModelFromTemplateDialogBase(QDialog, Ui_ModelFromTemplateDialogBase):
    '''Base dialog class to allow for easy creation of more specific model template creation dialogs
    
    When the user clicks the OK button, this base calls the method setup_node() before inserting the
    cloned node into the model tree. Child dialogs should implement and handle their modification 
    of the template node (self.model_template_node) in that method.
    They should not call _insert_model_and_create_estimation() or implement their own 
    _on_accepted() or _on_rejected() methods.
    
    Models that do not have estimation components should set the instance variable 
    create_estimation_component to False.
    '''
    def __init__(self, mainwindow, model_template_node, template_index, template_model):
        # parent window for the dialog box
        self.mainwindow = mainwindow
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        QDialog.__init__(self, self.mainwindow, flags)
        
        self.setupUi(self)

        self.xml_helper = ResultsManagerXMLHelper(self.mainwindow.toolboxBase)
        
        self.model_template_node = model_template_node
        self.template_index = template_index
        self.template_model = template_model
        
        self.connect(self.buttonBox, SIGNAL("accepted()"), self._on_accepted)
        self.connect(self.buttonBox, SIGNAL('rejected()'), self._on_rejected)
        
        self.setModal(True)
        # should we create an estimation component when inserting the
        # model into the tree. Override this value for model dialogs that do 
        # not have an estimation component.
        self.create_estimation_component = True
        
        # default name based on tag name for template
        tag_name = model_template_node.toElement().tagName()
        tag_name.replace('_template', '').replace('_', ' ')
        self.leModelName.setText(tag_name)
        self.leModelName.selectAll()
        self.leModelName.focusWidget()
        
        title = str(self.windowTitle())
        newtitle = '%s %s'%(title, tag_name)
        self.setWindowTitle(QString(newtitle))
        
    def add_widget_pair(self, left_widget, right_widget):
        '''Add a pair of widgets, typically a label and another widget, to the dialog'''
        # make the leftmost widget (usually a label) constraint to a certain size
        # to maintain a nice grid
        left_widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding))
        right_widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum))
        
        left_widget.setMinimumSize(QSize(100, 0))
        left_widget.setMaximumSize(QSize(200, 16777215))

        layout = QHBoxLayout()
        layout.addWidget(left_widget)
        layout.addWidget(right_widget)
        self.groupBox.layout().addLayout(layout)
        
    def get_model_name(self):
        '''return a valid model name based on the string the user entered'''
        #TODO: the name should actually be valid (ie, alphanumeric)
        return self.leModelName.text().replace(QString(' '), QString('_'))
    
    def _insert_model_and_create_estimation(self):
        '''insert the node back into the model system and create an entry for the new model in the estimations'''
        
        self.template_model.insertRow(self.template_model.rowCount(self.template_index),
                                      self.template_index,
                                      self.model_template_node)
        self.template_model.emit(SIGNAL('layoutChanged()'))

        # create an estimation component
        #TODO: verify that this belongs in this module
        if self.create_estimation_component:
            mt_node, _ = self.xml_helper.get_element_attributes(node_name = 'model_template', node_type = 'model_estimation')
            cloned_mt = mt_node.cloneNode()
            node_element = cloned_mt.toElement()
            
            node_element.setTagName(self.model_template_node.toElement().tagName())
            
            tree_model = self.mainwindow.toolboxBase.modelManagerTree.model
            
            # Find the parent node index to append to
            parentIndex = tree_model.index(0,0,QModelIndex()).parent()
            current_index = tree_model.findElementIndexByName('estimation', parentIndex)[0]
    
            # Now insert the head_node
            tree_model.insertRow(tree_model.rowCount(current_index),
                            current_index,
                            cloned_mt)
    
            tree_model.emit(SIGNAL("layoutChanged()"))
        
    def setup_node(self):
        # code that sets the specific template variables goes here
        pass
    
    def _on_accepted(self):
        # code that sets the specific template variables goes here
        self.setup_node()
        # insert into project tree and tree view model
        self._insert_model_and_create_estimation()
        
    def _on_rejected(self):
        self.close()
