# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt4.QtGui import QDialog, QMenu, QCursor, QFont
from PyQt4.QtCore import Qt, SIGNAL

from opus_gui.general_manager.views.ui_variable_library import Ui_VariableLibrary
from opus_gui.general_manager.views.variables_table_view import VariablesTableView
from opus_gui.general_manager.models.variables_table_model import VariablesTableModel
from opus_gui.general_manager.models.variables_table_model import node_from_variable
from opus_gui.general_manager.models.variables_table_model import create_empty_variable
from opus_gui.general_manager.models.variables_table_model import variable_batch_check
from opus_gui.general_manager.models.variables_table_model import variable_from_node
from opus_gui.general_manager.run.variable_validator import VariableValidator
from opus_gui.general_manager.general_manager_functions import get_variable_nodes_per_dataset
from opus_gui.general_manager.controllers.variable_editor import VariableEditor

from opus_gui.util import common_dialogs
from opus_gui.main.controllers.dialogs.message_box import MessageBox
from opus_gui.util.convenience import create_qt_action
from opus_gui.util.icon_library import IconLibrary

from opus_core.variables.dependency_query import DependencyChart
from opus_gui.general_manager.controllers.dependency_viewer import DependencyViewer
from opus_core.third_party.pydot import InvocationException

class VariableLibrary(QDialog, Ui_VariableLibrary):

    def __init__(self, project, parent_widget=None):
        QDialog.__init__(self, parent_widget, Qt.Window)
        self.setupUi(self)
        self.project = project
        # Change PICK MODE to true for old school selector
        self.view = VariablesTableView(pick_mode = False, parent_widget = self)
        self.original_nodes = set()
        self.cancel_validation_flag = {'value': False}
        self.model = None
        self.problem_variables = []

        self.initialize()
        self.table_container.addWidget(self.view)

        # Automatically update the save button state on model data change
        custom_update_signal = SIGNAL('model_changed')
        self.connect(self.model, custom_update_signal, self._update_apply_button)
        # Automatically enable or disable the validate selected vars button
        def on_sel_change(dummy_a, dummy_b):
            if self.view.pick_mode:
                enabled = len([var for var in self.model if var['selected']]) > 0
            else:
                enabled = len(self.view.selectedIndexes()) > 0
            self.pb_validate_selected.setEnabled(enabled)
        sel_changed = SIGNAL('selectionChanged(const QItemSelection&,const QItemSelection&)')
        self.connect(self.view.selectionModel(), sel_changed, on_sel_change)

        # Double clicking an item in the table brings up the editor
        dbl_click = SIGNAL('doubleClicked(QModelIndex)')
        def edit_wrapper(index):
            variable = self.model.variables[index.row()]
            self._edit_variable(variable)
        self.connect(self.view, dbl_click, edit_wrapper)

        # Explicit event handlers
        click = SIGNAL('released()')
        def apply_and_close():
            self._apply_variable_changes()
            self.accept()
        self.connect(self.pb_apply_and_close, click, apply_and_close)
        self.connect(self.pb_apply, click, self._apply_variable_changes)
        self.connect(self.pb_create_new, click, self._add_variable)
        self.connect(self.pb_problems, click, self._show_problem_variables)

        def cancel_validation(): self.cancel_validation_flag['value'] = True
        self.connect(self.pb_cancel_validation, click, cancel_validation)
        signal = SIGNAL('customContextMenuRequested(const QPoint &)')
        self.connect(self.view, signal, self.on_table_right_clicked)

        self.validator = VariableValidator(self.project)
        self.editor = VariableEditor(self)

    def _update_apply_button(self):
        self.pb_apply.setEnabled(self.model.dirty)

    def initialize(self):
        ''' override the default show to setup the library to current project variables '''
        # reset the variable library to reflect the current state of expression library in xml
        nodes_per_dataset = get_variable_nodes_per_dataset(self.project)
        variables = []
        all_original_nodes = set()
        for dataset in nodes_per_dataset:
            for variable_node in nodes_per_dataset[dataset]:
                new_variable = variable_from_node(variable_node)
                new_variable['originalnode'] = variable_node
                variables.append(new_variable)
                all_original_nodes.add(variable_node) # save original values for comparison
        self.original_nodes = all_original_nodes
        self.cancel_validation_flag = {'value': False}
        self.model = VariablesTableModel(project = self.project, variables = variables,
                                         parent_widget = self.view)
        self.view.setModel(self.model)
        self.model.re_sort()
        self._update_apply_button()

        self.group_progress.setVisible(False)
        self.pb_problems.setIcon(IconLibrary.icon('warning_small'))
        self.pb_problems.setAttribute(Qt.WA_AlwaysShowToolTips)
        self._set_problem_variables([])

    def _set_problem_variables(self, list_of_problem_variables):
        '''
        stores the list of problematic variables and updates the
        problem button to reflect the change
        '''
        self.problem_variables = list_of_problem_variables
        if self.problem_variables:
            self.pb_problems.setText('%d' % len(self.problem_variables))

        else:
            self.pb_problems.setText('')
            txt = "Last validation didn't discover any problems with the tested variables"
            self.pb_problems.setToolTip(txt)

        self.pb_problems.setEnabled(not not self.problem_variables)
        if self.problem_variables:
            self.pb_problems.setText('%d' % len(self.problem_variables))
            txt = 'Discovered problems with %d of the variables' % len(self.problem_variables)
            self.pb_problems.setToolTip(txt)
        else:
            self.pb_problems.setText('')

    def _show_problem_variables(self):
        ''' shows the current list of problem variables '''
        if not self.problem_variables:
            MessageBox.information(self, 'All tested variables passed.')
            return

        msg = '<qt>'
        for dummy, err_msg in self.problem_variables:
            msg += '<br/>'.join(err_msg)
            msg += '<br/><br/>'
        msg += '</qt>'
        txt = 'Found problems with %d of the variables' % len(self.problem_variables)
        MessageBox.warning(self, txt, msg)

    def _apply_variable_changes(self):
        ''' apply the changes the user made to the expression library '''
        # Case  XML (before)     Editor (after)   Change     Action
        # ----------------------------------------------------------
        #  A    <none>           local            created    create
        #  B    local            inherited        reverted   delete
        #  C    local            <none>           deleted    delete

        # TODO: also check into the possibility that an inherited variable can have it's name
        # changed (in this case don't overwrite the orginala variable's name. Instead create a new
        # variable with the new name.

        dirty_variables = [var for var in self.model.variables if var['dirty']]
        # case A
        create_set = [var for var in dirty_variables if var['originalnode'] is None]
        delete_set = []
        for xml_node in self.original_nodes:
            if xml_node.get('inherited') is not None: # only care about local or shadowing nodes
                continue
            for variable in self.model.variables:
                if variable['originalnode'] is xml_node: # original is represented in variable list
                    if variable['inherited']:
                        delete_set.append(xml_node) # Case B
                    break # stop looking
            else: # did not find node
                delete_set.append(xml_node) # case C
        # the rest of the variables should just be updated
        update_set = [var for var in dirty_variables if
                      not var['originalnode'] in delete_set and var not in create_set]

        # Apply the changes to each set of nodes
        expression_lib = self.project.find('general/expression_library')
        for variable in create_set:
            # print 'CREATE SET ', variable
            node = node_from_variable(variable)
            # print '  node', node
            self.project.insert_node(node, expression_lib)

        for variable in update_set:
            node = node_from_variable(variable)
            original_node = variable['originalnode'] # reference to the actual XML node
            # print 'UPDATE SET %s (original %s)' %(variable['name'], original_node)
            self.project.make_local(original_node)
            for key in node.attrib:
                if not key == 'inherited':
                    original_node.set(key, node.get(key))
                    # print '   copy key %s (=%s)' %(key, node.get(key))
            original_node.text = node.text

        for node in delete_set:
            # print 'DELETE SET %s' % (node)
            self.project.delete_node(node)
        self.initialize()
        return True

    def _edit_variable(self, variable):
        self.editor.init_for_variable(variable, self.validator)
        if self.editor.exec_() == self.editor.Accepted:
            edited_var = self.editor.variable
            for key in edited_var:
                variable[key] = edited_var[key]
            if edited_var['dirty']:
                self.model.dirty = True
            self._update_apply_button()

    def _add_variable(self, base_on_variable = None):
        var = create_empty_variable()
        if base_on_variable is not None:
            for key in VariablesTableModel.VARIABLE_NON_METADATA_KEYS:
                var[key] = base_on_variable[key]
            var['name'] += '_copy' #  TODO this name is not guaranteed to be unique!

        self.editor.init_for_variable(var, self.validator)
        if self.editor.exec_() == self.editor.Accepted:
            new_variable = self.editor.variable
            self.model.add_variable(new_variable)
            self._update_apply_button()

    def _view_dependencies(self, variable):
        chart = DependencyChart(self.project.xml_config)
        dialog = DependencyViewer(self)
        try:
            chart.graph_variable("temp", str(variable['definition']), False)
            dialog.show_graph('temp.png', variable['name'])
            dialog.show()
        except InvocationException:
            dialog.show_error_message()

    def update_validation_progress(self, ratio):
        ''' callback to show validation progress '''
        ratio = 1.0 if ratio > 1.0 else ratio
        self.progress_validation.setValue(ratio * 100)
        self.progress_validation.repaint()

    def on_table_right_clicked(self, point):
        ''' handler for the when users right click on table view '''
        index = self.view.indexAt(point)
        if not index.isValid:
            return
        self.view.setCurrentIndex(index)
        var = self.model.variables[index.row()]
        menu = QMenu(self.view)

        # Edit variable action
        p = ('edit', 'Edit <b>%s</b>' % var['name'], lambda x=var: self._edit_variable(x), self)
        edit_action = create_qt_action(*p)
        font = QFont()
        font.setBold(True)
        edit_action.setFont(font)
        # Clone variable action
        p = ('clone', 'Create new variable based on this', lambda x=var: self._add_variable(x), self)
        clone_action = create_qt_action(*p)
        def make_local(var = var):
            if var['inherited']:
                var['dirty'] = True
                var['inherited'] = None
                self.model.dirty = True
            self._update_apply_button()
        def delete_var(var = var):
            self.model.delete_variable(var)
            self._update_apply_button()
        p = ('make_local', 'Make local', make_local, self)
        make_local_action = create_qt_action(*p)
        p = ('delete', 'Delete %s' % var['name'], delete_var, self)
        delete_action = create_qt_action(*p)
        p = ('revert', 'Revert %s to inherited' % var['name'], delete_var, self)
        revert_action = create_qt_action(*p)

        # check to see if we have graphviz installed
        p = ('zoom', 'View dependencies', lambda x=var: self._view_dependencies(x), self)
        view_dependencies_action = create_qt_action(*p)

        if var['inherited']:
            menu.addAction(make_local_action)
            menu.addAction(clone_action)
            menu.addAction(view_dependencies_action)
        else:
            menu.addAction(edit_action)
            menu.addAction(clone_action)
            menu.addSeparator()
            # if the node in the table is local, but the original is inherited OR
            # if the original node is shadowing an inhertied node, allow user to 'revert'
            # instead of 'delete'. Read more about prototype nodes in opus_project.py.
            if var['originalnode'] is None:
                menu.addAction(delete_action)
            else:
                prototype_node = self.project.get_prototype_node(var['originalnode'])
                if var['originalnode'].get('inherited') or \
                    (prototype_node is not None and prototype_node.get('inherited')):
                    # This action will revert the node to the parent state. Show the values
                    # that it will revert to
                    revert_action.setToolTip('Revert %s to Name: %s, Definition: %s' %
                                             (var['name'], prototype_node.get('name'), prototype_node.text))
                    menu.addAction(revert_action)
                else:
                    menu.addAction(delete_action)
            menu.addAction(view_dependencies_action)

        # Menu constructed, present to user
        if not menu.isEmpty():
            menu.exec_(QCursor.pos())

    def check_syntax(self, variable):
        ''' validates the selected variable '''
        print 'TODO: validate', variable['name']

    def check_data(self, variable):
        ''' check the selected variable against data '''
        print 'TODO: check against data', variable['name']


