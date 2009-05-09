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

from lxml.etree import Element

from PyQt4.QtCore import QAbstractTableModel, QModelIndex, QVariant, Qt
from PyQt4.QtCore import SIGNAL, QEventLoop
from PyQt4.QtGui import QColor, qApp

def variable_to_validator_format(variable):
    '''
    Convert a given variable to the format used by varible validators
    format: (var_name, dataset_name, use, source, expr)
    @param variable (dict) a variable in the format used by VariablesTableModel
    @return the list of variables in VariableValidator format
    '''
    try:
        var_name = variable['name']
        dataset_name = variable['dataset']
        use = variable['use']
        source = variable['source']
        expr = variable['definition']
    except KeyError:
        raise RuntimeError('Tried to convert a nonvalid variable to validator form')
    return (var_name, dataset_name, use, source, expr)

def create_empty_variable():
    '''
    Get a dictionary that is initialized to hold a variable as defined in
    VariablesTableModel.
    @return a variable dict (dict)
    '''
    var = {}
    # variable data
    var['name'] = 'unnamed_variable'
    var['definition'] = ''
    var['dataset'] = ''
    var['use'] = 'both'
    var['source'] = 'expression'
    # metadata for model
    for key in ['selected', 'dirty', 'delete']: var[key] = False
    for key in ['syntaxerror', 'dataerror', 'originalnode', 'inherited']: var[key] = None
    return var

def variable_from_node(variable_node):
    '''
    convert a variable in node format to a variable in the variable table model format
    @param variable_node (Element) node to get values from
    @return the converted variable (dict)
    '''
    variable = create_empty_variable()
    for key in ['dataset', 'use', 'source', 'inherited', 'name']:
        variable[key] = variable_node.get(key)
    variable['definition'] = str(variable_node.text).strip()
    return variable

def node_from_variable(variable):
    '''
    convert a variable dict as specified under VariablesTableModel into a node
    @param variable (dict) the variable to convert to a node
    @return node (Element) the node representation of the given variable
    '''
    node = Element('variable')
    node.text = variable['definition']
    for key in ['dataset', 'use', 'source', 'inherited', 'name']:
        node.attrib[key] = str(variable[key])
    node.set('type', 'variable_definition')
    return node

def variable_batch_check(variables, validator_func, variable_key = None,
                         progress_callback = None, cancel_flag = None):
    '''
    Go through a list of variables and runs the validator_func on each of them.
    Variables that does not validate gets the key indicated by 'variable_key' set to the error msg.
    Variables that pass gets the key set to False.
    'variable_key' can also be None, in which case no key is set.

    @param variables list(dict) list of variables in the format specified in variable_table_model
    @param validator_func (function) a function that takes a list of variables (dict)and returns a
    tuple with result of the whole validation and the collected error messages (bool, list(str))
    @return a list of tuples. The tuples contain, for each variable:
        the variable (dict), the result (bool) and the error messages (str).
    '''
    if progress_callback is None:
        progress_callback = lambda x: None
    cancel_flag = cancel_flag or {'value':False}
    res = []
    num_steps = len(variables)
    for step, variable in enumerate(variables):
        qApp.processEvents(QEventLoop.AllEvents) # flush out events so that progress bars update
        if cancel_flag['value']: break
        converted_var = variable_to_validator_format(variable)
        try:
            success, msg = validator_func(variables = [converted_var,])
        except Exception, ex:
            success = False
            msg = ['ERROR while trying to validate %s: %s' %(variable['name'], ex),]
        if success is True:
            variable[variable_key] = False
        else:
            variable[variable_key] = msg
        res.append((variable, success, msg))
        progress_callback(float(step)/float(num_steps))
    cancel_flag['value'] = False # reset/set cancel flag
    return res

def batch_check_syntax(variables, validator):
    '''
    checks a list of variables for syntax errors
    @param variables list(dict) list of variables in dict format
    @param validator (VariableValidator) a validator to use for variable validation
    @return a list of [for each variable] tuples like variable(dict), result(bool), message(str)
    '''
    return variable_batch_check(variables = variables,
                                validator_func = validator.check_parse_errors,
                                variable_key = 'syntaxerror')

def batch_check_data(variables, validator):
    '''
    checks a list of variables against it's base year data
    @param variables list(dict) list of variables in dict format
    @param validator (VariableValidator) a validator to use for variable validation
    @return a list of [for each variable] tuples like variable(dict), result(bool), message(str)
    '''
    return variable_batch_check(variables = variables,
                                validator_func = validator.check_data_errors,
                                variable_key = 'dataerror')

