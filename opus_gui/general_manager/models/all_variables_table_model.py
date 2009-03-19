# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from PyQt4.QtCore import Qt, QVariant, QAbstractTableModel, SIGNAL, QModelIndex
from PyQt4.QtGui import QColor
from opus_gui.main.controllers.dialogs.message_box import MessageBox

import operator
from opus_gui.general_manager.run.variable_validator import VariableValidator

class AllVariablesTableModel(QAbstractTableModel):
    def __init__(self, datain, headerdata, parentWidget, editable=True, opus_gui = None):
        QAbstractTableModel.__init__(self, parentWidget)
        self.arraydata = datain
        self.headerdata = headerdata
        self.parentWidget = parentWidget
        self.editable = editable
        self.opus_gui = opus_gui

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        if index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable
        elif self.editable:
            return Qt.ItemIsEnabled
        else:
            return Qt.ItemIsEnabled

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        if self.rowCount(parent):
            # We store the state of the row (checked and hidden) as
            # hidden last elements, so subtract 3
            return len(self.arraydata[0]) - 3
        else:
            return 0

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        if role == Qt.DisplayRole:
            return QVariant(self.arraydata[index.row()][index.column()])
        if role == Qt.CheckStateRole:
            if index.column() == 0: # and (not self.arraydata[index.row()][-3]):
                if self.arraydata[index.row()][-2]:
                    return QVariant(Qt.Checked)
                else:
                    return QVariant(Qt.Unchecked)
            #else:
            #    return QVariant()
        if role == Qt.ForegroundRole:
            if self.arraydata[index.row()][-3]:
                return QVariant(QColor(Qt.blue))
            else:
                return QVariant(QColor(Qt.black))
        return QVariant()

    def getRowDataList(self,index):
        return self.arraydata[index.row()][1:-3]

    def isInherited(self, index):
        return self.arraydata[index.row()][-3]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

    def sort(self, ncol = 1, order = Qt.AscendingOrder):
        """Sort table by given column number.
        """
        self.ncol = ncol
        if self.ncol != 0:
            self.emit(SIGNAL("layoutAboutToBeChanged()"))
            # Create a list to order the sort by
            orderList = range(len(self.headerdata))
            orderList.remove(self.ncol)
            orderList.insert(0,self.ncol)
            # Reverse loop through and order based on columns
            for col in reversed(orderList):
                self.arraydata = sorted(self.arraydata, key=operator.itemgetter(col))
            # Flip if ascending vs descending...
            if order == Qt.DescendingOrder:
                self.arraydata.reverse()
            self.emit(SIGNAL("layoutChanged()"))

    def checkStateOfCheckBoxes(self,newItemAdded):
#        if newItemAdded and self.editable:
#            # If we have a check then we enable delete
#            # REMOVED APR - self.parentWidget.deleteSelectedVariables.setEnabled(True)
#            self.parentWidget.checkSelectedVariables.setEnabled(True)
        # Else now we loop through the items and see if that was the last one removed
        foundOne = False
        for testCase in self.arraydata:
            if testCase[-2]:
                foundOne = True
#        if (not foundOne) and self.editable:
#            # REMOVED APR - self.parentWidget.deleteSelectedVariables.setEnabled(False)
#            self.parentWidget.checkSelectedVariables.setEnabled(False)

    def initCheckBoxes(self,checkList):
        # Loop through the items and see if it needs a check mark
        for testCase in self.arraydata:
            if checkList.count(testCase[1]) > 0:
                testCase[-2] = 1
        self.emit(SIGNAL("layoutChanged()"))

    def setData(self,index,value,role):
        # print "Set Data Pressed with %s" % (value.toString())
        # when setting the appropriate element of arraydata, trim off whitespace at the end
        # (this handles the common case of typing a cr after editing some data)
        if not index.isValid():
            return False
        if role == Qt.EditRole:
            trimmed_value = value.toString().trimmed()
            if self.arraydata[index.row()][index.column()] != trimmed_value:
                # Only update if we change something
                self.arraydata[index.row()][index.column()] = trimmed_value
                self.emit(SIGNAL('dataChanged(const QModelIndex &, '
                                 'const QModelIndex &)'), index, index)
                # Mark that the data for this row is dirty
                self.arraydata[index.row()][-1] = 1
                if self.parentWidget:
                    self.parentWidget.dirty = True
