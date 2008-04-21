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

from PyQt4.QtCore import QString, Qt
from PyQt4.QtGui import QWidget, QVBoxLayout, QIcon, \
                        QTableWidget, QTableWidgetItem


from opus_core.storage_factory import StorageFactory
from opus_gui.results.xml_helper_methods import elementsByAttributeValue, get_child_values

class ViewTableForm(QWidget):
    def __init__(self, parent, visualization):
        QWidget.__init__(self, parent)
        self.inGui = False

        self.widgetLayout = QVBoxLayout(self)
        
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setObjectName("tableWidget")
        self.widgetLayout.addWidget(self.tableWidget)
        
        self.tabIcon = QIcon(":/Images/Images/map.png")
        self.tabLabel = visualization.table_name

        self.load_table(visualization = visualization)
    
    def load_table(self, visualization):
                
        storage = StorageFactory().get_storage(
                       type = 'csv_storage',
                       storage_location = visualization.storage_location)
        table_data = storage.load_table(
                                table_name = visualization.table_name)
        
        try:
            primary_keys = visualization.indicators[0].primary_keys
        except:
            primary_keys = []
            
        print primary_keys
            
        keys = primary_keys + [key for key in table_data.keys() 
                                   if key not in primary_keys]
        num_rows = len(table_data[keys[0]])
        num_cols = len(keys)
        
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(num_cols)
        self.tableWidget.setRowCount(num_rows)
        
        j = 0
        for key in keys:
            col = QTableWidgetItem()
            col.setText(QString(key))
            self.tableWidget.setHorizontalHeaderItem(j,col)
            j += 1
            
        for i in range(num_rows):
            row = QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(i,row)
            j = 0
            for key in keys:
                item = QTableWidgetItem()
                item.setText(QString(repr(table_data[key][i])))
                self.tableWidget.setItem(i,j,item)
                j += 1
                
        self.tableWidget.resizeColumnsToContents()