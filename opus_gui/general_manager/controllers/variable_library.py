# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt5.QtWidgets import QDialog, QMenu
from PyQt5.QtGui import QCursor, QFont
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

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
from opus_gui.util.convenience import create_qt_action, get_unique_name
from opus_gui.util.icon_library import IconLibrary

from opus_core.variables.variable_factory import VariableFactory
from opus_core.variables.dependency_query import DependencyChart
from opus_gui.general_manager.controllers.dependency_viewer import DependencyViewer
from opus_core.third_party.pydot import InvocationException
from opus_gui.main.controllers.instance_handlers import get_mainwindow_instance
from opus_gui.main.controllers.instance_handlers import update_mainwindow_savestate

class VariableLibrary(QDialog, Ui_VariableLibrary):

    '''
    An editor for creating and modifying variables in the expression library.
    Causes mainwindow to emit signal 'variables_updated' whenever changes have been applied.
    '''

    def __init__(self, project, parent_widget=None):
        QDialog.__init__(self, parent_widget, Qt.Window)
        self.setupUi(self)
        self.project = project
        # Change PICK MODE to true for old school selector
        self.variables_table = VariablesTableView(parent_widget = self)
        self.original_nodes = set()
        self.cancel_validation_flag = {'value': False}
        self.model = None
        self.problem_variables = []

        self.pb_create_new.setIcon(IconLibrary.icon('add'))

        self.initialize()
        self.table_container.addWidget(self.variables_table)

        # Automatically update the save button state on model data change
        self.connect(self.model, pyqtSignal('model_changed'), self._update_apply_button)

        # Automatically enable or disable the validate selected vars button
        def on_sel_change(dummy_a, dummy_b):
            enabled = len(self.variables_table.selectedIndexes()) > 0
            self.pb_validate_selected.setEnabled(enabled)
        sel_changed = pyqtSignal('selectionChanged(const QItemSelection&,const QItemSelection&)')
        self.connect(self.variables_table.selectionModel(), sel_changed, on_sel_change)

        # Double clicking an item in the table brings up the editor
        def edit_wrapper(index):
            variable = self.model.variables[index.row()]
            if not variable['inherited']:
                self._edit_variable(variable)
        self.connect(self.variables_table, pyqtSignal('doubleClicked(QModelIndex)'), edit_wrapper)

        def apply_and_close():
            self._apply_variable_changes()
            self.accept()
        def cancel_validation():
            self.cancel_validation_flag['value'] = True
        self.connect(self.pb_apply_and_close, pyqtSignal("clicked()"), apply_and_close)
        self.connect(self.pb_apply, pyqtSignal("clicked()"), self._apply_variable_changes)
        self.connect(self.pb_create_new, pyqtSignal("clicked()"), self._add_variable)
        self.connect(self.pb_problems, pyqtSignal("clicked()"), self._show_problem_variables)
        self.connect(self.pb_cancel_validation, pyqtSignal("clicked()"), cancel_validation)

        signal = pyqtSignal('customContextMenuRequested(const QPoint &)')
        self.connect(self.variables_table, signal, self._show_right_click_menu)

        signal = pyqtSignal('currentIndexChanged(int)')
        self.connect(self.cbo_dataset_filter, signal, lambda x: self._set_dataset_filter())

        self.validator = VariableValidator(self.project)
        self.editor = VariableEditor(self)

    def initialize(self):
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

        # to avoid quirky behavior when applying changes, store the column widths and restore them
        # after the model update
        col_widths = [self.variables_table.columnWidth(col) for col in range(5)]

        # bind to self to prevent PyQt from "losing" the object ref
        self.model = VariablesTableModel(project = self.project, variables = variables,
                                         parent_widget = self.variables_table)
        self.variables_table.setModel(self.model)
        self.model.re_sort()
        self.connect(self.model, pyqtSignal('layoutChanged()'), self.variables_table.resizeRowsToContents)
        self._update_apply_button()

        self.group_progress.setVisible(False)
        self.pb_problems.setIcon(IconLibrary.icon('warning_small'))
        self.pb_problems.setAttribute(Qt.WA_AlwaysShowToolTips)
        self._set_problem_variables([])
        self._update_dataset_filter()

        # use the inital size if the column widths is all zeroes
        if sum(abs(w) for w in col_widths) == 0:
            col_widths = [195, 80, 45, 50, -1]
        for col in range(5):
            if col_widths[col] > 0:
                self.variables_table.setColumnWidth(col, col_widths[col])
        self.variables_table.resizeRowsToContents()

    def update_validation_progress(self, ratio):
        ''' callback to show validation progress '''
        ratio = 1.0 if ratio > 1.0 else ratio
        self.progress_validation.setValue(ratio * 100)
        self.progress_validation.repaint()

    def _update_apply_button(self):
        self.pb_apply.setEnabled(self.model.dirty)
        self.pb_apply_and_close.setEnabled(self.model.dirty)

    def _update_dataset_filter(self):
        '''repopulate the dataset filter combobox with existing datasets'''
        all_datasets = set()
        for dataset, _ in self.model.get_variables():
            all_datasets.add(dataset)
        prev_selected_name = self.cbo_dataset_filter.currentText()
        self.cbo_dataset_filter.clear()
        self.cbo_dataset_filter.addItem('[All datasets]')
        for dataset_name in all_datasets:
            self.cbo_dataset_filter.addItem(dataset_name)

        refound_index = self.cbo_dataset_filter.findText(prev_selected_name)
        if refound_index > -1:
            self.cbo_dataset_filter.setCurrentIndex(refound_index)
        else:
            self.cbo_dataset_filter.setCurrentIndex(0)

    def _set_dataset_filter(self):
        index = self.cbo_dataset_filter.currentIndex()
        if index == 0:
            self.model.set_dataset_filter(None)
        else:
            self.model.set_dataset_filter(str(self.cbo_dataset_filter.currentText()))

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
        # TODO: also check into the possibility that an inherited variable can have its name
        # changed (in this case don't overwrite the original variable's name. Instead create a new
        # variable with the new name.)

        dirty_variables = [var for var in self.model.all_variables if var['dirty']]

        # partition dirty variables into create, delete and update sets
        create_set = [var for var in dirty_variables if var['originalnode'] is None]
        delete_set = [var for var in dirty_variables if var['delete'] and var['originalnode'] is not None]
        # the rest of the variables should just be updated
        update_set = [var for var in dirty_variables if
                      not var['originalnode'] in delete_set and var not in create_set]
        
        # verify if we have a partition
        assert(set([str(var) for var in create_set]) | set([str(var) for var in delete_set]) | set([str(var) for var in update_set]) 
               == set([str(var) for var in dirty_variables]))
        assert(set([str(var) for var in create_set]) & set([str(var) for var in delete_set]) & set([str(var) for var in update_set]) 
               == set())

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
            if 'dataset' in original_node.attrib:
                del original_node.attrib['dataset']
            original_node.text = node.text

        for variable in delete_set:
            # print 'DELETE SET %s' % (node)
            self.project.delete_node(variable['originalnode'])
        self.initialize()
        something_changed = bool(update_set or create_set or delete_set)
        update_mainwindow_savestate(something_changed)
        get_mainwindow_instance().emit(pyqtSignal('variables_updated'))
        return True

    def _edit_variable(self, variable):
        self.editor.init_for_variable(variable, self.validator, self.model.get_variables())
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
            name, dataset = var['name'], var['dataset']
            var['name'] = get_unique_name(name, self.model.get_variable_names_in_dataset(dataset))

        self.editor.init_for_variable(var, self.validator, self.model.get_variables())
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
            #dialog.show_error_message()
            chart.print_dependencies(str(variable['definition']))

    def _show_right_click_menu(self, point):
        ''' handler for the when users right click on table variables_table '''
        index = self.variables_table.indexAt(point)
        if not index.isValid:
            return
        self.variables_table.setCurrentIndex(index)
        var = self.model.variables[index.row()]
        menu = QMenu(self.variables_table)

        # Edit variable action
        p = ('edit', 'Edit %s' % var['name'], lambda x=var: self._edit_variable(x), self)
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
#            menu.addAction(edit_action)
            menu.addAction(make_local_action)
            menu.addAction(clone_action)
            menu.addSeparator()
            menu.addAction(view_dependencies_action)
        else:
            menu.addAction(edit_action)
            menu.addAction(clone_action)
            menu.addSeparator()
            # if the node in the table is local, but the original is inherited OR
            # if the original node is shadowing an inherited node, allow user to 'revert'
            # instead of 'delete'. Read more about prototype nodes in opus_project.py.
            if var['originalnode'] is None:
                menu.addAction(delete_action)
            else:
                prototype_node = self.project.get_prototype_node(var['originalnode'])
                if var['originalnode'].get('inherited') or \
                    (prototype_node is not None and prototype_node.get('inherited')):
                    # This action will revert the node to the parent state. Show the values
                    # that it will revert to
                    tt = ('Revert %s to Name: %s, Definition: %s' % (var['name'],
                                                                     prototype_node.get('name'),
                                                                     prototype_node.text))
                    revert_action.setToolTip(tt)
                    menu.addAction(revert_action)
                else:
                    menu.addAction(delete_action)
            menu.addAction(view_dependencies_action)

        # Menu constructed, present to user
        if not menu.isEmpty():
            menu.exec_(QCursor.pos())

