# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE
from lxml import etree
from opus_gui.util import common_dialogs

import copy
from lxml.etree import SubElement

from PyQt4 import QtGui, QtCore

from opus_gui.util.convenience import create_qt_action
from opus_core.configurations.xml_configuration import get_variable_name
from opus_gui.util.convenience import dictionary_to_menu, hide_widget_on_value_change
from opus_gui.general_manager.general_manager_functions import get_built_in_variable_nodes, get_built_in_constant_node
from opus_gui.general_manager.general_manager_functions import get_variable_nodes_per_dataset

from opus_gui.util.icon_library import IconLibrary
from opus_gui.main.controllers.dialogs.message_box import MessageBox
from opus_gui.models_manager.views.ui_submodel_editor import Ui_SubModelEditor
from opus_gui.models_manager.models.submodel_structure_item import SubmodelStructureItem
from opus_gui.models_manager.models.variable_selector_table_model import VariableSelectorTableModel

class SubModelEditor(QtGui.QDialog, Ui_SubModelEditor):

    '''
    Submodel Editing dialog.
    The editor support three different structures of submodels:
    I call these structures Plain Structures, Equation Structures and Nested Structures
    The Plain Structures are submodels that only have a variable list.
    The Equation Structures are submodels that have one or more <equation>, with each equation
    having it's own variable list.
    The Nested Structures have one or more levels of <nest>:s. Each nest can either have an
    <equation> (that in turn have a variable list) or another nest.
    Nests can not have variable lists themselves.

    The assignment of variables happen on either the different <equation>:s (in the case of
    Equation Structures and Nested Structures) or on the submodel itself if it has a Plain Structure

    The GUI dialog is made somewhat simpler if the submodel has a Plain Structure, as some
    functionality is not needed in this case.
    '''

    def __init__(self, project, parent_widget = None):
        QtGui.QDialog.__init__(self, parent_widget)
        self.setupUi(self)


        self.project = project
        self.submodel_node = None # the submodel that we are editing (a copy of actual submodel node)
        self.active_variables_node = None
        self.selector_table_model = VariableSelectorTableModel(project)

        self.tree_structure_editor.header().setStretchLastSection(True)
        self.tree_structure_editor.header().setMinimumWidth(50)

        self.frame_name_warning.setVisible(False)
        self.pb_remove_variable.setVisible(False)
        # hide the name warning when the user edit the name
        hide_widget_on_value_change(self.lbl_name_warning, self.le_name)

        S = QtCore.SIGNAL # temporarily use a shorter name for all the connections below

        self.connect(self.selector_table_model, S('layoutChanged()'), self._selector_model_column_resize)
        signal = S("currentItemChanged(QTreeWidgetItem*, QTreeWidgetItem*)")
        self.connect(self.tree_structure_selector, signal, self._change_structure_node)
        signal = S('currentIndexChanged(int)')
        self.connect(self.cbo_dataset_filter, signal, self._update_available_variables)

        # Setup Variable Selector Table
        self.table_selected_variables.setModel(self.selector_table_model)
        self.table_selected_variables.horizontalHeader().setStretchLastSection(True)
        self.table_selected_variables.verticalHeader().hide()
        self.table_selected_variables.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        signal = S("customContextMenuRequested(const QPoint &)")
        self.connect(self.table_selected_variables, signal, self._right_click_variables)

        f_create_nest = lambda x = 'nest': self.tree_structure_editor.create_structure_node(x)
        f_create_equation = lambda x = 'equation': self.tree_structure_editor.create_structure_node(x)
        self.connect(self.pb_create_nest, S('released()'), f_create_nest)
        self.connect(self.pb_create_equation, S('released()'), f_create_equation)

        self.connect(self.buttonBox, S('rejected()'), self.reject)
        self.connect(self.buttonBox, S('accepted()'), self.validate_submodel_and_accept)
        # the label "OK" can be confusing when switching between the structure
        # editor and the variable selector. Some users clicked "OK" to confirm the structure changes
        # Therefore we set a more explicit label.
        self.buttonBox.button(self.buttonBox.Ok).setText('Save and Close')

        signal = S('structure_changed')
        self.connect(self.tree_structure_editor, signal, self._update_submodel_structure_trees)
        signal = S('clicked()')
        self.connect(self.pb_update_model_structure, signal, self.update_model_nested_structure)

    def _lookup_model_node_for(self, node):
        ''' seek up the tree structure for the <model> parent of the submodel node '''
        while node is not None:
            if node.tag == 'model':
                return node
            node = node.getparent()
        return None

    def _change_structure_node(self, new_item, old_item):
        self._set_variable_list_node(new_item.variable_list() if new_item else None)

    def _show_name_warning(self, text):
        self.lbl_name_warning.setText(text)
        self.frame_name_warning.setVisible(True)
        self.le_name.selectAll()
        self.le_name.setFocus()

    def _set_variable_list_node(self, variable_list_node):
        ''' populate the list of selected variables with the variable_spec nodes of the given
        variable_list_node '''
        # "save' the changes to the previously edited variable_list before changing active node
        self._apply_selected_variables(self.active_variables_node)
        self.active_variables_node = variable_list_node

        self.selector_table_model.clear()

        if variable_list_node is not None:
            for variable_spec_node in variable_list_node:
                self.selector_table_model.add_variable_spec_node(variable_spec_node)
            self.table_selected_variables.setEnabled(True)
            self._selector_model_column_resize()
            self.pb_show_picker.setEnabled(True)
        else:
            self.table_selected_variables.setEnabled(False)
            self.pb_show_picker.setEnabled(False)

    def _apply_selected_variables(self, variables_node):
        if variables_node is None:
            return
        self.selector_table_model.apply_selected_variables(variables_node)

    def _update_submodel_structure_trees(self):
        ''' updates both of the tree widgets to show the structure of self.submodel_node '''
        self.tree_structure_selector.clear()
        self.tree_structure_editor.clear()
        self._populate_structure_tree(self.submodel_node, False, self.tree_structure_selector)
        self._populate_structure_tree(self.submodel_node, True, self.tree_structure_editor)

        for tree_widget in [self.tree_structure_editor, self.tree_structure_selector]:
            tree_widget.resizeColumnToContents(0)
            tree_widget.resizeColumnToContents(1)

        # make the GUI a little simpler if the submodel is "plain" (i.e has no structural elements)
        # by automatically hiding the "structure selector" tree
        if self._in_simple_mode():
            self.split_struct_variables.setSizes([0, 10]) # hide structure selector
            # auto select the only variable_list
            self._set_variable_list_node(self.submodel_node.find('variable_list'))
        else:
            # make sure that the structure widget is visible
            if not self.pb_show_picker.isChecked():
                self.stack_struct_picker.setCurrentIndex(1)
            self.split_struct_variables.setSizes([10, 10])
            self._set_variable_list_node(None)
            # auto select the first structural element
            item = self.tree_structure_selector.topLevelItem(0)
            self.tree_structure_selector.setCurrentItem(item)

    def _populate_structure_tree(self, parent_node, editable, parent_widget):
        ''' adds all <nest> nodes and <equation> nodes of parent_node to parent_widget. Recurses
        down added <nest> nodes. '''
        nest_nodes = parent_node.findall('nest')
        equation_nodes = parent_node.findall('equation')
        # recursively add nest nodes
        for nest_node in nest_nodes:
            item = SubmodelStructureItem(nest_node, editable, parent_widget)
            item.setExpanded(True)
            self._populate_structure_tree(nest_node, editable, item)
        # add any equations
        for equation_node in equation_nodes:
            item = SubmodelStructureItem(equation_node, editable, parent_widget)

    def _selector_model_column_resize(self):
        ''' updates the column widths whenever there has been a layout change to the model '''
        self.selector_table_model.sort_variables_by_name()
        self.table_selected_variables.resizeRowsToContents()
        for col in [0, 3, 4]:
            self.table_selected_variables.resizeColumnToContents(col)

    def _validate_names(self, show_error_message = False):
        ''' go through all nest and equation names and ensure that there are no collisions.
        Returns True if all the names are valid and False otherwise.
        If @param show_error_message is True an error message of the name errors is displayed.'''
        # Check for colliding names among the nest and equations
        colliding_names = set()
        nodes_to_inspect = self.submodel_node.findall('.//nest')
        nodes_to_inspect.extend(self.submodel_node.findall('.//equation'))
        for inspected_node in nodes_to_inspect:
            # get all sibling names with the same tag
            sibling_names = [node.get('name') for node in inspected_node.getparent() if
                             node is not inspected_node and node.tag == inspected_node.tag]
            # if there is a name collision, add the name to the set of found colliding names
            if inspected_node.get('name') in sibling_names:
                parent_node = inspected_node.getparent()
                if parent_node.tag == 'nest':
                    desc = '&lt;%s&gt;/%s' % (parent_node.get('name'), inspected_node.get('name'))
                else:
                    desc = '%s' % inspected_node.get('name')
                colliding_names.add(desc)

        # the concept of colliding names might be confusing so we want to be clear on what is
        # happening and (more importantly) how to solve it
        if colliding_names:
            if not show_error_message:
                return False
            str_collide_list = ''.join(['<li>%s</li>\n' % name for name in colliding_names])
            short_msg = 'Name collisions found.'
            longer_msg = ''' <qt> Colliding names:
            <b> <ul> %s </ul> </b>
            <p>A name collision is when there are two items with the same name, the same type and the same level.</p>
            For example:
            <ul>
                <li>MY_NEST</li>
                <li><ul><li>MY_EQUATION</li><li>MY_EQUATION</li></ul></li>
            </ul>
            <p>will cause a name collision, while this example;</p>
            <ul>
                <li>MY_NEST</li>
                <li><ul><li>MY_EQUATION</li></ul></li>
                <li>MY_OTHER_NEST</li> <li>
                <ul><li>MY_EQUATION</li></ul></li>
            </ul>
            <p>is fine since the two equations with the same name are on different levels.</p>
            <p>To correct this error please give unique names for the above mentioned equations
            and/or nests.</p></qt>'''% str_collide_list
            MessageBox.warning(self, short_msg, longer_msg)
            return False
        return True

    def _create_nested_structure_xml(self, nest_node, counter):
        ''' create and return an XML representation of the nested_structure for the given node '''
        # quickie method to get the nest_id or equiation_id from a node dep. on it's tag
        the_id = lambda x: str(x.get('nest_id')) if x.tag == 'nest' else str(x.get('equation_id'))

        # the submodel node is passed in the first time this method is called, so we create the
        # special containing node then
        if nest_node.tag == 'submodel':
            created_nest_node = etree.Element('argument', {'name': 'nested_structure',
                                                           'type': 'dictionary'})
        else:
            attrib = {'name': the_id(nest_node),
                      'type': 'dictionary',
                      'parser_action': 'convert_key_to_integer'}
            created_nest_node = etree.Element('nest', attrib)

        if nest_node.find('nest') is not None: # decend into multiple levels of nests
            for nest_child_node in nest_node.findall('nest'):
                child_xml = self._create_nested_structure_xml(nest_child_node, counter)
                created_nest_node.append(child_xml)
        elif nest_node.get('number_of_samples') is not None:
            # auto generate a series of equation ID's
            num_of_samples = int(nest_node.get('number_of_samples'))
            id_start = counter['current count']
            counter['current count'] = id_end = id_start + num_of_samples
            index_range = range(id_start, id_end)
            created_nest_node.set('type', 'list')
            created_nest_node.text = repr(index_range)
        elif nest_node.find('equation') is not None:
            index_range = [int(the_id(x)) for x in nest_node.findall('equation')]
            created_nest_node.set('type', 'list')
            created_nest_node.text = repr(index_range)
        else:
            raise ValueError('Found empty nest without "number_of_samples" attribute or <equation> '
                             'child nodes (%s name=%s)' % (nest_node.tag, nest_node.get('name')))
        return created_nest_node

    def _create_add_variable_menu(self):
        # function to display variables in the popup menu
        def display_node(node, selected_nodes):
            if node in selected_nodes:
                return '(already selected) %s' % get_variable_name(node)
            return get_variable_name(node)
        # call back to only add unselected variables from the popup menu
        def add_if_unselected(node, selected_nodes):
            if not node in selected_nodes:
                self.add_variable(node)

        dataset_variable_nodes = get_variable_nodes_per_dataset(self.project)
        selected_names = map(get_variable_name, self.selector_table_model._variable_nodes)
        selected_nodes = []

        for variable_node_list in dataset_variable_nodes.values():
            for variable_node in variable_node_list:
                if get_variable_name(variable_node) in selected_names:
                    selected_nodes.append(variable_node)
            # sort by variable name
            variable_node_list.sort(lambda x, y: cmp(get_variable_name(x), get_variable_name(y)))
            # display selected items at the bottom
            for node in variable_node_list[:]:
                if node in selected_nodes:
                    variable_node_list.remove(node)
                    variable_node_list.insert(len(variable_node_list), node)

        display_func = lambda x, y = selected_nodes: display_node(x, y)
        callback = lambda x, y = selected_nodes: add_if_unselected(x, y)
        return dictionary_to_menu(source_dict = dataset_variable_nodes,
                                  callback = callback,
                                  display_func = display_func,
                                  parent_widget = self)

    def _right_click_variables(self, point):
        ''' construct and show an operations operations_menu when the user right clicks the variable selector '''
        operations_menu = QtGui.QMenu(self)
        add_variable_menu = self._create_add_variable_menu()
        add_variable_menu.setTitle('Add a variable')
        add_variable_menu.setIcon(IconLibrary.icon('add'))
        operations_menu.addMenu(add_variable_menu)

        index_under_cursor = self.table_selected_variables.indexAt(point)
        if index_under_cursor.isValid():
            row = index_under_cursor.row()
            variable_node = self.selector_table_model.get_variable(row)
            self.table_selected_variables.selectRow(row)
            action = create_qt_action(None, 'Remove %s' % get_variable_name(variable_node),
                                      self._remove_selected_variables,
                                      self.table_selected_variables)
            action.setIcon(IconLibrary.icon('delete'))
            operations_menu.addAction(action)
        else:
            # if the index is not valid -- assume that the user clicked the "white space" of the table
            pass
        operations_menu.exec_(QtGui.QCursor.pos())

    def _in_simple_mode(self):
        return self.tree_structure_selector.topLevelItemCount() == 0

    def _update_available_variables(self):
        # populate the list of available variables while considering A) what dataset filter the user
        # has selected, an d B) what variables that have already been selected)
        self.lst_available_variables.clear()
        if self.cbo_dataset_filter.currentIndex() > 0:
            dataset_filter = str(self.cbo_dataset_filter.currentText())
        else:
            dataset_filter = None
        selected_variable_names = [node.get('name') for node in self.selector_table_model._variable_nodes]

        available_variable_nodes = []
        variable_nodes_per_dataset = get_variable_nodes_per_dataset(self.project)

        if not dataset_filter: # take all variables
            for variable_nodes in variable_nodes_per_dataset.values():
                available_variable_nodes.extend(variable_nodes)
        else:
            available_variable_nodes = variable_nodes_per_dataset[dataset_filter]
        available_variable_nodes.append(get_built_in_constant_node())
        
        # filter already selected variables and show the list of available variables
        not_selected_variables = [var_node for var_node in available_variable_nodes if
                                  not var_node.get('name') in selected_variable_names]
        for variable_node in not_selected_variables:
            item = QtGui.QListWidgetItem(self.lst_available_variables)
            item.setIcon(IconLibrary.icon('variable'))
            item.node = variable_node # monkey in the node for adding later
            item.setText(get_variable_name(variable_node))
            self.lst_available_variables.addItem(item)
        self.lst_available_variables.sortItems()

    def _update_dataset_filter_list(self):
        # update the combo box list (keeping selection)
        variable_nodes_per_dataset = get_variable_nodes_per_dataset(self.project)
        pre_update_dataset_name = self.cbo_dataset_filter.currentText()
        self.cbo_dataset_filter.clear()
        self.cbo_dataset_filter.addItem('[All datasets]')
        for dataset_name in variable_nodes_per_dataset:
            if dataset_name is not None: # built ins are manually added
                self.cbo_dataset_filter.addItem(dataset_name)
        post_update_index = self.cbo_dataset_filter.findText(pre_update_dataset_name)
        if post_update_index > -1:
            self.cbo_dataset_filter.setCurrentIndex(post_update_index)

    def _remove_selected_variables(self):
        # delete the rows from highest to lowest so we don't change the row number when we delete
        # a row (i.e if we want to delete row 1 and 2 and start with one, then the row that was
        # number 2 will have become one and we will actually delete row number 3
        selected_indices = self.table_selected_variables.selectedIndexes()
        selected_rows = list(set([idx.row() for idx in selected_indices]))
        selected_rows.sort(reverse=True)
        for row in selected_rows:
            self.table_selected_variables.model().removeRow(row)
        self._update_available_variables()

    def _show_advanced_parameters(self, set_advanced_visible = None):
        # updates the selector table to show only the basic data if set_advanced_visible is True
        # otherwise all available data is shown
        if set_advanced_visible is None:
            set_advanced_visible = self.cb_show_advanced_parameters.isChecked()
        if set_advanced_visible:
            for column in range(5):
                self.table_selected_variables.showColumn(column)
        else:
            advanced_columns = [0, 2, 3, 4]
            for column in range(5):
                if column in advanced_columns:
                    self.table_selected_variables.hideColumn(column)
                else:
                    self.table_selected_variables.showColumn(column)

    def _set_picker_visible(self, visible):
        # shows / hides the variable picker
        # visible =
        if visible:
            self.stack_struct_picker.setCurrentIndex(0)
            if self._in_simple_mode():
                self.split_struct_variables.setSizes([1, 1])
            # hide unnecessary information while picking variables
            self._show_advanced_parameters(False)
        else:
            self.stack_struct_picker.setCurrentIndex(1)
            if self._in_simple_mode():
                self.split_struct_variables.setSizes([0, 10])
            self._show_advanced_parameters()
            # sometimes the table gets messed up when shown again so force refresh
            self.selector_table_model.emit(QtCore.SIGNAL("layoutChanged()"))
        self.cb_show_advanced_parameters.setEnabled(not visible)
        self.pb_remove_variable.setVisible(visible)
        self.pb_show_picker.setChecked(visible)

    def update_model_nested_structure(self, node = None):
        '''
        Create an XML representation to use for the argument "nested_structure" used by Nested Logit
        Models (NLM). The argument is used in the NLMs init() method.
        @param node submodel node to construct a nested structure from (default self.submodel_node)
        @raise RuntimeError: If the model node could not be updated
        @return the created nested_structure node (useful for tests)
        '''
        node = self.submodel_node if node is None else node
        if node.find('nest') is None: # can't create a nested structure if there are no nests
            return None
        counter = {'current count': 1} # pass object ref to keep increments down the recursive chain
        try:
            new_nested_structure_node = self._create_nested_structure_xml(node, counter)
        except ValueError, ex:
            MessageBox.error(self, 'Not all nests have equations assigned to them.', str(ex))
            return None
        model_node = self._lookup_model_node_for(node)
        if new_nested_structure_node is None or model_node is None:
            err_msg = 'Warning: Could not update the model nested node because:'
            if new_nested_structure_node is None:
                err_msg = err_msg + ' * the created "nested_structure" was empty'
            if model_node is None:
                err_msg = err_msg + ' * a parent <model> node to update could not be found'
            raise RuntimeError(err_msg)

        # replace existing nested_structure(s) with the new one
        init_node = model_node.find('structure/init/')
        for existing_nest_node in init_node.findall("argument[@name='nested_structure']"):
            init_node.remove(existing_nest_node)
        init_node.append(new_nested_structure_node)
        return new_nested_structure_node

    def init_for_submodel_node(self, submodel_node):
        ''' Setup up the dialog to edit (a copy of) the given submodel_node '''
        self.submodel_node = copy.deepcopy(submodel_node)
        # keep a reference to the parent node so we can always get an up-to-date list of taken names
        self._submodel_parent_node = submodel_node.getparent().getchildren()

        self.frame_name_warning.setVisible(False)

        # Populate the submodel info widgets
        submodel_name = submodel_node.get('name')
        if submodel_node.find('description') is not None:
            submodel_description = submodel_node.find('description').text.strip()
        else:
            submodel_description = ''
        submodel_id = int(submodel_node.get('submodel_id'))
        self.le_name.setText(submodel_name)
        self.le_description.setText(submodel_description)
        self.spin_id.setValue(submodel_id)

        self.tree_structure_editor.set_root_node(self.submodel_node)
        self._update_submodel_structure_trees()
        # We only want to enable the "Update Model Structure" button for NLMs.
        # We guess that is a NLM if it has a structure/init/nested_structure node
        model_node = self._lookup_model_node_for(submodel_node)
        path_to_nested_struct = "structure/init/argument[@name='nested_structure']"
        if model_node is not None and model_node.find(path_to_nested_struct) is not None:
            self.pb_update_model_structure.setEnabled(True)
        else:
            self.pb_update_model_structure.setEnabled(False)
        self._update_dataset_filter_list()
        self._show_advanced_parameters()
        self._set_picker_visible(False)


    def add_variable(self, variable_definition_node):
        ''' create a new variable_spec node based on a given variable_def node and add it '''
        self.selector_table_model.add_variable_from_definition_node(variable_definition_node)

    def on_tree_submodel_structure_currentItemChanged(self, current, previous):
        # change the variables of the selector table when the user clicks on a structure element
        # that has a variable list (i.e a <equation>)
        self._set_variable_list_node(current.node.find('variable_list') if current else None)

    def on_pb_help_on_released(self):
        QtGui.QWhatsThis.enterWhatsThisMode()

