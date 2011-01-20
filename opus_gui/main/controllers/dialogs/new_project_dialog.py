# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import sys

from PyQt4.QtCore import SIGNAL, Qt

from PyQt4 import QtGui

from PyQt4.QtGui import QDialog, QSizePolicy

from opus_gui.main.opus_project import OpusProject
from opus_gui.util.icon_library import IconLibrary
from opus_gui.main.views.dialogs.ui_new_project_dynamic_dialog import Ui_NewProjectDynamicDialog

from opus_gui.main.controllers.dialogs.new_project_dialog_functions import merge_templated_nodes_with_project
from lxml.etree import SubElement

class NewProjectDynamicDialog(QDialog, Ui_NewProjectDynamicDialog):
    '''
    Class description
    '''
    
    def __init__(self, template_project, parent_widget = None):
        '''
        @param project (OpusProject): Currently loaded project
        @param parent_widget (QObject): parent object
        '''
        # parent window for the dialog box
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        QtGui.QDialog.__init__(self, parent_widget, flags)
        self.setupUi(self)
        
        self.template_nodes = template_project.get_template_nodes()
        self.new_project_filename = '' # this is what the caller of this dialog can expect to find the filename
        self.parent_project_filename = template_project.filename
        
        # collect all template nodes from the template project and categorize them on field_identifier
        self.fields_to_nodes = {}
        self._map_fields_to_nodes()
        
        # generate editing widgets for all the template nodes
        self.widgets = []
        self.data_extractors = {}
        self._generate_widgets()
        
        # visual tweaks
        self.lbl_header.setText('Create a new project based on ' + template_project.name)
        self._hide_error()
        self.buttonBox.button(self.buttonBox.Ok).setText('Create and load')
        self.le_project_name.setFocus()
        
        
    def _show_error(self, msg):
        ''' Show an error to the user '''
        msg = msg.replace('\n', '<br />')
        msg = '<qt><strong style="color: darkred;">Error</strong>&nbsp;' + msg + '</qt>'
        self.lbl_error.setText(msg)
        self.lbl_error.setVisible(True)
        
        
    def _hide_error(self):
        ''' Hide the error message widget '''
        self.lbl_error.setVisible(False)
        
        
    def _map_fields_to_nodes(self):
        ''' Group template nodes by their field_identifier ( id -> [node, ...] )'''
        self.fields_to_nodes = {}
        for node in self.template_nodes:
            field_id = node.get('field_identifier')
            if not field_id in self.fields_to_nodes:
                self.fields_to_nodes[field_id] = [node,]
            else:
                self.fields_to_nodes[field_id].append(node)
        # print self.fields_to_nodes
        

    def _get_widget_and_method_from_node_type(self, template_node):
        ''' 
        Retuns a widget and a method for the given node type.
        The widget is choosen to allow suitable input for the given node type.
        The method is a curried method that generates the suitable XML text value when called.
        Methods are guaranteed to always output a Python string value.
        '''
        
        # pre-populate the widget with data from the template node if it's not empty
        default_value = template_node.text or ''
        
        # selector for what data type to generate a widget for
        # TODO: add support for custom types ('field_data_type' argument) as in the new model dialog
        data_type = template_node.get('type')

        #  integers and float generates a numeric input only widget
        if data_type  in ['integer', 'float']:
            if data_type == 'integer':
                widget = QtGui.QSpinBox()
                widget.setMaximum(2**31-1)
            else:
                widget = QtGui.QDoubleSpinBox()
                widget.setMaximum(2**64-1)
            widget.setMinimum(-widget.maximum())

            try:
                value = float(default_value)
            except ValueError:
                value = 0.0

            widget.setValue(value)
            # both QSpinBox and QDoubleSpinBox return their value with value()
            return (widget, lambda x = widget: str(x.value()))

        # boolean generates a checkbox that outputs "True" or "False"
        if data_type == 'boolean':
            widget = QtGui.QCheckBox()
            widget.setChecked(default_value == 'True')
            return (widget, lambda x = widget: 'True' if x.isChecked() else 'False')

        # default to QLineEdit (string value editing). Outputs it's value as a Python string
        widget = QtGui.QLineEdit()
        widget.setText(default_value)
        return (widget, lambda x = widget: str(x.text()))


    def _generate_widgets(self):
        '''
        Iterate over all templated nodes and create a field (hidden or with a widget) for each.
        
        Note that the behavior is undefined when multiple nodes have the same field_identifier but different
        node types.
        '''
        
        self.data_extractors = {} # value extracting method for each field identifier
        self.widgets = [] # list of widgets to populate the GUI with
        
        # sizing policies for the generated widgets
        label_size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        widget_size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        description_size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        def get_widget_label(text):
            ''' Helper to generate a QLabel containing the given text '''
            l = QtGui.QLabel(field_id)
            l.setMinimumWidth(100)
            l.setSizePolicy(label_size_policy)
            return l

        # Remove the existing widgets. PyQt is buggy about removing dynamic widgets, 
        # so we need to explicitly call deleteLater() and 'del' the Python objects
        while self.dynamic_widgets.count() > 0:
            item = self.dynamic_widgets.takeAt(0)
            widget = item.widget()
            widget.hide()
            widget.deleteLater()
            del widget
            del item
        
        prev_widget = self.le_project_filename # prev_widget is used to link the tab order of widgets
        
        # create a widget for each field_identifier
        for field_id, nodes in self.fields_to_nodes.items():
            # pick the first node out of the list of nodes for this field identifier (there are at least one)
            node = nodes[0]
            
            current_row = len(self.widgets) # keep track of where to insert widgets (top to bottom)
            
            # get a suitable widget and a data-extrating method for the node
            widget, data_extractor = self._get_widget_and_method_from_node_type(node)
            self.data_extractors[field_id] = data_extractor # map the field_identifier to the data extractor
            
            label = get_widget_label(field_id)
            self.dynamic_widgets.addWidget(label, current_row, 0)

            widget.setSizePolicy(widget_size_policy) # make the widget expand to fill it's space
            self.dynamic_widgets.addWidget(widget, current_row, 1)
            
            # set the tab order so we get a nice tab flow between fields
            self.setTabOrder(prev_widget, widget)
            prev_widget = widget

            # an information widget is created if the templated node contains the optional field_description
            # argument was given 
            field_description = node.get('field_description') 
            if field_description:
                description_label = QtGui.QLabel()
                description_label.setSizePolicy(description_size_policy)
                description_label.setPixmap(IconLibrary.icon('info_small').pixmap(32, 32))
                desc = '<qt><b>%s</b><br/>%s</qt>' % (field_id, field_description)
                description_label.setToolTip(desc)
                self.dynamic_widgets.addWidget(description_label, current_row, 2)
            else:
                description_label = None
            self.widgets.append(widget)

    def _apply_widget_data_to_template_nodes(self):
        ''' Updated templated nodes using values from the dynamic widgets '''
        for template_node in self.template_nodes:
            template_field_id = template_node.get('field_identifier')
            template_node.text = self.data_extractors[template_field_id]()
            
    def _set_project_details(self, empty_project, project_name, project_parent, project_description):
        ''' Modify an empty project by setting up the <general> section using provided values '''
        root = empty_project.root_node()
        xml_version_node = SubElement(root, 'xml_version')
        general_node = SubElement(root, 'general')
        description_node = SubElement(general_node, 'description', {'type': 'string'})
        parent_node = SubElement(general_node, 'parent', {'type': 'file'})
        project_name_node = SubElement(general_node, 'project_name', {'hidden': 'True', 'type': 'string'})
        
        # set node values
        xml_version_node.text = '2.0'
        description_node.text = project_description
        parent_node.text = project_parent
        project_name_node.text = project_name