class VariablesTableModel(QAbstractTableModel):
    """
    Table Data Model for Opus Model Variables.

    data is contained in a list of dictionaries (self.variables)

    variables are defined as a dictionary with the following keys:

        'name': string (variable name)
        'definition': string (variable definition)
        'dataset': string (variable dataset or None)
        'use': string ('model variable', 'indicator' or 'both')
        'source': ('expression', 'Python Class' or 'primary attribute')
        'inherited': string (name of parent)

        'selected': bool (check box)
        'dirty': bool
        'syntaxerror': None or error description
        'dataerror': None or error description
        'originalnode': None or reference to the original XML node (Element)
        'delete': True if the variable should be deleted from the project on Apply
    """

    VARIABLE_METADATA_KEYS = ('selected', 'dirty', 'syntaxerror', 'dataerror',
                              'originalnode', 'delete', 'inherited')
    VARIABLE_NON_METADATA_KEYS = ('name', 'definition', 'dataset', 'use', 'source')

    def __init__(self, project = None, variables = None, parent_widget = None):
        '''
        @param parent_widget parent widget for the model
        @param variables_dict dictionary of initial variable data
        '''
        QAbstractTableModel.__init__(self, parent_widget)
        self.project = project
        self.variables = variables or []
        self.headers = ["", "Name", "Dataset", "Use", "Type", "Definition"]
        # mapping of columns -> keys
        self.keys = ('selected', 'name', 'dataset', 'use', 'source', 'definition')
        self.parent_widget = parent_widget
        self.to_be_deleted = [] # variables the user wants to delete
        self.sorted_by_column = 1
        self.sorting_order = Qt.AscendingOrder
        self.dirty = False
        self.palette = qApp.palette() # for system-coherent selection colors

    def flags(self, index):
        ''' PyQt4 API Method '''
        flags = Qt.ItemIsEnabled # all variables are enabled
        if index.isValid(): # valid items are selectable
            flags = flags | Qt.ItemIsSelectable
        if index.column() == 0: # first row has a checkbox
            flags = flags | Qt.ItemIsUserCheckable
        return flags

    def rowCount(self, parent = QModelIndex()):
        ''' PyQt4 API Method '''
        if parent.isValid():
            return 0
        return len(self.variables)

    def columnCount(self, parent = QModelIndex()):
        ''' PyQt4 API Method '''
        # don't display columns when there are no rows
        if not self.rowCount(parent):
            return 0
        return len(self.headers)

    def data(self, index, role):
        ''' PyQt4 API Method '''
        if not index.isValid():
            return QVariant()

        row = index.row()
        col = index.column()
        var = self.variables[row]
        col_key = None
        if 0 < col < len(self.keys):
            col_key = self.keys[col]

        if role == Qt.DisplayRole:
            # Displayed text
            if index.column() == 0:
                return QVariant() # no text for checkbox
            # Show a single letter for variable use
            if col_key == 'use':
                abbr = var['use']
                if var['use'] == 'model variable':
                    abbr = 'M'
                elif var['use'] == 'indicator':
                    abbr = 'I'
                elif var['use'] == 'both':
                    abbr = 'I+M'
                return QVariant(abbr)
            if col_key == 'source':
                abbr = '?'
                if var['source'] == 'expression':
                    abbr = 'Exp'
                elif var['source'] == 'Python class':
                    abbr = 'PyC'
                elif var['source'] == 'primary attribute':
                    abbr = 'Pri'
                return QVariant(abbr)
            if col_key:
                if col_key == 'name':
                    name = var['name']
                    if var['syntaxerror']: pass
                    if var['dataerror']: pass
                    return QVariant(name)
                return QVariant(var[col_key])

        elif role == Qt.ToolTipRole:
            tooltip = ''
            if col_key == 'use':
                tooltip = 'use: <b>%s</b>' % var['use']
            elif col_key == 'source':
                tooltip = 'source: <b>%s</b>' % var['source']
            elif col_key == 'name':
                tooltip = 'name: <b>%s</b>' % var['name']
            return QVariant(tooltip)

        elif role == Qt.CheckStateRole and col == 0:
            if self.variables[row]['selected']:
                return QVariant(Qt.Checked)
            return QVariant(Qt.Unchecked)

        elif role == Qt.ForegroundRole:
            # Color of text
            variable = self.variables[row]
            if variable['inherited']:
                if variable['selected']:
                    return QVariant(self.palette.highlightedText().color())
                return QVariant(QColor(Qt.blue))

        elif role == Qt.BackgroundRole:
            # Color of background
            variable = self.variables[row]
            if variable['selected']:
                return QVariant(self.palette.highlight().color())

        elif role == Qt.TextAlignmentRole:
            if col in (3, 4):
                return QVariant(Qt.AlignCenter)
            return QVariant()

        return QVariant()

    def setData(self, index, value, role):

        if role == Qt.CheckStateRole and index.column() == 0:
            state = value.toInt()[0]
            checked = state == Qt.Checked
            self.variables[index.row()]['selected'] = checked
            # Make the model redraw the whole row
            row = index.row()
            first_index = self.createIndex(row, 0)
            last_index = self.createIndex(row, len(self.headers))
            self.emit(SIGNAL('dataChanged (const QModelIndex &, '
                             'const QModelIndex &)'), first_index, last_index)
            self.emit(SIGNAL('model_changed'))
        return True

    def insertRow(self, row, variable, parent = QModelIndex()):
        '''
        insert a variable into the model.
        raise an error if the variable is a duplicate (i.e if name + dataset
        is not unique)
        '''
        returnval = QAbstractTableModel.insertRow(self, row, parent)
        self.variables.append(variable)
        variable['dirty'] = True
        self.dirty = True
        idx_start = self.createIndex(row, 0)
        idx_end = self.createIndex(row, self.columnCount() - 1)
        self.emit(SIGNAL("dataChanged(const QModelIndex&, const QModelIndex&)"),
                  idx_start, idx_end)
        self.emit(SIGNAL('model_changed'))
        return returnval

    def removeRow(self, row, parent = QModelIndex()):
        ''' PyQt4 API Method '''
        returnval = QAbstractTableModel.removeRow(self, row, parent)
        self.beginRemoveRows(parent, row, row)
        self.variables.pop(row)
        self.endRemoveRows()
        self.dirty = True
        self.emit(SIGNAL('model_changed'))
        return returnval

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headers[col])
        return QVariant()

    def sort(self, column_num = 1, order = Qt.AscendingOrder):
        ''' Sort table by given column number. '''
        if column_num == 0: # don't allow sorting by check boxes (column 0)
            return

        self.sorted_by_column = column_num


        # sort the list of variables by the given column
        # (use self.keys for mapping keys -> columns)
        sort_key = self.keys[column_num ] # offset for check boxes
        def cmp_(x, y, k = sort_key): return cmp(x[k], y[k])
        self.variables.sort(cmp_, reverse = order == Qt.DescendingOrder)
        self.emit(SIGNAL("layoutChanged()"))

    def re_sort(self): self.sort(self.sorted_by_column, self.sorting_order)

    def add_variable(self, variable):
        '''
        insert a new variable row into the model and re-sorts the table
        @param variable_dict the variable data
        @return the row number for the created variable
        '''
        self.insertRow(0, variable)
        variable['dirty'] = True
        variable['inherited'] = False
        self.sort(self.sorted_by_column, self.sorting_order)
        return self.variables.index(variable)

    def edit_variable(self, edited_copy, original_var):
        made_changes = False
        for k in edited_copy:
            if original_var[k] != edited_copy[k]:
                made_changes = True
                original_var[k] = edited_copy[k]
        if made_changes:
            original_var['dirty'] = True
            original_var['inherited'] = False
            self.dirty = True
        if original_var['dirty']:
            self.dirty = True
        self.emit(SIGNAL('model_changed'))

    def delete_variable(self, variable):
        '''
        Delete the variable in a given row
        @param variable (dict) the row to delete a variable from
        @return True if the row was removed, False otherwise
        '''
        # This is a little bit complicated since we need to 'fake' deleting nodes (the actual
        # deletion is done when the user click apply.
        # This is trivial except for the case where the original node is shadowing an inherited
        # node. In this case we need to get the prototype node (the inherited node that's being
        # shadowed) and copy the values into the variable we "delete".
        row = self.variables.index(variable)
        if row < 0 or row > self.rowCount() or variable['inherited']:
            return False

        original_node = variable['originalnode']
        prototype_node = self.project.get_prototype_node(original_node) if original_node is not None else None
        if original_node is None or prototype_node is None: # node (or original node) is local only
            self.removeRow(row)
        else:
            # the prototype of an inherited node is itself
            node = original_node if (prototype_node is original_node) else prototype_node
            template_variable = variable_from_node(node)
            for key in template_variable:
                variable[key] = template_variable[key]
            variable['originalnode'] = original_node
            variable['dirty'] = True
        # Emit update signal
        self.dirty = True
        self.emit(SIGNAL('model_changed'))
        return True
