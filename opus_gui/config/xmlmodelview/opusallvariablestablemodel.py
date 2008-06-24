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
 
    def rowCount(self, parent): 
        return len(self.arraydata) 
 
    def columnCount(self, parent): 
        if self.rowCount(parent):
            return len(self.arraydata[0]) 
        else:
            return 0
        
    def data(self, index, role): 
        if not index.isValid(): 
            return QVariant() 
        elif role != Qt.DisplayRole: 
            return QVariant() 
        return QVariant(self.arraydata[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

    def sort(self, ncol, order):
        """Sort table by given column number.
        """
        self.ncol = ncol
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
        
