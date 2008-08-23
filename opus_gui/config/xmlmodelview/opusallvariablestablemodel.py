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



# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from opus_core.variables.variable_name import VariableName
import sys
import operator
from opus_gui.results.gui_result_interface.indicator_framework_interface import IndicatorFrameworkInterface
from opus_gui.results.gui_result_interface.opus_gui_thread import OpusGuiThread
from opus_gui.results.gui_result_interface.opus_result_generator import OpusResultGenerator

class OpusAllVariablesTableModel(QAbstractTableModel): 
    def __init__(self, datain, headerdata, parentWidget, editable=True, *args): 
        QAbstractTableModel.__init__(self, parentWidget, *args) 
        self.arraydata = datain
        self.headerdata = headerdata
        self.parentWidget = parentWidget
        self.editable = editable
 
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        if index.column() == 0:
            #if (not self.arraydata[index.row()][-3]) or (not self.editable):
            #    return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable
            #else:
            #    return Qt.ItemIsEnabled
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable
        elif self.editable:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable                
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
        if role == Qt.BackgroundRole:
            if self.arraydata[index.row()][-3]:
                return QVariant(QColor(Qt.darkGray))
            else:
                return QVariant(QColor(Qt.lightGray))
        return QVariant()

    def isInherited(self, index):
        return self.arraydata[index.row()][-3]

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
        if newItemAdded and self.editable:
            # If we have a check then we enable delete
            # REMOVED APR - self.parentWidget.deleteSelectedVariables.setEnabled(True)
            self.parentWidget.checkSelectedVariables.setEnabled(True)
        # Else now we loop through the items and see if that was the last one removed
        foundOne = False
        for testCase in self.arraydata:
            if testCase[-2]:
                foundOne = True
        if (not foundOne) and self.editable:
            # REMOVED APR - self.parentWidget.deleteSelectedVariables.setEnabled(False)        
            self.parentWidget.checkSelectedVariables.setEnabled(False)        
        
    def initCheckBoxes(self,checkList):
        # Loop through the items and see if it needs a check mark
        for testCase in self.arraydata:
            if checkList.count(testCase[1]) > 0:
                testCase[-2] = 1
        self.emit(SIGNAL("layoutChanged()"))

    def setData(self,index,value,role):
        # print "Set Data Pressed with %s" % (value.toString())
        if not index.isValid():
            return False
        if role == Qt.EditRole:
            if self.arraydata[index.row()][index.column()] != value.toString():
                # Only update if we change something
                self.arraydata[index.row()][index.column()] = value.toString()
                self.emit(SIGNAL('dataChanged(const QModelIndex &, '
                                 'const QModelIndex &)'), index, index)
                # Mark that the data for this row is dirty
                self.arraydata[index.row()][-1] = 1
                if self.parentWidget:
                    self.parentWidget.dirty = True
                if self.parentWidget and self.parentWidget.saveChanges:
                    self.parentWidget.saveChanges.setEnabled(True)  
                return True
        if role == Qt.CheckStateRole:
            if index.column() == 0:
                state = value.toInt()[0]
                self.arraydata[index.row()][-2] = state
                self.checkStateOfCheckBoxes(state)
        return False

    def insertRow(self, row, listToInsert, parent = QModelIndex()):
        returnval = QAbstractTableModel.insertRow(self,row,parent)
        self.beginInsertRows(parent,row,row)
        # Add the element
        if parent == QModelIndex():
            self.arraydata.insert(row,listToInsert)
        self.endInsertRows()
        if self.parentWidget:
            self.parentWidget.dirty = True
        if self.parentWidget and self.parentWidget.saveChanges:
            self.parentWidget.saveChanges.setEnabled(True)
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
        if self.parentWidget and self.parentWidget.saveChanges:
            self.parentWidget.saveChanges.setEnabled(True)  
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
        
    def checkSelectedVariables(self):
        # check the variables in the expression library that have check boxes checked
        tocheck = []
        for i,testCase in enumerate(self.arraydata):
            if testCase[-2]:
                tocheck.append(i)
        self._checkVariables(tocheck, 'All expressions for selected variables parse correctly and can be executed on the baseyear data!')
    
    def checkAllVariables(self):
        # check all the variables in the expression library
        self._checkVariables(range(len(self.arraydata)), 'All expressions parse correctly and can be executed on the baseyear data!')
    
    def _checkVariables(self, tocheck, ok_msg):
        # Helper method -- check the variables in the expression library as indexed by the list 'tocheck'.
        # Right now the only check is that the expression parses correctly; later we'll want to try 
        # evaluating it against the current cache.
        errors = []
        for i in tocheck:
            expr = str(self.arraydata[i][5])
            var_name = str(self.arraydata[i][1])
            dataset_name = str(self.arraydata[i][2])
                 
            try:
                VariableName(expr)
            except (SyntaxError, ValueError), e:
                errors.append("Parsing error: (%s, %s): %s" % (var_name, dataset_name, str(e)))
        
        if len(errors)==0:
            parsing_errors = False
        else:
            parsing_errors = True
            errorString = "Parse errors: <br><br>  " + "<br><br>".join(errors)
            QMessageBox.warning(self.parentWidget, 'Expression check results', errorString)

        
        errors = []
        for i in tocheck:
            var_name = str(self.arraydata[i][1])
            dataset_name = str(self.arraydata[i][2])
            successful, error = self._test_generate_results(indicator_name = var_name, dataset_name = dataset_name)
            if not successful:
                errors.append("Expression %s could not be run on <br>dataset %s on the baseyear data.<br>Details:<br>%s"%(
                                var_name, dataset_name, str(error) ))
            
            
        if len(errors) == 0 and not parsing_errors:
            QMessageBox.information(self.parentWidget, 'Expression check results', ok_msg)
        elif not parsing_errors:
            errorString = "Errors executing expression on baseyear data: <br><br>  " + "<br><br>".join(errors)
            QMessageBox.warning(self.parentWidget, 'Expression check results', errorString)            
        
    def _test_generate_results(self, indicator_name, dataset_name):
        
        interface = IndicatorFrameworkInterface(self.parentWidget.mainwindow.toolboxStuff)
        node, vals = interface.xml_helper.get_element_attributes(node_name = 'base_year_data', 
                                                                 child_attributes = ['start_year'],
                                                                 node_type = 'source_data')
        years = [int(str(vals['start_year']))]

        result_generator = OpusResultGenerator(self.parentWidget.mainwindow.toolboxStuff)
        result_generator.set_data(
               source_data_name = 'base_year_data',
               indicator_name = indicator_name,
               dataset_name = dataset_name,
               years = years)
        
        try:
            result_generator.run(raise_exception = True)
            return True, None
        except Exception, e:
            return False, e
