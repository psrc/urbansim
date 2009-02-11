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

from PyQt4.QtGui import QDialog, QMenu, QCursor, QAction
from PyQt4.QtCore import Qt, SIGNAL

from opus_gui.main.controllers.dialogs.message_box import MessageBox

from opus_gui.general_manager.views.ui_variable_library import Ui_VariableLibrary
from opus_gui.general_manager.views.variables_table_view import VariablesTableView
from opus_gui.general_manager.models.variables_table_model import variable_to_validator_format, \
    VariablesTableModel, create_empty_variable
from opus_gui.general_manager.run.variable_validator import VariableValidator
from opus_gui.general_manager.general_manager import get_variable_nodes_per_dataset
from opus_gui.general_manager.controllers.all_variables import AllVariablesEditGui
from opus_gui.main.controllers.instance_handlers import get_mainwindow_instance
from opus_gui.general_manager.controllers.variable_editor import VariableEditor

class VariableLibrary(QDialog, Ui_VariableLibrary):

    def __init__(self, project, parent_widget=None):
        QDialog.__init__(self, parent_widget, Qt.Window)
        self.setupUi(self)
        self.project = project
        # Format the variables of the project in a way that the
        # VariableTableModel likes (see VariableTableModel for documentation)
        nodes_per_ds = get_variable_nodes_per_dataset(project)
        variables = []
        # Keep a mapping of nodes <-> variables so that we can keep track of
        # which variables that where added, edited or removed and save it back
        # to XML
        variable_to_node_map = {}
        for variable_nodes in nodes_per_ds.values():
            for variable_node in variable_nodes:
                v = create_empty_variable()
                v['name'] = variable_node.tag
                v['definition'] = str(variable_node.text).strip()
                for key in ['dataset', 'use', 'source', 'inherited']:
                    v[key] = variable_node.get(key)
                for key in ['selected', 'dirty', 'syntaxerror', 'dataerror']:
                    v[key] = False
                variables.append(v)
                # Hash on nodes since dicts are unhashable
                variable_to_node_map[variable_node] = v

        self.view = VariablesTableView(self)
        self.model = VariablesTableModel(self.view, variables)
        self.view.setModel(self.model)

        # Automatically update the save button state on model data change
        def update_savestate():
            self.pbSave.setEnabled(self.model.dirty)
        signal = 'dataChanged(const QModelIndex &, const QModelIndex &)'
        self.connect(self.model, SIGNAL(signal), update_savestate)
        # Right clicking the table brings a context menu
        self.connect(self.view,
                     SIGNAL("customContextMenuRequested(const QPoint &)"),
                     self.on_table_right_clicked)
        # Double clicking an item in the table brings up the editor
        # TODO connect doubleClick

        # Explicit event handlers
        self.connect(self.pbNewVariable, SIGNAL('released()'),
                     self.add_variable)

        # Get an instance of a variable validator for variable checking
        self.validator = VariableValidator(self.project)

        # Add the table
        self.table_container.layout().addWidget(self.view)

    def on_pbClose_released(self):
        ''' event handler for when user clicks the close button '''
        if self.model.dirty:
            # TODO ask for confirmation
            MessageBox(self, 'closing with saved data')
        else:
            self.close()

    def on_pbSave_release(self):
        ''' event handler for when the user clicks the save button '''
        print 'save'

    def on_pbValidateSelected_released(self):
        ''' User clicked the validate selected button '''
        selected_variables = [var for var in self.view.variables() if
                              var['selected']]
        self.check_variable_syntax(selected_variables)

    def check_variable_syntax(self, variables):
        '''
        Sends a variable to the variable validator for syntax check
        '''
        # Get a list of all the variables in validator format (vf)
        variables_in_vf = map(variable_to_validator_format, variables)
        for var, var_vf in zip(variables, variables_in_vf):
            result, errors = self.validator.check_parse_errors(variables=(var_vf,))
            var['syntaxerror'] = errors if result == False else False
            if var['syntaxerror']:
                print var['name'], 'has syntaxerrors'
            else:
                print var['name'], 'has no syntaxerrors'

    def on_table_right_clicked(self, point):
        ''' handler for the when users right click on table view '''
        index = self.view.indexAt(point)
        if not index.isValid: return
        self.view.setCurrentIndex(index)
        variable = self.model.variables[index.row()]
        menu = QMenu(self.view)
        # Edit variable action
        edit_action = QAction('Edit %s' % variable['name'], self)
        cb = lambda x = variable: \
            VariableEditor(variable = x,
                           validator = self.validator,
                           callback = self.edit_variable_cb,
                           parent_widget = self).show()
        self.connect(edit_action, SIGNAL('triggered()'), cb)
        menu.addAction(edit_action)
        # Clone variable action
        clone_action = QAction('Create new variable based on this', self)
        cb = lambda x = variable: self.add_variable(x)
        self.connect(clone_action, SIGNAL('triggered()'), cb)
        menu.addAction(clone_action)
        # Check syntax
        syntax_action = QAction('Check syntax', self)
        self.connect(syntax_action, SIGNAL('triggered()'), lambda x:None)
        syntax_action.setEnabled(False)
        menu.addAction(syntax_action)
        # Check against data
        data_check_action = QAction('Check against data', self)
        self.connect(data_check_action, SIGNAL('triggered()'), lambda x: None)
        data_check_action.setEnabled(False)
        menu.addAction(data_check_action)
        # Delete the variable
        delete_action = QAction('Delete %s' % variable['name'], self)
        self.connect(delete_action, SIGNAL('triggered()'),
                     lambda x = variable: self.delete_variable(x))
        menu.addAction(delete_action)
        # Make the variable local
        make_local_action = QAction('Make variable local', self)
        self.connect(make_local_action, SIGNAL('triggered()'),
                     lambda x = variable: self.make_local(x))
        menu.addAction(make_local_action)

        # Menu constructed, present to user
        if not menu.isEmpty():
            menu.exec_(QCursor.pos())

    def add_variable(self, base_on_variable = None):
        '''
        Add and edit a new variable.
        @param base_on_variable (dict) if given, all values are copied from
        this variable to the new variable.
        '''
        var = create_empty_variable()
        if base_on_variable is not None:
            for key in base_on_variable:
                var[key] = base_on_variable[key]
            var['name'] += '_copy'
        variable_editor = VariableEditor(variable = var,
                                         validator = self.validator,
                                         callback = self.add_variable_cb,
                                         parent_widget = self)
        variable_editor.show()

    def on_pbDEBUG_released(self):
        print 'debug button'
        v = AllVariablesEditGui(get_mainwindow_instance(), Qt.Dialog)
        v.show()

    def delete_variable(self, variable):
        ''' delete the given variable '''
        if variable in self.model.variables:
            self.model.removeVariable(variable)

    def validate_variable(self, variable):
        ''' validates the selected variable '''
        print 'validate', variable['name']

    def check_against_data(self, variable):
        ''' check the selected variable against data '''
        print 'check against data', variable['name']

    def make_variable_local(self, variable):
        ''' remove the inherited flag for the selected variable '''
        variable['inherited'] = False

    # call backs for adding/editing variables
    def add_variable_cb(self, edited_variable, original_variable):
        self.model.add_variable(edited_variable)

    def edit_variable_cb(self, edited_variable, original_variable):
        # copy all changes back to the variable that was edited
        for k in edited_variable:
            original_variable[k] = edited_variable[k]

