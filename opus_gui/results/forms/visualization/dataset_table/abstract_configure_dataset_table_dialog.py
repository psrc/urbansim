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
from PyQt4.QtCore import QString, Qt
from PyQt4.QtGui import QDialog, QTableWidgetItem, QHeaderView


from opus_gui.results.forms.visualization.dataset_table.configure_dataset_table_ui import Ui_dlgDatasetTableDialog
from opus_gui.results.xml_helper_methods import ResultsManagerXMLHelper

class AbstractConfigureDatasetTableDialog(QDialog, Ui_dlgDatasetTableDialog):
    def __init__(self, resultManagerBase):
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint

        QDialog.__init__(self, resultManagerBase.mainwindow, flags)
        self.setupUi(self)
        self.resultManagerBase = resultManagerBase
        self.model = resultManagerBase.toolboxStuff.resultsManagerTree.model
        self.xml_helper = ResultsManagerXMLHelper(self.resultManagerBase.toolboxStuff)
        self.viz_type = 'Table (per year, spans indicators)'
        self.leVizName.setText(QString('(enter a name for this visualization)'))
        
        self.twAvailableIndicators.verticalHeader().hide()
        self.twIndicatorsToVisualize.verticalHeader().hide()
        
        self.twAvailableIndicators.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.twIndicatorsToVisualize.horizontalHeader().setResizeMode(QHeaderView.Stretch)

        self.lblOption1.hide()
        self.leOption1.hide()
                    
    def _setup_indicators(self, existing_indicators = []):
        indicators = self.xml_helper.get_available_indicator_names()

        for indicator in indicators:
            indicator_name = indicator['name']
            item = QTableWidgetItem(indicator_name)
            
            if str(indicator_name) not in existing_indicators:
                
                #self.lstAvailableIndicators.addItem(indicator_name)
                row = self.twAvailableIndicators.rowCount()
                self.twAvailableIndicators.insertRow(row)
                self.twAvailableIndicators.setItem(row, 0, item)
            else:
                #self.lstIndicatorsToVisualize.addItem(indicator_name)   
                row = self.twIndicatorsToVisualize.rowCount()
                self.twIndicatorsToVisualize.insertRow(row)
                self.twIndicatorsToVisualize.setItem(row, 0, item)     
                
    def _set_column(self, column, values):
        row = 0
        for value in values:
            item = QTableWidgetItem(value)
            self.twIndicatorsToVisualize.setItem(row, column, item)       
            row += 1      
                        
    def _setup_co_output_type(self, value = None):

        available_output_types = {
            'Tab delimited':'tab',
#            'Comma separated':'csv',
#            'Esri':'esri',
            'Database':'sql',
            'Fixed field':'fixed_field' 
        }
        
        if value is None:
            value = QString('Tab delimited')
        
        for otype in sorted(available_output_types.keys()):
            self.cboOutputType.addItem(QString(otype))
            
        for k,v in available_output_types.items():
            if v == value:
                idx = self.cboOutputType.findText(value)
                if idx != -1:
                    self.cboOutputType.setCurrentIndex(idx)        
                break
        
    def _setup_co_dataset_name(self, value = None):
        available_datasets = self.xml_helper.get_available_datasets()
        for dataset in available_datasets:
            self.cboDataset.addItem(QString(dataset))
        
        if value is not None:
            idx = self.cboDataset.findText(value)
            if idx != -1:
                self.cboDataset.setCurrentIndex(idx)
                           
    
    def _get_column_values(self, column = 0):
        #column 0 will get you the indicators
        col_vals = []
        for row in range(self.twIndicatorsToVisualize.rowCount()):
            item = self.twIndicatorsToVisualize.item(row,column)
            col_vals.append(str(item.text()))
        return col_vals
        
    def on_cboOutputType_currentIndexChanged(self, param):
        if isinstance(param, int):
            return #qt sends two signals for the same event; only process one
        
        
        output_type = str(param)

        if output_type in ['Fixed field', 'Database']:
            self.lblOption1.show()
            self.leOption1.show()
        else:
            self.lblOption1.hide()
            self.leOption1.hide()            
            
        if output_type == 'Fixed field':
            self.twIndicatorsToVisualize.horizontalHeader().showSection(1)            
        else:
            self.twIndicatorsToVisualize.horizontalHeader().hideSection(1)
            
        if output_type == 'Fixed field':
            self.lblOption1.setText(QString('ID format:'))
            self.lblOption1.setToolTip(QString('The fixed format of all id \ncolumns of the indicator result'))
        elif output_type == 'Database':
            self.lblOption1.setText(QString('Database name'))
            self.lblOption1.setToolTip(QString('The name of the database to \noutput the indicator result.\n The database will be created if \nit does not already exist. If a table with the same name \nas this indicator already exists in the database,\nit will be overwritten.'))
            
        
    def on_buttonBox_accepted(self):
        self.close()

    def on_buttonBox_rejected(self):
        self.close()
        

    def on_pbnAddIndicator_released(self):
        current_row = self.twAvailableIndicators.currentRow()
        self.move_item(self.twAvailableIndicators, self.twIndicatorsToVisualize, current_row)
        
    def on_pbnRemoveIndicator_released(self):
        current_row = self.twIndicatorsToVisualize.currentRow()
        self.move_item(self.twIndicatorsToVisualize, self.twAvailableIndicators, current_row)
            
    def move_item(self, from_table_widget, to_table_widget, row):
        value = QString(from_table_widget.item(row, 0).text())
        item = QTableWidgetItem(value) #need to create new item because QT deletes object
        if item is not None:
            last_row = to_table_widget.rowCount()
            to_table_widget.insertRow(last_row)
            to_table_widget.setItem(last_row, 0, QTableWidgetItem(value))
            if to_table_widget.columnCount() > 1:
                to_table_widget.setItem(last_row, 1, QTableWidgetItem())
        from_table_widget.removeRow(row)
        