# ====================
# AUTO WIRED CALLBACKS
# ====================


    def on_tb_browse_folder_released(self):
        ''' User clicked the "browse" for save file name '''
        project_filename = QtGui.QFileDialog.getSaveFileName(self)
        if len(str(project_filename)) == 0:
            return
        
        # ensure xml ending
        project_filename = str(project_filename)
        
        if not project_filename.endswith('.xml'):
            project_filename = project_filename + '.xml'
        
        self.le_project_filename.setText(project_filename)
    
    def on_le_project_name_textChanged(self, new_text):
        ''' User typed into the project name line edit '''
        self._hide_error()
    
    def on_buttonBox_accepted(self):
        ''' User accepted the values in the dialog '''
        # convert values from QString to Python strings
        project_name = str(self.le_project_name.text())
        project_filename = str(self.le_project_filename.text())
        project_description = str(self.le_project_description.text())

        # validate required fields
        if len(project_filename) == 0:
            self.le_project_filename.setFocus()
            self._show_error('Please specify where to save the new project')
            return
        
        if len(project_name) == 0:
            self.le_project_name.setFocus()
            self._show_error('Please give the project a descriptive name')
            return
        
        # fetch user entered data to set the template node text values
        self._apply_widget_data_to_template_nodes()
        
        # create a new empty project and merge the templated nodes into it
        new_project = OpusProject()
        new_project.load_minimal_project()
        
        # manually create and set project name and project parent
        self._set_project_details(new_project, project_name, self.parent_project_filename, project_description)

        # merge in user node settings
        merge_templated_nodes_with_project(self.template_nodes, new_project)
        
        # try to save the project to the location given by the user
        flag, message = new_project.save(project_filename)
        if flag is not True:
            self._show_error(message)
            return
        
        # set the expected response attribute
        self.new_project_filename = project_filename
        
        print('Saved new project to {0}'.format(project_filename))
        self.accept()
        
    def on_buttonBox_rejected(self):
        ''' User rejected the changes in the GUI. Close and return '''
        self.reject()
        
        

    
