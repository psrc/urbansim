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

import copy

from lxml.etree import SubElement

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, Qt

from opus_gui.util.icon_library import IconLibrary
from opus_gui.general_manager.general_manager_functions import get_variable_nodes_per_dataset
from opus_gui.models_manager.views.ui_submodel_editor import Ui_SubModelEditor


class SubModelEditor(QtGui.QDialog, Ui_SubModelEditor):

    '''
    Submodel Editing dialog.
    The editor support three different structures for specifying submodel variables;
    Plain (submodel/variables),
    Equations (submodel/equation/variables) and
    Nested (submodel/nest1/nest2/nest...N/equation/variables)

    current_variables_node: The current <variables> node to operate on.
    submodel_node: The submodel node that is being edited.
    '''

    def __init__(self, project, parent_widget = None):
        QtGui.QDialog.__init__(self, parent_widget)
        self.setupUi(self)

        self.tree_submodel_structure.header().setStretchLastSection(True)
        self.tree_submodel_structure.header().setMinimumWidth(50)
        self.tree_submodel_structure.header().setSizePolicy(QtGui.QSizePolicy.Maximum,
                                                            QtGui.QSizePolicy.Maximum)

        self.project = project
        self.submodel_node = None
        self.current_variables_node = None

        self.pb_add.setIcon(IconLibrary.icon('arrow_right'))
        # switch writing direction to have the icon the left
        self.pb_add.setLayoutDirection(Qt.RightToLeft)
        self.pb_remove.setIcon(IconLibrary.icon('arrow_left_red'))
        double_clk = SIGNAL('doubleClicked(QModelIndex)')
        self.connect(self.lst_available, double_clk, lambda x: self.on_pb_add_released())
        self.connect(self.lst_selected, double_clk, lambda x: self.on_pb_remove_released())
        self.connect(self.buttonBox, SIGNAL('rejected()'), self.reject)
        self.connect(self.cbo_dataset_filter, SIGNAL('currentIndexChanged(int)'),
                     self._update_available)
        self.variable_names = []
        self.all_variable_names = set()

    def on_tree_submodel_structure_currentItemChanged(self, current, previous):
        self._set_current_variable_node(current.node.find('variables') if current else None)

    def _add_structure_tree_items(self, parent_node, parent_widget):
        ''' (recursively) add all nests and equations '''
        nest_nodes = parent_node.findall('nest')
        equation_nodes = parent_node.findall('equation')
        # recursively add nest nodes
        for nest_node in nest_nodes:
            item = QtGui.QTreeWidgetItem(parent_widget)
            item.setText(0, '%s' % nest_node.get('nest_id'))
            item.setText(1, '%s' % (nest_node.get('name')))
            item.setText(2, 'nest')
            item.node = nest_node
            self._add_structure_tree_items(nest_node, item)

        # add any equations
        for equation_node in equation_nodes:
            item = QtGui.QTreeWidgetItem(parent_widget)
            item.setText(0, '%s' % equation_node.get('equation_id'))
            item.setText(1, '%s' % (equation_node.get('name')))
            item.setText(2, 'equation')
            item.node = equation_node

    def init_for_submodel_node(self, submodel_node):
        ''' Setup up the dialog to edit (a copy of) the given submodel_node '''
        self.submodel_node = copy.deepcopy(submodel_node)

        # Populate the widgets
        submodel_name = submodel_node.get('name')
        if submodel_node.find('description') is not None:
            submodel_description = submodel_node.find('description').text.strip()
        else:
            submodel_description = ''
        submodel_id = int(submodel_node.get('submodel_id'))
        self.le_name.setText(submodel_name)
        self.le_description.setText(submodel_description)
        self.spin_id.setValue(submodel_id)

        # don't show the structure node for plain submodels
        self.tree_submodel_structure.clear()

        self._add_structure_tree_items(parent_node = self.submodel_node,
                                       parent_widget = self.tree_submodel_structure)
        is_simple_model = self.tree_submodel_structure.topLevelItemCount() == 0
        if is_simple_model:
            self.tree_submodel_structure.setVisible(False)
        else:
            self.tree_submodel_structure.setVisible(True)
            item = self.tree_submodel_structure.topLevelItem(0)
            self.tree_submodel_structure.setCurrentItem(item)
            self.tree_submodel_structure.resizeColumnToContents(0)
            self.tree_submodel_structure.resizeColumnToContents(1)

        # Setup the available variables section

        self.variables_per_dataset = get_variable_nodes_per_dataset(self.project)
        # get all variable names
        self.all_variable_names.clear()
        for _, variable_nodes in self.variables_per_dataset.items():
            map(self.all_variable_names.add, [node.get('name') for node in variable_nodes])

        # Keep the dataset filter list updated. If there is a dataset already selected, keep the
        # selection if it is still available.
        prev_dataset_filter = self.cbo_dataset_filter.currentText()
        self.cbo_dataset_filter.clear()
        self.cbo_dataset_filter.addItem('[Show all variables]')
        for dataset_name in self.variables_per_dataset:
            self.cbo_dataset_filter.addItem(dataset_name)
        if self.cbo_dataset_filter.findText(prev_dataset_filter) > -1:
            index = self.cbo_dataset_filter.findText(prev_dataset_filter)
            self.cbo_dataset_filter.setCurrentIndex(index)
        else:
            self.cbo_dataset_filter.setCurrentIndex(0)

        # if we are editing a plain submodel, we set the list of selected variables immediately,
        # if it's a more complex submodel we wait until the user selects an equation to edit
        if is_simple_model:
            self._set_current_variable_node(self.submodel_node.find('variables'))

    def _set_current_variable_node(self, variables_node):
        # apply the current selection to the previously selected variable node
        self._apply_selected_variables(self.current_variables_node)
        self.current_variables_node = variables_node
        if variables_node is None or variables_node.text is None:
            current_list = ''
        else:
            current_list = self.current_variables_node.text

        currently_selected_names = [v.strip() for v in current_list.split(',')]

        self.lst_selected.clear()
        for variable_name in currently_selected_names:
            if variable_name in self.all_variable_names: # filter out invalid variables
                self.lst_selected.addItem(variable_name)

        if variables_node is not None:
            msg = 'Selecting for %s' %(self.current_variables_node.getparent().get('name'))
        else:
            msg = 'No equation selected'

        self.lbl_active_variablelist.setText(msg)
        self._update_available()

    def _update_available(self):
        ''' update the list of available variables to not include already selected ones '''
        selected_names = set(str(self.lst_selected.item(row).text()) for
                             row in range(0, self.lst_selected.count()))
        self.lst_available.clear()

        # filter by dataset if a filter is selected
        if self.cbo_dataset_filter.currentIndex() > 0:
            dataset_name = str(self.cbo_dataset_filter.currentText())
            variable_names = [node.get('name') for node in self.variables_per_dataset[dataset_name]]
        else:
            variable_names = self.all_variable_names

        for variable_name in variable_names:
            if not variable_name in selected_names:
                self.lst_available.addItem(variable_name)
        self.lst_available.sortItems()
        self.lst_selected.sortItems()

    def _apply_selected_variables(self, variables_node):
        if variables_node is None:
            return
        # is this really the easiest way to get all selected item texts?
        selected_variable_names = [str(self.lst_selected.item(row).text()) for
                                   row in range(0,self.lst_selected.count())]
        variable_list = ','.join(selected_variable_names)
        variables_node.text = variable_list

    def on_pb_add_released(self):
        ''' user clicked add button '''
        # "move" the selected variables from available to selected
        selected_for_move = [item.text() for item in self.lst_available.selectedItems()]
        for variable_name in selected_for_move:
            self.lst_selected.addItem(variable_name)
        self._update_available()

    def on_pb_remove_released(self):
        ''' user clicked remove button '''
        num_sel = self.lst_selected.count()
        selected_names = [self.lst_selected.item(row).text() for row in range(0, num_sel)]
        for item in self.lst_selected.selectedItems():
            selected_names.remove(item.text())
        self.lst_selected.clear()
        for variable_name in selected_names:
            self.lst_selected.addItem(variable_name)
        self._update_available()

    def on_buttonBox_accepted(self):
        self._apply_selected_variables(self.current_variables_node)
        description_node = self.submodel_node.find('description')
        if description_node is None:
            description_node = SubElement(self.submodel_node, 'description')
        description_node.text = str(self.le_description.text())
        self.submodel_node.set('submodel_id', str(self.spin_id.value()))
        self.submodel_node.set('name', str(self.le_name.text()))
        self.accept()
