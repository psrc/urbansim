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
from PyQt4.QtXml import QDomElement

from opus_gui.results_manager.xml_helper_methods import ResultsManagerXMLHelper

from opus_gui.models_manager.views.ui_model_from_template_dialog_base import \
     Ui_ModelFromTemplateDialogBase

class ModelFromTemplateDialogBase(QDialog, Ui_ModelFromTemplateDialogBase):
    '''Base dialog class to allow for easy creation of more specific model
    template creation dialogs
    
    When the user clicks the OK button, this base calls the method
    setup_node() before inserting the cloned node into the model tree. Child
    dialogs should implement and handle their modification of the template
    node (self.model_template_node) in that method. They should not call
    _insert_model_and_create_estimation() or implement their own
    _on_accepted() or _on_rejected() methods.
    
    Models that do not have estimation components should set the instance
    variable create_estimation_component to False.
    '''
    def __init__(self, mainwindow, model_template_node, model_manager_model):
        # parent window for the dialog box
        self.mainwindow = mainwindow
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | \
                Qt.WindowMaximizeButtonHint
        QDialog.__init__(self, self.mainwindow, flags)
        self.setupUi(self)
       
        self.xml_helper = ResultsManagerXMLHelper(mainwindow.toolboxBase)
        
        self.model_template_node = model_template_node
        self.model_manager_model = model_manager_model
        
        self.connect(self.buttonBox, SIGNAL("accepted()"), self._on_accepted)
        self.connect(self.buttonBox, SIGNAL('rejected()'), self._on_rejected)
        
        self.setModal(True)
      
        # default name based on tag name for template
        tag_name = model_template_node.toElement().tagName()
        tag_name.replace('_template', '').replace('_', ' ')
        self.leModelName.setText(tag_name)
        self.leModelName.selectAll()
        self.leModelName.focusWidget()
        
        title = str(self.windowTitle())
        newtitle = '%s %s'%(title, tag_name)
        self.setWindowTitle(QString(newtitle))
        
        # the pairings of xml nodes (by path) and their values
        self._xmlpath_value_pairs = []
        
    def add_widget_pair(self, left_widget, right_widget):
        '''Add a pair of widgets to the dialog.'''
        # make the leftmost widget (usually a label) constraint to a certain 
        # size to maintain a nice grid
        left_widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, 
                                              QSizePolicy.MinimumExpanding))
        right_widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, 
                                               QSizePolicy.Maximum))
        
        left_widget.setMinimumSize(QSize(100, 0))
        left_widget.setMaximumSize(QSize(200, 16777215))

        layout = QHBoxLayout()
        layout.addWidget(left_widget)
        layout.addWidget(right_widget)
        self.groupBox.layout().addLayout(layout)

    def set_structure_element_to_value(self, xmlpath, value):
        '''sets an element rooted in the models structure to a value
        usage example:
        to set "structure/init/name" to "modelname"; 
          set_structure_element_to_value("init/name", "modelname")'''
        structure_element = \
        self.xml_helper.get_sub_element_by_path(self.model_template_node, 
                                                'structure/')
        
        xml_element = \
            self.xml_helper.get_sub_element_by_path(structure_element, xmlpath)
        
        if not xml_element or not isinstance(xml_element, QDomElement):
            raise ValueError('No such element (%s>%s)' \
                             %(structure_element.toElement().tagName(),xmlpath))
        self.xml_helper.set_text_child_value(xml_element, value)

    def get_model_xml_name(self):
        '''return a valid model name based on the string the user entered'''
        #TODO: make sure that the name is actually a valid xml name
        return self.leModelName.text().replace(QString(' '), QString('_'))
    
    def set_model_name(self, value = None):
        '''set the name of the root node to a valid xml value. 
        Default value is self.get_model_xml_name().'''
        xmlname = value if value else self.get_model_xml_name()
        self.model_template_node.toElement().setTagName(xmlname)
        
    def _create_estimations_and_insert_node(self):
        '''insert the node back into the model system and create an entry for 
        the new model in the estimations'''
        new_model_element = self.model_template_node.toElement()
        new_model_element.removeAttribute('hidden')
        new_model_element.setAttribute('type', QString('model'))
        self.model_manager_model.insert_model(new_model_element)
        
    def setup_node(self):
        # code that sets the specific template variables goes here
        pass

    def _on_accepted(self):
        # code that sets the specific template variables goes here
        self.setup_node()
        # insert into project tree and tree view model
        self._create_estimations_and_insert_node()

    def _on_rejected(self):
        self.close()
