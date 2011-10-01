# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt, QVariant # these are used so frequently so a shorter name is nicer

class SubmodelStructureEditorModel(QtCore.QAbstractTableModel):

    '''
    Table model for displaying and editing submodel structures.

    Handles <equation> and <nest> (multiple levels of nests are possible).
    '''

    def __init__(self, project, parent_widget = None):
        QtCore.QAbstractTableModel.__init__(self, parent_widget)

        # the internal data structure
        self._structure = {}
        self.HEA

        # header constants (values appear as title for columns)
        self.HEADER_ID = 'ignore'
        self.HEADER_NAME = 'name'
        self.HEADER_NUM_SAMPLES = 'number of samples'
        self._headers = [self.HEADER_ID, self.HEADER_NAME, self.HEADER_NUM_SAMPLES]

    def get_nested_structure(self):
        ''' convert the internal datastructure to the format used in nested logit models
        'nested_structure' argument '''
        pass

    def structure_from_submodel(self, submodel_node):
        ''' convert the submodel structure to the internal datastructure '''
        pass

    # PyQt API
    def rowCount(self, parent_index = QtCore.QModelIndex()):
        node = parent_index.node
        return len(node.findall('nest')) + len(node.findall('equation'))

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
                    definition = definition_node.text or '<empty definition>'
            else:
                definition = '<unknown definition>'

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

        if role == Qt.EditRole:
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
    from lxml import etree #@UnresolvedImport
    from opus_gui.models_manager.models.variable_selector_table_item import VariableSelectorTableItem
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

    pb.connect(pb, QtCore.SIGNAL("clicked()"), update_text)
    pb2 = QtGui.QPushButton('add')
    pb2.connect(pb2, QtCore.SIGNAL("clicked()"), add_variable)

    l.addWidget(pb)
    l.addWidget(pb2)
    l.addWidget(lbl)
    f.show()
    f.resize(QtCore.QSize(640, 480))
    i = VariableSelectorTableItem(tv)
    tv.setItemDelegate(i)
    tv.setSelectionBehavior(tv.SelectRows)
    tv.resizeColumnToContents(0)
    tv.resizeColumnToContents(1)
    tv.resizeRowsToContents()
    tv.resizeColumnToContents(4)
    tv.horizontalHeader().setStretchLastSection(True)
    tv.verticalHeader().hide()
    update_text()
    app.exec_()