# AUTO WIDGET EVENT HANDLERS

    def on_pb_close_released(self):
        ''' event handler for when user clicks the close button '''
        if self.model.dirty:
            question = 'Do you want to apply your changes before closing?'
            user_answer = common_dialogs.apply_before_close(question)
            if user_answer == common_dialogs.YES:
                if not self._apply_variable_changes(): return
                self.close()
            elif user_answer == common_dialogs.NO:
                self.close()
            else:
                return
        else:
            self.close()

    def on_pb_apply_release(self):
        ''' event handler for when the user clicks the save button '''
        self._apply_variable_changes()
        self.close()

    def on_pb_validate_selected_released(self):
        ''' User clicked the validate selected button '''
        # Get all the selected variables
        selected_rows = set()
        map(selected_rows.add, [i.row() for i in self.view.selectedIndexes()])

        # Setup GUI for batch run
        self.pb_cancel_validation.setEnabled(True)
        self._set_problem_variables([])
        self.progress_validation.setValue(0)
        self.group_progress.setVisible(True)
        self.view.setEnabled(False) # disable selecting variables during run
        self.group_progress.setTitle('Validating %d variables...' % len(selected_rows))

        # Batch process the selected variables
        variables = [self.model.variables[i] for i in selected_rows]
        func = self.validator.check_data_errors
        var_key = 'dataerror'
        callback = self.update_validation_progress
        cancel_flag = self.cancel_validation_flag
        results = variable_batch_check(variables = variables,
                                       validator_func = func,
                                       variable_key = var_key,
                                       progress_callback = callback,
                                       cancel_flag = cancel_flag)

        # Setup GUI for investigating results
        self.pb_cancel_validation.setEnabled(False)
        self.progress_validation.setValue(100)
        self.view.setEnabled(True)
        failed_variables = [(var, msg) for (var, flag, msg) in results if flag is False]
        self._set_problem_variables(failed_variables)
        self._show_problem_variables()
        self.group_progress.setVisible(False)
        if failed_variables:
            self.pb_problems.setFocus()

