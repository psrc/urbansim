# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QVariant

class SubmodelStructureItem(QtGui.QTreeWidgetItem):

    '''
    Provide custom display of items in a submodel structure tree
    '''
    NEST_ID = 'nest_id'
    EQUATION_ID = 'equation_id'

    def __init__(self, node, editable = False, parent_widget = None):
        QtGui.QTreeWidgetItem.__init__(self, parent_widget)
        self._node = node
        self._editable = bool(editable)
        if node.tag == 'equation':
            self._type_id = self.EQUATION_ID
        elif node.tag == 'nest':
            self._type_id = self.NEST_ID
        else:
            raise TypeError('Can only create items for <equation> or <nest>')
        self._id = self._node.get(self._type_id)

        self.setText(0, node.get('name'))
        self.setText(1, self._id)
        self.setText(2, node.get('number_of_samples') or '')

        if self._type_id == self.EQUATION_ID:
            font = QtGui.QFont()
            font.setBold(True)
            self.setFont(0, font)

        q = QtCore.Qt
        flags = q.ItemIsEnabled | q.ItemIsSelectable
        if self._editable:
            flags = flags | q.ItemIsDragEnabled | q.ItemIsDropEnabled | q.ItemIsEditable
        self.setFlags(flags)

    def setData(self, column, role, value):
        # intercept the data setting to update the node
        qt_value = value
        if role == QtCore.Qt.EditRole:
            if column == 0:
                value = qt_value.toString()
                self._node.set('name', str(value))
                self.setText(column, value)
            elif column == 1:
                value, flag = qt_value.toInt()
                if flag:
                    self._node.set(self._type_id, str(value))
                else:
                    return
            elif column == 2:
                # # of samples is only applicable to <nest>
                if self._type_id != self.NEST_ID:
                    return
                # keep clean nodes by removing the number_of_samples attribute when it's cleared
                if qt_value.toString() == '' and 'number_of_samples' in self._node.attrib:
                    del self._node.attrib['number_of_samples']
                else:
                    value, flag = qt_value.toInt()
                    if flag:
                        self._node.set('number_of_samples', str(value))
                    else:
                        return

        QtGui.QTreeWidgetItem.setData(self, column, role, qt_value)

    def data(self, column, role):
        # override the data retrieval to make the item interact with the node rather than the
        # internal data strcuture. This enables us to easily sync the items in both tree views
        if role == QtCore.Qt.DisplayRole:
            display_value = ''
            if column == 0:
                if self._type_id == self.NEST_ID:
                    if len(self._node) == 0:
                        display_value = '<%s> (empty)' % self._node.get('name')
                    else:
                        display_value = '<%s>' % self._node.get('name')
                else:
                    display_value = self._node.get('name')
            elif column == 1:
                display_value = '%s' % self._node.get(self._type_id)
            elif column == 2:
                if self._type_id == self.NEST_ID:
                    display_value = self._node.get('number_of_samples')
                else:
                    display_value = '' # attribute not applicable for anything but 'nest'
            else:
                raise ValueError('TreeWidget asked for unknown data')
            return QVariant(display_value)
        elif role == QtCore.Qt.ForegroundRole:
            if column == 0 and self._type_id == self.NEST_ID and len(self._node) == 0:
                return QVariant(QtGui.QColor(QtCore.Qt.gray))
        # use default for everything else
        return QtGui.QTreeWidgetItem.data(self, column, role)

    def variable_list(self):
        ''' return the variable_list node if the represented node has one '''
        return self._node.find('variable_list')
