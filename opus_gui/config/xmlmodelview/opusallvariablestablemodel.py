# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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



# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys
import operator

class OpusAllVariablesTableModel(QAbstractTableModel): 
    def __init__(self, datain, headerdata, parentWidget=None, *args): 
        QAbstractTableModel.__init__(self, parentWidget, *args) 
        self.arraydata = datain
        self.headerdata = headerdata
        self.parentWidget = parentWidget
 
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        if index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable # | Qt.ItemIsEditable           
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable                

    def rowCount(self, parent): 
        return len(self.arraydata) 
 
    def columnCount(self, parent): 
        if self.rowCount(parent):
            # We store the state of the row as a hidden last element, so subtract 1
            return len(self.arraydata[0]) - 1
        else:
            return 0
        
    def data(self, index, role): 
        if not index.isValid(): 
            return QVariant() 
        if role == Qt.DisplayRole:
            return QVariant(self.arraydata[index.row()][index.column()])
        if role == Qt.CheckStateRole:
            if index.column() == 0:
                if self.arraydata[index.row()][-1]:
                    return QVariant(Qt.Checked)
                else:
                    return QVariant(Qt.Unchecked)
        return QVariant()

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

    def sort(self, ncol, order):
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
            # Flip if accending vs decending...
            if order == Qt.DescendingOrder:
                self.arraydata.reverse()
            self.emit(SIGNAL("layoutChanged()"))
        

    def checkStateOfCheckBoxes(self,newItemAdded):
        if newItemAdded:
            # If we have a check then we enable delete
            self.parentWidget.deleteRow.setEnabled(True)
        # Else now we loop through the items and see if that was the last one removed
        foundOne = False
        for testCase in self.arraydata:
            if testCase[-1]:
                foundOne = True
        if not foundOne:
            self.parentWidget.deleteRow.setEnabled(False)        
        
    def setData(self,index,value,role):
        # print "Set Data Pressed with %s" % (value.toString())
        if not index.isValid():
            return False
        if role == Qt.EditRole:
            self.arraydata[index.row()][index.column()] = value.toString()
            self.emit(SIGNAL('dataChanged(const QModelIndex &, '
                             'const QModelIndex &)'), index, index)
            if self.parentWidget:
                self.parentWidget.dirty = True
            if self.parentWidget and self.parentWidget.saveChanges:
                self.parentWidget.saveChanges.setEnabled(True)  
            return True
        if role == Qt.CheckStateRole:
            if index.column() == 0:
                state = value.toInt()[0]
                self.arraydata[index.row()][-1] = state
                self.checkStateOfCheckBoxes(state)
        return False

    def removeRow(self,row,parent = QModelIndex()):
        returnval = QAbstractTableModel.removeRow(self,row,parent)
        self.beginRemoveRows(parent,row,row)
        # Remove the element
        if parent == QModelIndex():
            self.arraydata.pop(row)
        self.endRemoveRows()
        if self.parentWidget:
            self.parentWidget.dirty = True
        if self.parentWidget and self.parentWidget.saveChanges:
            self.parentWidget.saveChanges.setEnabled(True)  
        return returnval

    def deleteAllChecked(self):
        for i,testCase in enumerate(self.arraydata):
            if testCase[-1]:
                self.removeRow(i)
        self.checkStateOfCheckBoxes(False)
                
        