#    def on_pb_add_variable_released(self):
#
#        # Christoffer: adding variables is done using a temporary functionality (popup menu).
#        # I'll think of something nicer later, but at this point we can't really afford the
#        # vertical space that the former two-pane variable selector required.
#
#        # only enable adding variables when it makes sense
#        if not self.table_selected_variables.isEnabled():
#            return
#        menu = self._create_add_variable_menu()
#        menu.exec_(QtGui.QCursor.pos())

    def on_pb_show_picker_released(self):
        self._update_available_variables()
        self._set_picker_visible(self.pb_show_picker.isChecked())


    def on_pb_add_variable_released(self):
        selected_items = self.lst_available_variables.selectedItems()
        for item in selected_items:
            self.add_variable(item.node)
        self._update_available_variables()

    def on_pb_remove_variable_released(self):
        self._remove_selected_variables()

    def on_cb_show_advanced_parameters_released(self):
        self._show_advanced_parameters()
        self.selector_table_model.emit(QtCore.SIGNAL('layoutChanged()'))

    def on_pb_delete_struct_released(self):
        # delete the selected structure element
        # if the element is a non-empty nest, move all the child nodes to the root
        if self.tree_structure_editor.selectedItems():
            selected_item = self.tree_structure_editor.selectedItems()[0]
        else:
            return
        node = selected_item._node
        if node.tag == 'nest' and node.getchildren():
            # give the user to bail if before deleting non-empty nests
            question = ('Are you sure you want to delete the non empty nest %s?\n'
                'All child nests and equations will be deleted. There is no undo.' %
                node.get('name'))
            if not common_dialogs.user_is_sure(question, self):
                return

        self.tree_structure_editor.delete_struct_item(selected_item)

    def validate_submodel_and_accept(self):
        ''' clean up and validate the submodel node before accepting the dialog '''
        # collect the list of taken names (excluding the current name of the submodel) and see if
        # the user entered name is unique
        taken_names = [n.get('name') for n in self._submodel_parent_node]
        taken_names.remove(self.submodel_node.get('name'))
        entered_name = str(self.le_name.text())
        if entered_name in taken_names:
            self._show_name_warning('There is already a submodel named "%s" in this model.\n'
                                    'Please enter another name.' % entered_name)
            return 'name collision' # this return value is used for testing

        # apply changes made to the active variable list and setup the submodel node for delivery
        self._apply_selected_variables(self.active_variables_node)
        description = str(self.le_description.text())
        if description:
            description_node = self.submodel_node.find('description')
            if description_node is None:
                description_node = SubElement(self.submodel_node, 'description')
            description_node.text = description
        self.submodel_node.set('submodel_id', str(self.spin_id.value()))
        self.submodel_node.set('name', entered_name)

        self.accept()

