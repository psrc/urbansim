# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt, QVariant # these are used frequently so a shorter name is nicer
from lxml import etree
from opus_gui.general_manager.general_manager_functions import get_variable_nodes_per_dataset
from opus_core.configurations.xml_configuration import get_variable_dataset_and_name, get_variable_name
from opus_gui.tests.mockup_project import MockupOpusProject
from opus_gui.util.icon_library import IconLibrary

class VariableSelectorTableModel(QtCore.QAbstractTableModel):

    '''
    Table model for showing and defining specification variables.

    The data of the model is a list() of <variable_spec> nodes.
    '''

    def __init__(self, project, parent_widget = None):
        QtCore.QAbstractTableModel.__init__(self, parent_widget)
        self.project = project
        self._variable_nodes = [] # list of variables included in the specification
        self._names_to_definition_nodes = {} # variable nodes from the expression lib, indexed by name

        # header constants (values appear as title for columns)
        self.HEADER_IGNORE = 'ignore'
        self.HEADER_VARIABLE = 'variable'
        self.HEADER_COEFF_NAME = 'coeff. name'
        self.HEADER_STARTING_VAL = 'starting value'
        self.HEADER_FIXED = 'fixed'
        self.HEADER_DEFINITION = 'definition'

        self._headers = [self.HEADER_IGNORE, self.HEADER_VARIABLE, self.HEADER_COEFF_NAME,
                         self.HEADER_STARTING_VAL, self.HEADER_FIXED, self.HEADER_DEFINITION]

        self

    def init_for_variable_node_list(self, variable_list_node):
        '''
        Initialize the table for a variable_list node.
        @param variable_list_node a <variable_list> node.
        @param variable_nodes_per_dataset a dict() of variables; [dataset name] -> variables
        '''
        # self._variable_nodes = variable_list_node.findall('variable_spec')
        for variable_spec_node in variable_list_node.findall('variable_spec'):
            self.insertRow(0, QtCore.QModelIndex(), variable_spec_node)
        # map the selected variables to a variable node in the expression library for faster lookups
        map(self._map_variable_to_definition_node, self._variable_nodes)
        self.sort_variables_by_name()

    def add_variable_from_definition_node(self, variable_definition_node):
        ''' create a new variable_spec node with the same name as a definition node and add it to
        the model '''
        name_attrib = {'name': variable_definition_node.get('name')}
        variable_spec_node = etree.Element('variable_spec', name_attrib)
        self.add_variable_spec_node(variable_spec_node)

    def add_variable_spec_node(self, variable_spec_node):
        ''' add a variable_spec node to the model. The node is mapped to a it's definition node
        before it's added. '''
        self._map_variable_to_definition_node(variable_spec_node)
        root_index = QtCore.QModelIndex()
        row = self.rowCount(root_index)
        self.insertRow(row, root_index, variable_spec_node)

    def apply_selected_variables(self, variable_list_node):
        ''' changes the list of child nodes for the given variable_list node to the list of
        variable_spec nodes of the model '''
        # replace the set of child nodes with the selected variable_spec nodes
        for child_node in variable_list_node:
            variable_list_node.remove(child_node)
        for child_node in self._variable_nodes:
            variable_list_node.append(child_node)

    def clear(self):
        parent_index = QtCore.QModelIndex()
        QtCore.QAbstractTableModel.removeRows(self, 0, self.rowCount(parent_index), parent_index)
        self._variable_nodes = []
        self.emit(QtCore.SIGNAL('layoutChanged()'))

    def get_variable(self, row):
        ''' returns the variable at row, or none if row is not in the model '''
        if self.rowCount() <= row < 0:
            return None
        return self._variable_nodes[row]

    def _map_variable_to_definition_node(self, variable_node):
        ''' creates a mapping between the variables (name, dataset) and it's definition node '''
        dataset, name = get_variable_dataset_and_name(variable_node)
        expression_lib_nodes = get_variable_nodes_per_dataset(self.project)

        # Before XML 2.0 there was no dataset associated with variable selections, so some converted
        # files might have an empty dataset (variable name starts with a . [dot]).
        # in these cases we try to guess wich variable in the expression lib to associate with.
        # Note that built-ins like 'constant' return None as dataset, not an empty string.
        if dataset == '':
            possible_datasets = []
            for dataset_name, variable_nodes in expression_lib_nodes.items():
                for variable_definition_node in variable_nodes:
                    def_variable_name = get_variable_name(variable_definition_node)
                    if def_variable_name == name:
                        possible_datasets.append(dataset_name)
                        break
            if len(possible_datasets) == 1:
                dataset = possible_datasets[0]
                # update the variable node with the guessed dataset
                # variable_node.set('name', '%s.%s' %(dataset, name))

        if not dataset in expression_lib_nodes:
            self._names_to_definition_nodes[(name, dataset)] = None
        else: # look through the dataset to find a variable with the same name
            for variable_definition_node in expression_lib_nodes[dataset]:
                def_variable_name = get_variable_name(variable_definition_node)
                if def_variable_name == name:
                    self._names_to_definition_nodes[(name, dataset)] = variable_definition_node
                    break
            else:
                self._names_to_definition_nodes[(name, dataset)] = None

    def _set_or_remove_attrib(self, node, attrib_name, value):
        ''' sets an attribute of the node to value. if value evaluates to False, the attribute is
        removed from the node'''
        if value:
            node.set(attrib_name, value)
        elif attrib_name in node.attrib:
            del node.attrib[attrib_name]

    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self._variable_nodes)

    def columnCount(self, parent = QtCore.QModelIndex()):
        return len(self._headers)

    def flags(self, index):
        if not index.isValid():
            return QVariant()
        header = self._headers[index.column()]
        if header == self.HEADER_VARIABLE:
            flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        elif header in [self.HEADER_IGNORE, self.HEADER_FIXED]:
            flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEditable
        elif header  ==self.HEADER_DEFINITION:
            flags = Qt.ItemIsSelectable
        else:
            flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        return flags

    def insertRow(self, row, parent_index = QtCore.QModelIndex(), variable_spec_node = None):
        self.beginInsertRows(parent_index, row, row)
        self._variable_nodes.append(variable_spec_node)
        return_val = QtCore.QAbstractItemModel.insertRow(self, row, parent_index)
        self.endInsertRows()
        self.emit(QtCore.SIGNAL('layoutChanged()'))
        return return_val

    def removeRow(self, row, parent_index = QtCore.QModelIndex()):
        self.beginRemoveRows(parent_index, row, row)
        self._variable_nodes.pop(row)
        return_val = QtCore.QAbstractItemModel.removeRow(self, row, parent_index)
        self.endRemoveRows()
        self.emit(QtCore.SIGNAL('layoutChanged()'))
        return return_val

    def data(self, index, role):
        if not index.isValid():
            return QVariant()

        row = index.row()
        header = self._headers[index.column()]
        node = self._variable_nodes[row]

        # look up the definition once for easy access by multiple roles
        if header == self.HEADER_DEFINITION:
            dataset, name = get_variable_dataset_and_name(node)
            if name == 'constant':
                definition = '<built-in constant>'
            elif (name, dataset) in self._names_to_definition_nodes:
                definition_node = self._names_to_definition_nodes[(name, dataset)]
                if definition_node is not None:
                    definition = definition_node.text
                else:
                    definition = '<empty definition>'
            else:
                definition = '<unknown definition>'

        if role == Qt.DecorationRole:
            if header == self.HEADER_VARIABLE:
                return QVariant(IconLibrary.icon('variable'))

        if role == Qt.DisplayRole:
            var_name = get_variable_name(self._variable_nodes[row])
            if header == self.HEADER_VARIABLE:
                return QVariant(var_name)

            if header == self.HEADER_DEFINITION:
                return QVariant(definition)

            if header == self.HEADER_COEFF_NAME:
                if 'coefficient_name' in node.attrib:
                    return QVariant(node.get('coefficient_name'))
                return QVariant(var_name)

            if header == self.HEADER_STARTING_VAL:
                return QVariant(node.get('starting_value') or '')

        if role == Qt.EditRole:
            if header == self.HEADER_STARTING_VAL:
                return self.data(index, Qt.DisplayRole)
            if header == self.HEADER_COEFF_NAME:
                # give a clear coeff name if it's not set yet
                if 'coefficient_name' in node.attrib:
                    return QVariant(node.get('coefficient_name'))
                return QVariant()

        if role == Qt.CheckStateRole:
            if header == self.HEADER_IGNORE:
                return QVariant(Qt.Checked if node.get('ignore') == 'True' else Qt.Unchecked)
            if header == self.HEADER_FIXED:
                return QVariant(Qt.Checked if node.get('keep_fixed') == 'True' else Qt.Unchecked)

        if role == Qt.FontRole:
            font = QtGui.QFont()
            if header == self.HEADER_VARIABLE:
                if node.get('ignore') != 'True':
                    font.setBold(True)
                    return QVariant(font)
            elif header == self.HEADER_COEFF_NAME and node.get('coefficient_name'):
                font.setBold(True)
                return QVariant(font)

        if role == Qt.ForegroundRole:
            # color default values of coefficient name as light gray
            if header == self.HEADER_COEFF_NAME:
                if 'coefficient_name' not in node.attrib:
                    return QVariant(QtGui.QColor(Qt.gray))

        if role == Qt.ToolTipRole:
            if header == self.HEADER_DEFINITION: # defs easily get cramped so show in tool tip as well
                return QVariant(definition)

        return QVariant()

    def setData(self, index, value, role):
        if not index.isValid():
            return QVariant()

        row = index.row()
        header = self._headers[index.column()]
        node = self._variable_nodes[row]

        if role == Qt.CheckStateRole:
            val, flag = value.toInt()
            is_checked = val == Qt.Checked and flag
            if header == self.HEADER_FIXED:
                self._set_or_remove_attrib(node, 'keep_fixed', 'True' if is_checked else '')
            elif header == self.HEADER_IGNORE:
                self._set_or_remove_attrib(node, 'ignore', 'True' if is_checked else '')
            else:
                return False
            self.emit(QtCore.SIGNAL('layoutChanged()'))

        elif role == Qt.EditRole:
            if header == self.HEADER_STARTING_VAL:
                # if the user enters an empty string, delete the starting value
                # otherwise only change it on a successful conversion to a double
                if value.toString() == '' and 'starting_value' in node.attrib:
                    del node.attrib['starting_value']
                else:
                    value, flag = value.toDouble()
                    if flag:
                        node.set('starting_value', str(value))

            elif header  == self.HEADER_COEFF_NAME:
                self._set_or_remove_attrib(node, 'coefficient_name', str(value.toString()))

        return True

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self._headers[col])
        return QVariant()

    def sort_variables_by_name(self):
        ''' sort all the variables by their variable name '''
        compare_by_var_name = lambda x, y: cmp(get_variable_name(x), get_variable_name(y))
        self._variable_nodes.sort(compare_by_var_name)

