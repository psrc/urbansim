# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE
from opus_gui.util.icon_library import IconLibrary

import sys
import copy

from PyQt4.QtCore import SIGNAL, Qt
from PyQt4 import QtGui

from opus_gui.models_manager.views.ui_model_from_template_dialog_base import Ui_DynamicTemplateDialog
from opus_gui.general_manager.general_manager_functions import get_available_dataset_names
from opus_gui.general_manager.general_manager_functions import get_variable_nodes_per_dataset

class DynamicTemplateDialog(QtGui.QDialog, Ui_DynamicTemplateDialog):
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
    def __init__(self, model_node, project = None, parent_widget = None):
        '''
        @param project (OpusProject): Currently loaded project
        @param model_node (Element): template node to base the new model on
        @param parent_widget (QObject): parent object
        '''
        # parent window for the dialog box
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        QtGui.QDialog.__init__(self, parent_widget, flags)
        self.setupUi(self)

        self.model_node = copy.deepcopy(model_node)
        self.project = project

        self.fields_to_nodes = {}
        self.fields_to_data_methods = {}
        self.widgets = []

        QSP = QtGui.QSizePolicy # temporary alias
        self.label_size_policy = QSP(QSP.Expanding, QSP.MinimumExpanding)
        self.widget_size_policy = QSP(QSP.Expanding, QSP.Maximum)
        self.description_size_policy = QSP(QSP.Fixed, QSP.Fixed)
        del QSP

        self._hide_name_warning()
        self.connect(self.le_model_name, SIGNAL('textChanged(const QString &)'),
                     self._hide_name_warning)

        self.le_model_name.setText('new_%s' % model_node.get('name'))
        self.le_model_name.selectAll()
        self.le_model_name.focusWidget()

        self.lbl_header.setText('Creating model from template: %s' % self.model_node.get('name'))
        self._map_fields_to_nodes()
        self._generate_widgets()

    def _hide_name_warning(self):
        self.lbl_name_warning.setVisible(False)

    def _show_name_warning(self, warning_message):
        ''' Display a warning label about the name being invalid. '''
        self.lbl_name_warning.setText(warning_message)
        self.lbl_name_warning.setVisible(True)
        self.le_model_name.setFocus()
        self.le_model_name.selectAll()

    def _get_valid_model_name(self):
        '''
        Check that the model name is valid (i.e not taken and is over three characters in length).
        If it is the name is returned and the warning box is hidden.
        If the name is not valid, a message is displayed and ValueError is raised.
        '''
        taken_names = [n.get('name') for n in self.project.findall('model_manager/models/model')]
        trying_name = str(self.le_model_name.text()).strip()
        if trying_name in taken_names:
            msg = 'There is already a model named "%s", please enter another name.' % trying_name
            self._show_name_warning(msg)
            raise ValueError('%s is not a unique model name' % trying_name)
        if len(trying_name) < 3:
            msg = ('Models must have names that are at least three characters. '
                   'Please enter another name.')
            self._show_name_warning(msg)
            raise ValueError('%s to short (should be at least 3 characters)' % trying_name)

        self._hide_name_warning()
        return trying_name

    def _map_fields_to_nodes(self):
        ''' Categorize all nodes in a dictionary by their field_identifier '''
        self.fields_to_nodes = {}
        field_nodes = [n for n in self.model_node.getiterator() if n.get('field_identifier')]
        for node in field_nodes:
            field_id = node.get('field_identifier')
            if not field_id in self.fields_to_nodes:
                self.fields_to_nodes[field_id] = [node,]
            else:
                self.fields_to_nodes[field_id].append(node)

    def _apply_data_methods(self):
        ''' Map the data-method to all nodes '''
        for field, method in self.fields_to_data_methods.items():
            for node in self.fields_to_nodes[field]:
                node.text = method()

    def _widget_and_method_from_field_data_type(self, template_node):
        '''
        Fetch the widget and the data-method for a given node based in it's field_data_type
        argument. If the node doesn't have a field_data_type, or it's value is unknown, return None
        '''
        data_type = template_node.get('field_data_type')
        if not data_type:
            return None

        # Helper function to get a string based on the model name.
        # both the name and the type of the model node are updated before this method is called.
        def get_model_name_based_string(node = template_node, prefix = '', suffix = ''):
            while node is not None and node.tag != 'model':
                node = node.getparent()
            if node is None:
                raise LookupError('Could not locate the parent <model> node for %s' % str(node))
            return '%s%s%s' %(prefix, node.get('name'), suffix)

        # dataset
        if data_type == 'dataset':
            widget = QtGui.QComboBox()
            for dataset_name in get_available_dataset_names(self.project):
                widget.addItem(dataset_name)
            return (widget, widget.currentText)

        # model variable
        if data_type == 'model_variable':
            variables_per_dataset = get_variable_nodes_per_dataset(self.project)
            widget = QtGui.QComboBox()
            for dataset, variables in variables_per_dataset.items():
                for variable in variables:
                    widget.addItem('%s: %s' % (dataset, variable.get('name')))
            # return a method that only gives the name of the variable, and skips the dataset
            return (widget, lambda x = widget: widget.currentText().split(':')[1])

        # specification table
        # data-method should return a table name based on the models name
        if data_type == 'specification_table':
            return (None, lambda x = '_specification' : get_model_name_based_string(suffix = x))
        # coefficients table
        if data_type == 'coefficients_table':
            return (None, lambda x = '_coefficients': get_model_name_based_string(suffix = x))

        # unknown, notify with a warning
        print ('Warning: <%s name=%s> has a field_data_type of unknown value (%s) and is ignored.' %
               (template_node.tag, template_node.get('name'), data_type))
        return None

    def _widget_and_method_from_type(self, template_node):
        ''' return a widget and a method pair to edit data for the given node type '''
        default_value = template_node.text or ''
        data_type = template_node.get('type')

        #  Integer & Float
        if data_type  in ['integer', 'float']:
            if data_type == 'integer':
                widget = QtGui.QSpinBox()
                widget.setMaximum(sys.maxint)
            else:
                widget = QtGui.QDoubleSpinBox()
                widget.setMaximum(2**64)
            widget.setMinimum(-widget.maximum())

            try:
                value = float(default_value)
            except ValueError:
                value = 0.0
            widget.setValue(value)
            return (widget, widget.value)

        # Boolean
        if data_type == 'boolean':
            widget = QtGui.QCheckBox()
            widget.setChecked(default_value == 'True')
            def boolean_converter(_widget = widget):
                if widget.isChecked():
                    return 'True'
                return 'False'
            return (widget, lambda x = widget: 'True' if x.isChecked() else 'False')

        # default to QLineEdit
        widget = QtGui.QLineEdit()
        widget.setText(default_value)
        return (widget, widget.text)

    def _widget_and_method_for_template_node(self, template_node):
        '''
        Create a suitable widget for the given template node depending on it's type argument.
        For example, a node of type "string" should get a QLineEdit, while one with type="integer"
        should get a QSpinBox widget.
        Special widgets can be created if the node has an attribute 'field_data_type'.
        One special case is 'dataset', where a combobox with the available datasets is returned.
        'field_data_type' is used if it exists, otherwise 'type' is used. If neither attributes are
        present a QLineEdit is used.
        '''
        widget_and_method = self._widget_and_method_from_field_data_type(template_node)
        if not widget_and_method:
            widget_and_method = self._widget_and_method_from_type(template_node)
        return widget_and_method

    def _generate_widgets(self):
        '''
        Iterate over all templated nodes and create a field (hidden or with a widget) for each.
        '''
        self.fields_to_data_methods = {}
        self.widgets = []

        # PyQt is buggy about removing dynamic widgets, so we need to be very explicit here
        while self.dynamic_widgets.count() > 0:
            item = self.dynamic_widgets.takeAt(0)
            widget = item.widget()
            widget.hide()
            widget.deleteLater()
            del widget
            del item

        templated_nodes = [(n.get('field_identifier'), n) for n in self.model_node.getiterator() if
                           n.get('field_identifier') is not None]

        for field_id, node in templated_nodes:
            if field_id in self.fields_to_data_methods:
                continue # field_id already mapped to a widget + data-method
            widget, data_method = self._widget_and_method_for_template_node(node)
            # ensure that the data-method return clean Python strings
            self.fields_to_data_methods[field_id] = lambda fn = data_method: str(fn()).strip()
            if widget is not None:
                current_row = len(self.widgets)
                label = QtGui.QLabel(field_id)
                label.setMinimumWidth(100)
                label.setSizePolicy(self.label_size_policy)
                self.dynamic_widgets.addWidget(label, current_row, 0)

                widget.setSizePolicy(self.widget_size_policy)
                self.dynamic_widgets.addWidget(widget, current_row, 1)

                field_description = node.get('field_description')
                if field_description:
                    description_label = QtGui.QLabel()
                    description_label.setSizePolicy(self.description_size_policy)
                    description_label.setPixmap(IconLibrary.icon('info_small').pixmap(32, 32))
                    desc = '<qt><b>%s</b><br/>%s</qt>' % (field_id, field_description)
                    description_label.setToolTip(desc)
                    self.dynamic_widgets.addWidget(description_label, current_row, 2)
                else:
                    description_label = None

                # keep a list of widgets for testing purposes
                self.widgets.append((label, widget, description_label))

    def on_buttonBox_accepted(self):
        ''' Do some template -> model node magic before returning to the caller '''
        # don't leave with a broken model name
        try:
            model_name = self._get_valid_model_name()
        except ValueError:
            return

        # some data-methods need to have the new name before being run
        self.model_node.set('name', model_name)
        self.model_node.set('type', 'model')
        self.model_node.tag = 'model'

        self._apply_data_methods()

        # strip template attributes that was used for mapping in apply_values
        for node in self.model_node.getiterator():
            for attribute_to_strip in ['field_identifier', 'field_data_type']:
                if node.get(attribute_to_strip):
                    del node.attrib[attribute_to_strip]
        # let the caller know that the model node is ready
        self.accept()

    def on_buttonBox_rejected(self):
        self.reject()