if __name__ == '__main__':
    from opus_gui.tests.mockup_project import MockupOpusProject
    xml = '''
    <opus_project>
    <general>
      <expression_library>
          <variable name="zone.number_of_jobs" source="Python class" type="variable_definition" use="both">urbansim.zone.number_of_jobs</variable>
          <variable name="gridcell.population" source="Python class" type="variable_definition" use="both">urbansim.gridcell.population</variable>
          <variable name="gridcell.population_density" source="Python class" type="variable_definition" use="both">urbansim.gridcell.population_density</variable>
          <variable name="gridcell.ln_du" source="expression" type="variable_definition" use="model variable">ln(gridcell.residential_units)</variable>
          <variable name="gridcell.ln_duw" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.ln_residential_units_within_walking_distance</variable>
          <variable name="gridcell.pcthiwa" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.percent_high_income_households_within_walking_distance</variable>
          <variable name="gridcell.wetland" source="expression" type="variable_definition" use="model variable">gridcell.percent_wetland&gt;50</variable>
          <variable name="gridcell.cbdtrvl" source="Python class" type="variable_definition" use="model variable">eugene.gridcell.travel_time_hbw_am_drive_alone_to_220</variable>
          <variable name="gridcell.ln_impval" source="expression" type="variable_definition" use="model variable">ln(urbansim.gridcell.total_improvement_value)</variable>
          <variable name="gridcell.pctdevwal" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.percent_developed_within_walking_distance</variable>
          <variable name="constant" source="expression" type="variable_definition" use="model variable" />
          <variable name="gridcell.ln_hwy" source="expression" type="variable_definition" use="model variable">ln(gridcell.distance_to_highway)</variable>
          <variable name="gridcell.flood" source="expression" type="variable_definition" use="model variable">gridcell.percent_floodplain&gt;50</variable>
          <variable name="gridcell.hwy600" source="expression" type="variable_definition" use="model variable">gridcell.distance_to_highway&lt;600</variable>
          <variable name="gridcell.hwy300" source="expression" type="variable_definition" use="model variable">gridcell.distance_to_highway&lt;300</variable>
          <variable name="gridcell.land_value" source="expression" type="variable_definition" use="indicator">gridcell.residential_land_value+gridcell.nonresidential_land_value</variable>
          <variable name="gridcell.ble_rew" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.ln_retail_sector_employment_within_walking_distance</variable>
          <variable name="job_x_gridcell.ble_saw" source="Python class" type="variable_definition" use="model variable">urbansim.job_x_gridcell.ln_same_sector_employment_within_walking_distance</variable>
          <variable name="household_x_gridcell.ctir" source="Python class" type="variable_definition" use="model variable">urbansim.household_x_gridcell.cost_to_income_ratio</variable>
          <variable name="gridcell.bpliw" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.percent_low_income_households_within_walking_distance</variable>
          <variable name="gridcell.hwy" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.is_near_highway</variable>
          <variable name="gridcell.ldevsfi" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.ln_developable_industrial_sqft_capacity</variable>
          <variable name="gridcell.sfc_0" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.has_0_commercial_sqft</variable>
          <variable name="gridcell.bltv" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.ln_total_value</variable>
          <variable name="gridcell.bldhw" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.ln_distance_to_highway</variable>
          <variable name="gridcell.bltlv" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.ln_total_land_value</variable>
          <variable name="household_x_gridcell.plihwwdihi" source="Python class" type="variable_definition" use="model variable">urbansim.household_x_gridcell.percent_low_income_households_within_walking_distance_if_high_income</variable>
          <variable name="household_x_gridcell.ruwhhc" source="Python class" type="variable_definition" use="model variable">urbansim.household_x_gridcell.residential_units_when_household_has_children</variable>
          <variable name="gridcell.bpmiw" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.percent_mid_income_households_within_walking_distance</variable>
          <variable name="gridcell.blnrsfw" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance</variable>
          <variable name="household_x_gridcell.yhihdr" source="Python class" type="variable_definition" use="model variable">urbansim.household_x_gridcell.young_household_in_high_density_residential</variable>
          <variable name="gridcell.ldevsfc" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.ln_developable_commercial_sqft_capacity</variable>
          <variable name="household_x_gridcell.iayb" source="Python class" type="variable_definition" use="model variable">urbansim.household_x_gridcell.income_and_year_built</variable>
          <variable name="gridcell.nrs" source="expression" type="variable_definition" use="model variable">ln_bounded(urbansim.gridcell.non_residential_sqft)</variable>
          <variable name="gridcell.bart" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.is_near_arterial</variable>
          <variable name="gridcell.blwap_1" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.ln_work_access_to_population_1</variable>
          <variable name="gridcell.piw" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.percent_industrial_within_walking_distance</variable>
          <variable name="gridcell.ble_sew" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.ln_service_sector_employment_within_walking_distance</variable>
          <variable name="gridcell.prw" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.percent_residential_within_walking_distance</variable>
          <variable name="gridcell.ble_bw" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.ln_basic_sector_employment_within_walking_distance</variable>
          <variable name="household_x_gridcell.pmhwwdim" source="Python class" type="variable_definition" use="model variable">urbansim.household_x_gridcell.percent_minority_households_within_walking_distance_if_minority</variable>
          <variable name="household_x_gridcell.phihwwdili" source="Python class" type="variable_definition" use="model variable">urbansim.household_x_gridcell.percent_high_income_households_within_walking_distance_if_low_income</variable>
          <variable name="gridcell.o_ugb" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.is_outside_urban_growth_boundary</variable>
          <variable name="gridcell.bflood" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.is_in_floodplain</variable>
          <variable name="gridcell.bwet" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.is_in_wetland</variable>
          <variable name="household_x_gridcell.yhimu" source="Python class" type="variable_definition" use="model variable">urbansim.household_x_gridcell.young_household_in_mixed_use</variable>
          <variable name="gridcell.le_w" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.ln_total_employment_within_walking_distance</variable>
          <variable name="gridcell.lru" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.ln_residential_units</variable>
          <variable name="gridcell.blimp" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.ln_total_improvement_value</variable>
          <variable name="gridcell.lsfiw" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.ln_industrial_sqft_within_walking_distance</variable>
          <variable name="gridcell.btt_cbd" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.travel_time_to_CBD</variable>
          <variable name="gridcell.blsfcw" source="Python class" type="variable_definition" use="model variable">urbansim.gridcell.ln_commercial_sqft_within_walking_distance</variable>
    </expression_library>
    </general>
    <model_manager>
        <models>
            <model name="land_price_model" type="model">
            <structure>
            <init>
            <argument name="nested_structure" />
            </init>
            </structure>
                <specification type="dictionary">
                  <submodel hidden="Children" name="submodel" submodel_id="-2" type="submodel">
                    <description type="string">No description</description>
                    <variable_list type="variable_list">
                      <variable_spec name=".pcthiwa"/>
                      <variable_spec name=".ln_duw"/>
                      <variable_spec name=".lru"/>
                      <variable_spec name=".bwet"/>
                      <variable_spec name=".cbdtrvl"/>
                      <variable_spec name=".ln_impval"/>
                      <variable_spec name=".bflood"/>
                      <variable_spec name=".bldhw"/>
                      <variable_spec name=".hwy"/>
                      <variable_spec name=".pctdevwal"/>
                      <variable_spec name="constant"/>
                    </variable_list>
                  </submodel>
                </specification>
              </model>

              <model name="employment_location_choice_model" type="model">
                  <structure>
                  <init>
                  <argument name="nested_structure" />
                  </init>
                  </structure>
                <specification type="dictionary">
                    <submodel hidden="Children" name="submodel w/ Equations" submodel_id="1" type="submodel">
                      <description type="string">No description</description>
                      <nest nest_id="1" name="nest one" />
                      <nest nest_id="2" name="nest two" />
                      <nest nest_id="3" name="nest three" />
                      <equation name="equation one" equation_id="1">
                          <variable_list type="variable_list">
                            <variable_spec name=".ble_saw"/>
                            <variable_spec name=".ble_sew"/>
                            <variable_spec name=".ble_rew"/>
                            <variable_spec name=".blnrsfw"/>
                            <variable_spec name=".bltv"/>
                            <variable_spec name=".bart"/>
                          </variable_list>
                    </equation>
                    <equation equation_id="2" name="eq two">
                      <variable_list type="variable_list">
                        <variable_spec name=".ble_saw"/>
                        <variable_spec name=".ble_sew"/>
                        <variable_spec name=".ble_rew"/>
                        <variable_spec name=".blnrsfw"/>
                        <variable_spec name=".bltv"/>
                        <variable_spec name=".bart"/>
                      </variable_list>
                    </equation>
                    <equation equation_id="3" name="simpler equation">
                      <variable_list type="variable_list">
                        <variable_spec name=".ble_rew"/>
                        <variable_spec name=".bltv"/>
                      </variable_list>
                    </equation>
                    </submodel>
                </specification>
              </model>
          </models>
      </model_manager>
      </opus_project>
    '''
    p = MockupOpusProject(xml)
    app = QtGui.QApplication([], True)
    w = SubModelEditor(p)
    # model_node = p.find('model_manager/models/model', name='land_price_model')
    model_node = p.find('model_manager/models/model', name='land_price_model')
    w.init_for_submodel_node(model_node.find('specification/submodel'))
    while w.exec_() == w.Accepted:
        print etree.tostring(w.submodel_node, pretty_print=True)