#                if self.parentWidget and self.parentWidget.saveChanges:
#                    self.parentWidget.saveChanges.setEnabled(True)
                return True
        if role == Qt.CheckStateRole:
            if index.column() == 0:
                state = value.toInt()[0]
                self.arraydata[index.row()][-2] = state
                self.checkStateOfCheckBoxes(state)
                self.emit(SIGNAL('dataChanged(const QModelIndex &, '
                 'const QModelIndex &)'), index, index)
        return False

    def insertRow(self, row, listToInsert, parent = QModelIndex()):
        # trim the QStrings in the new row if need be to remove whitespace at the end or beginning
        trimmedlist = []
        trimmedlist.append(listToInsert[0])
        for i in range(1,6):
            trimmedlist.append(listToInsert[i].trimmed())
        for i in range(6,len(listToInsert)):
            trimmedlist.append(listToInsert[i])
        returnval = QAbstractTableModel.insertRow(self,row,parent)
        self.beginInsertRows(parent,row,row)
        # Add the element
        if parent == QModelIndex():
            self.arraydata.insert(row,trimmedlist)
        self.endInsertRows()
        if self.parentWidget:
            self.parentWidget.dirty = True
#        if self.parentWidget and self.parentWidget.saveChanges:
#            self.parentWidget.saveChanges.setEnabled(True)
        return returnval

    def removeRow(self,row,parent = QModelIndex()):
        returnval = QAbstractTableModel.removeRow(self,row,parent)
        self.beginRemoveRows(parent,row,row)
        # Remove the element
        if parent == QModelIndex():
            self.arraydata.pop(row)
        self.endRemoveRows()
        if self.parentWidget:
            self.parentWidget.dirty = True
#        if self.parentWidget and self.parentWidget.saveChanges:
#            self.parentWidget.saveChanges.setEnabled(True)
        return returnval

    def deleteAllChecked(self):
        listIndexToRemove = []
        for i,testCase in enumerate(self.arraydata):
            if testCase[-2]:
                listIndexToRemove.insert(0,i)
        # List is now reverse so we will be poping items
        # off the end of the main element list and our
        # indexes will remain valid... i.e. go big to little index
        for index in listIndexToRemove:
            self.removeRow(index)
        self.checkStateOfCheckBoxes(False)

    def checkSyntax(self, row):
        variables = [(str(self.arraydata[row][1]), str(self.arraydata[row][2]), str(self.arraydata[row][3]), str(self.arraydata[row][4]), str(self.arraydata[row][5]))]
        return VariableValidator(self.opus_gui.project).check_parse_errors(variables = variables)

    def checkAgainstData(self, row):
        variables = [(str(self.arraydata[row][1]), str(self.arraydata[row][2]), str(self.arraydata[row][3]), str(self.arraydata[row][4]), str(self.arraydata[row][5]))]
        return VariableValidator(self.opus_gui.project).check_data_errors(variables = variables)


    def checkSelectedVariables(self):
        # check the variables in the expression library that have check boxes checked
        tocheck = []
        for i,testCase in enumerate(self.arraydata):
            if testCase[-2]:
                tocheck.append((str(self.arraydata[i][1]), str(self.arraydata[i][2]), str(self.arraydata[i][3]), str(self.arraydata[i][4]), str(self.arraydata[i][5])))
        success, msg = VariableValidator(self.opus_gui.project).validate(variables = tocheck,
                                     ok_msg = 'All expressions for selected variables parse correctly and can be executed on the baseyear data!')
        if success:
            MessageBox.information(mainwindow = self.parentWidget,
                              text = 'The expressions passed the tests.',
                              detailed_text = msg)            
        else:   
            MessageBox.warning(mainwindow = self.parentWidget,
                              text = 'Some or all expressions failed a test.',
                              detailed_text = msg)
            
    def checkAllVariables(self):
        # check all the variables in the expression library

#        1 variable_name
#        2 dataset_name
#        4 source
#        5 expression
        vars = [(str(v[1]), str(v[2]), str(v[3]), str(v[4]), str(v[5])) for v in self.arraydata]
        success,msg = VariableValidator(self.opus_gui.project).validate(variables = vars,
                                     ok_msg = 'All expressions parse correctly and can be executed on the baseyear data!')
        if success:
            MessageBox.information(mainwindow = self.parentWidget,
                              text = 'The expressions passed the tests.',
                              detailed_text = msg)            
        else:
            MessageBox.warning(mainwindow = self.parentWidget,
                              text = 'Some or all expressions failed a test.',
                              detailed_text = msg)