# AUTO WIDGET EVENT HANDLERS

    @pyqtSlot()
    def on_pb_close_clicked(self):
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

    @pyqtSlot()
    def on_pb_validate_selected_clicked(self):
        ''' User clicked the validate selected button '''
        # Get all the selected variables
        selected_rows = set()
        list(map(selected_rows.add, [i.row() for i in self.variables_table.selectedIndexes()]))

        # Setup GUI for batch run
        self.pb_cancel_validation.setEnabled(True)
        self._set_problem_variables([])
        self.progress_validation.setValue(0)
        self.group_progress.setVisible(True)
        self.variables_table.setEnabled(False) # disable selecting variables during run
        self.group_progress.setTitle('Validating %d variables...' % len(selected_rows))
        
        # Set the expression library in VariableFactory to the variables for this configuration.
        # We need to get this from the VariablesTableModel rather than from the xml configuration
        # since newly added variables may not yet have been saved to the xml configuration but we
        # still want to check them.
        VariableFactory().set_expression_library(self.model.get_variables_dict())

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
        self.variables_table.setEnabled(True)
        failed_variables = [(var, msg) for (var, flag, msg) in results if flag is False]
        self._set_problem_variables(failed_variables)
        self._show_problem_variables()
        self.group_progress.setVisible(False)
        if failed_variables:
            self.pb_problems.setFocus()

