# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt4.QtCore import QString
from PyQt4.QtGui import QWidget, QVBoxLayout, QIcon, QSizePolicy, QTableWidget, QTableWidgetItem

from opus_gui.main.controllers.dialogs.message_box import MessageBox

from opus_core.storage_factory import StorageFactory

class ViewTableForm(QWidget):
    def __init__(self, visualization, parent_widget = None):
        QWidget.__init__(self, parent_widget)
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
                msg = 'The table %s has been truncated to %i rows because of memory limitations.'%(visualization.table_name,limit)
                detailed_msg = '<qt>To view the full results, open the following file:<br><br><small>%s</small></qt>'%visualization.get_file_path()
                MessageBox.warning(mainwindow = self,
                                  text = msg,
                                  detailed_text = detailed_msg)
                break


        #self.tableWidget.resizeRowsToContents()
    def removeElement(self):
        return True
