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

from PyQt4.QtCore import QString, Qt, QSize
from PyQt4.QtGui import QWidget, QVBoxLayout, QIcon, QSizePolicy, \
                        QTableWidget, QTableWidgetItem


from opus_core.storage_factory import StorageFactory

class ViewTableForm(QWidget):
    def __init__(self, mainwindow, visualization):
        QWidget.__init__(self, mainwindow)
        self.mainwindow = mainwindow
        self.inGui = False

        self.widgetLayout = QVBoxLayout(self)
        
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setObjectName("tableWidget")
        size = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tableWidget.setSizePolicy(size)
        self.widgetLayout.addWidget(self.tableWidget)
        
        self.tabIcon = QIcon(":/Images/Images/map.png")
        
        self.tabLabel = visualization.table_name

        self.load_table(visualization = visualization)
    
    def load_table(self, visualization, limit = 10000):
            
        storage = StorageFactory().get_storage(
                       type = '%s_storage'%visualization.output_type,
                       storage_location = visualization.storage_location)
        table_data = storage.load_table(
                                table_name = visualization.table_name)
        
        try:
            primary_keys = visualization.indicators[0].primary_keys
        except:
            primary_keys = []
                        
        keys = primary_keys + [key for key in table_data.keys() 
                                   if key not in primary_keys]
        num_rows = min(len(table_data[keys[0]]), limit)
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
            
        self.tableWidget.resizeColumnsToContents()
        
        order = sorted(enumerate(table_data[keys[0]]), lambda (i,v),(j,v2): int(v*100)-int(v2*100))
        

        for i, (idx,v) in enumerate(order):
            row = QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(i,row)
            j = 0
            for key in keys:
                item = QTableWidgetItem()
                item.setText(QString(str(table_data[key][idx])))
                self.tableWidget.setItem(i,j,item)
                j += 1
            if i > limit:
                break
        
        
        #self.tableWidget.resizeRowsToContents()
    def removeElement(self):
        return True