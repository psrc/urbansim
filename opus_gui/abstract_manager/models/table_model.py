# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from PyQt4.QtCore import Qt, QVariant, QAbstractTableModel, SIGNAL
from PyQt4.QtGui import QTextBrowser

import sys
import operator

class TableModel(QAbstractTableModel):
    def __init__(self, datain, headerdata, parentWidget=None, *args):
        QAbstractTableModel.__init__(self, parentWidget, *args)
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        if not self.arraydata:
            return 0
        if isinstance(self.arraydata,list):
            return len(self.arraydata)
        else:
            return 1

    def columnCount(self, parent):
        if not self.arraydata:
            return 0
        myList = self.arraydata[0]
        if isinstance(myList,tuple):
            return len(myList)
        else:
            return 1

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        if role == Qt.DisplayRole:
            if isinstance(self.arraydata,list):
                if isinstance(self.arraydata[index.row()],tuple):
                    myVal = self.arraydata[index.row()][index.column()]
                else:
                    myVal = self.arraydata[index.row()]
            else:
                myVal = self.arraydata
            if myVal.dtype.name in ['int', 'int32', 'int64']:
                return QVariant(int(myVal))
            elif myVal.dtype.name in ['float', 'float32','float64']:
                return QVariant(float(myVal))
            else:
                return QVariant(str(myVal))
        elif role == Qt.TextAlignmentRole:
            return QVariant(Qt.AlignRight)
        else:
            return QVariant()

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

    # Not currently used
    def sortorder(self,arraydata):
        orderList = range(len(self.headerdata))
        orderList.remove(self.ncol)
        orderList.insert(0,self.ncol)
        returnsortorder = tuple(orderList)
        return returnsortorder

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
            if len(self.headerdata) > 1 and isinstance(self.arraydata,list):
                self.arraydata = sorted(self.arraydata, key=operator.itemgetter(col))
            else:
                self.arraydata = sorted(self.arraydata)
        # Flip if accending vs decending...
        if order == Qt.DescendingOrder:
            if isinstance(self.arraydata,list):
                self.arraydata.reverse()
        self.emit(SIGNAL("layoutChanged()"))

class CatchOutput(QTextBrowser):
    class Output:
        def __init__( self, writefunc ):
            self.writefunc = writefunc
        def write( self, line ):
            if line != "\n":
                map( self.writefunc, line.split("\n") )
        def flush( self ):
            pass

    def __init__( self,parentWidget ):
        QTextBrowser.__init__( self, parentWidget )
        self.output = CatchOutput.Output(self.writeResult)
        self.stdout = sys.stdout
        self.stderr = sys.stderr
    def writeResult( self, result ):
        if result == "":
            return
        self.append( result )
    def start(self):
        #print "Getting Start"
        #sys.stdout, sys.stderr = self.output, self.output
        sys.stdout = self.output
    def stop(self):
        #print "Getting Stop"
        #sys.stdout, sys.stderr = self.stdout, self.stderr
        sys.stdout = self.stdout