if __name__ == '__main__':
    xml = '''
    <opus_project>
        <general>
            <expression_library type="dictionary">
                    <variable source="Python class" type="variable_definition" use="both" name="zone.ln_distance_to_highway">ln(urbansim_parcel.zone.distance_to_highway)</variable>
                    <variable source="expression" type="variable_definition" use="model variable" name="parcel.land_price">urbansim.land_price * 5</variable>
                    <variable source="expression" type="variable_definition" use="model variable" name="zone.ignore_me">urbansim.ignore_with_reeeeeeeeeeeeeeeeeeeeeeaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaallllllllllllllllllllllllllllllllyyyyyyyyyyy_loooooooooooooooooooooooooooooooong_name</variable>

                    <variable source="expression" type="variable_definition" use="model variable" name="dataset1.variable">urbansim.dataset1.somevariable_def</variable>
                    <variable source="expression" type="variable_definition" use="model variable" name="dataset2.variable">10 - ln(urbansim.dataset2.somevariable_def)</variable>

                    <variable source="Python class" type="variable_definition" use="both" name="zone.population_per_acre">urbansim_parcel.zone.population_per_acre</variable>
                    <variable source="expression" type="variable_definition" use="model variable" name="constant">constant</variable>
                    <variable source="expression" type="variable_definition" use="model variable" name="building.people_in_building">10 * urbansim.building.people_in_building</variable>
                    <variable source="expression" type="variable_definition" use="model variable" name=".add me">urbansim.zone.ln_constraint</variable>
            </expression_library>
        </general>
        <variable_list type="selectable_list">
            <variable_spec name=".ln_distance_to_highway" keep_fixed="True" starting_value="42.0" coefficient_name="dth" type="variable" />
            <variable_spec name=".land_price" keep_fixed="False" type="variable" />
            <variable_spec name=".ignore_me" type="variable" ignore="True"/>
            <variable_spec name="constant" type="variable" />
            <variable_spec name="dataset2.variable" type="variable" />
        </variable_list>
    </opus_project>
    '''
    app = QtGui.QApplication([], True)
    p = MockupOpusProject(xml)

    f = QtGui.QFrame()
    l = QtGui.QVBoxLayout()
    f.setLayout(l)
    tv = QtGui.QTableView()
    m = VariableSelectorTableModel(p)
    v_defs = p.findall('expression_library/variable')
    m.init_for_variable_node_list(p.find('variable_list'))
    tv.setModel(m)
    l.addWidget(QtGui.QLabel('Hello'))
    l.addWidget(tv)
    pb = QtGui.QPushButton('reload')
    lbl = QtGui.QLabel()
    def update_text():
        text = ''
        for v in m._variable_nodes:
            text = text + etree.tostring(v, pretty_print=True)
        lbl.setText(text)
    def add_variable():
        node = p.find('variables/variable', name='add me')
        m.add_selection_for_variable_node(node)

    pb.connect(pb, QtCore.SIGNAL('released()'), update_text)
    pb2 = QtGui.QPushButton('add')
    pb2.connect(pb2, QtCore.SIGNAL('released()'), add_variable)

    l.addWidget(pb)
    l.addWidget(pb2)
    l.addWidget(lbl)
    f.show()
    f.resize(QtCore.QSize(640, 480))
    tv.setSelectionBehavior(tv.SelectRows)
    tv.resizeColumnToContents(0)
    tv.resizeColumnToContents(1)
    tv.resizeRowsToContents()
    tv.resizeColumnToContents(4)
    tv.horizontalHeader().setStretchLastSection(True)
    tv.verticalHeader().hide()
    update_text()
    app.exec_()
