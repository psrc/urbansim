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
from PyQt4.QtCore import QString, Qt, QFileInfo
from PyQt4.QtGui import QDialog, QTableWidgetItem, QFileDialog, QMessageBox
import os

from opus_gui.results_manager.views.ui_configure_dataset_table import Ui_dlgDatasetTableDialog
from opus_gui.results_manager.xml_helper_methods import ResultsManagerXMLHelper
from opus_gui.results_manager.run.indicator_framework.visualizer.visualizers.table import Table
from opus_gui.util.exception_formatter import formatExceptionInfo
from opus_core.logger import logger

class AbstractConfigureBatchIndicatorVisualization(QDialog, Ui_dlgDatasetTableDialog):
    def __init__(self, resultManagerBase):
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint

        QDialog.__init__(self, resultManagerBase.mainwindow, flags)
        self.setModal(True)
        self.setupUi(self)
        self.resultManagerBase = resultManagerBase
        self.model = resultManagerBase.toolboxBase.resultsManagerTree.model
        self.xml_helper = ResultsManagerXMLHelper(self.resultManagerBase.toolboxBase)
        self.leVizName.setText(QString('New visualization'))
        self.dataset_name = None
#        self.twAvailableIndicators.verticalHeader().hide()
#        self.twIndicatorsToVisualize.verticalHeader().hide()
#        
#        self.twAvailableIndicators.horizontalHeader().setResizeMode(QHeaderView.Stretch)
#        self.twIndicatorsToVisualize.horizontalHeader().setResizeMode(QHeaderView.Stretch)

        self.lblOption1.hide()
        self.leOption1.hide()
        self.pbn_set_storage_location.hide()
        #self.setToolTip(QString('In this visualization, a table of values \nwill be output for every simulation year. \nThe table consists of the ID columns \nof the specified dataset and \nthe values for each of the indicators \nspecified in this form.'))
                    

    def _setup_indicators(self, existing_indicators = []):
        if self.dataset_name is None: return
        
        indicators = self.xml_helper.get_available_indicator_names(attributes = ['dataset'])
        
        current_row = self.twAvailableIndicators.currentRow()
        
        self.twAvailableIndicators.clear()
        self.twAvailableIndicators.setColumnCount(2)
        self.twAvailableIndicators.horizontalHeader().setStretchLastSection(True) 
        self.twIndicatorsToVisualize.horizontalHeader().setStretchLastSection(True)
        
        while self.twAvailableIndicators.rowCount() > 0:
            self.twAvailableIndicators.removeRow(0)
            
        while self.twIndicatorsToVisualize.rowCount() > 0:
            self.twIndicatorsToVisualize.removeRow(0)
        
#        self.twAvailableIndicators.setRowCount(len(indicators) - len(existing_indicators))
        
        col = QTableWidgetItem()
        col.setText(QString('Name'))
        self.twAvailableIndicators.setHorizontalHeaderItem(0,col)
        
        #col = QTableWidgetItem()
        #col.setText(QString('Dataset'))
        #self.twAvailableIndicators.setHorizontalHeaderItem(1,col)

        col = QTableWidgetItem()
        col.setText(QString('Definition'))
        self.twAvailableIndicators.setHorizontalHeaderItem(1,col)
                    
        self.indicators = {}
        
        for indicator in indicators:
            
            name = indicator['name']
            
            self.indicators[name] = indicator
        
            if name not in existing_indicators:
                if self.dataset_name == indicator['dataset']:
                    item = QTableWidgetItem()
                    item.setText(indicator['name'])
                    row = self.twAvailableIndicators.rowCount()
                    self.twAvailableIndicators.insertRow(row)
                    #self.twAvailableIndicators.setVerticalHeaderItem(row,QTableWidgetItem())
    
                    self.twAvailableIndicators.setItem(row,0,item)
        
                    #item = QTableWidgetItem()
                    #item.setText(indicator['dataset'])
                    #self.twAvailableIndicators.setItem(i,1,item)
                
                    item = QTableWidgetItem()
                    item.setText(indicator['value'])
                    self.twAvailableIndicators.setItem(row,1,item)
            else:
                if self.dataset_name != indicator['dataset']:
                    logger.log_warning('Visualization configured incorrectly. Cannot have indicators for different datasets. Skipping indicator %s'%str(indicator['name']))
                    continue
                item = QTableWidgetItem()
                item.setText(indicator['name'])                
                row = self.twIndicatorsToVisualize.rowCount()
                self.twIndicatorsToVisualize.insertRow(row)
                self.twIndicatorsToVisualize.setItem(row, 0, item)     
                
              
                
        if current_row is None or current_row == -1:
            current_row = 0

        self.twAvailableIndicators.setCurrentCell(current_row,0)

#        self.twAvailableIndicators.resizeColumnsToContents()
#        self.twAvailableIndicators.resizeRowsToContents()
#        
#        self.twIndicatorsToVisualize.resizeColumnsToContents()
#        self.twIndicatorsToVisualize.resizeRowsToContents()
        
        
    def _set_column(self, column, values):
        row = 0
        for value in values:
            item = QTableWidgetItem(value)
            self.twIndicatorsToVisualize.setItem(row, column, item)       
            row += 1      
                        
    def _get_output_types(self, viz_type):
        if str(viz_type) == 'Table':
            available_output_types = {
                'Tab delimited file (.tab)':'tab',
    #            'Comma separated':'csv',
                'ESRI database':'esri',
                'Export to SQL database':'sql',
                'Fixed field file (.dat)':'fixed_field' 
            }       
        elif str(viz_type) == 'Map':
            available_output_types = {
                'Matplotlib map (.png)':'matplotlib_map',
            }            
        else:
            available_output_types = {}
            
        return available_output_types
            
                      
    def _setup_co_output_type(self, value = None):
        viz_type = self.cboVizType.currentText()
        available_output_types = self._get_output_types(viz_type = viz_type)
        
        if value is None:
            value = 'Tab delimited file (.tab)'
 
        loc = -1
        self.cboOutputType.clear()
        for idx,(k,v) in enumerate(available_output_types.items()):
            self.cboOutputType.addItem(QString(k))

            if k == value:
                loc = idx
                
        if loc != -1:
            self.cboOutputType.setCurrentIndex(loc)  
            if loc == 0:
                self.on_cboOutputType_currentIndexChanged(QString(value))      
        
    def _setup_co_dataset_name(self, value = None):
        available_datasets = self.xml_helper.get_available_datasets()

        for dataset in available_datasets:
            self.cboDataset.addItem(QString(dataset))
        
        if value is not None:
            idx = self.cboDataset.findText(value)
            if idx != -1:
                self.dataset_name = value
                self.cboDataset.setCurrentIndex(idx)        
        
        if value is None or idx == -1:
            self.dataset_name = QString(str(self.cboDataset.currentText()))

    def _setup_co_viz_type(self, value = None):
        
        if value is not None:
            idx = self.cboVizType.findText(value)
            if idx != -1:
                self.cboVizType.setCurrentIndex(idx)        
            
    def on_cboVizType_currentIndexChanged(self, param):
        if isinstance(param, int):
            return #qt sends two signals for the same event; only process one
        
        self._setup_co_output_type()
             
    def on_cboDataset_currentIndexChanged(self, param):

        if isinstance(param, int):
            return #qt sends two signals for the same event; only process one
        
        dataset = param
        if self.dataset_name != dataset:
            self.dataset_name = QString(str(dataset))
            self._setup_indicators()

                           
    def _get_type_mapper(self):
        return {
            'Table': 'tab',
            'Map': 'matplotlib_map'
        }
    def _get_inverse_type_mapper(self):
        mapper = self._get_type_mapper()
        inv = dict([(v,k) for k,v in mapper.items()])
        
        return inv
        
    def _get_viz_spec(self, convert_to_node_dictionary = True):
        viz_type = self.cboVizType.currentText()
        translation = self._get_output_types(viz_type)
        dataset_name = self.dataset_name
        output_type = QString(translation[str(self.cboOutputType.currentText())])
        indicators = QString(str(self._get_column_values(column = 0)))
                        
        vals = {
                'indicators': indicators,
                'output_type': output_type,
                'dataset_name': dataset_name,
                'visualization_type': QString(self._get_type_mapper()[str(viz_type)])
        }
        
        if output_type == 'fixed_field':
            try:
                fixed_field_params = QString(str(self._get_column_values(column = 1)))
            except:
                errorInfo = formatExceptionInfo(custom_message = 'Could not get fixed field parameters for all columns')
                logger.log_error(errorInfo)
                QMessageBox.warning(self.mainwindow, 'Warning', QString(errorInfo))
                return None
                
            vals['fixed_field_specification'] = fixed_field_params
            vals['id_format'] = self.leOption1.text()
        elif output_type == 'sql':
            vals['database_name'] = self.leOption1.text()
        elif output_type == 'esri':
            vals['storage_location'] = self.leOption1.text()
        elif output_type == 'tab':
            if self.rbSingleTable.isChecked():
                output_style = Table.ALL
            elif self.rbTablePerIndicator.isChecked():
                output_style = Table.PER_ATTRIBUTE
            elif self.rbTablePerYear.isChecked():
                output_style = Table.PER_YEAR
                
            vals['output_style'] = QString(str(output_style))
        
        if convert_to_node_dictionary:
            node_vals = []
            for k,v in vals.items():
                node_vals.append({'name':k, 'value':v})
            vals = node_vals
        return vals
        
        
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

        if output_type in ['Fixed field file (.dat)', 'Export to SQL database', 'ESRI database']:
            self.lblOption1.show()
            self.leOption1.show()
            self.leOption1.activateWindow()
            self.rbSingleTable.hide()
            self.rbTablePerIndicator.hide()
            self.rbTablePerYear.hide()
        else:
            self.lblOption1.hide()
            self.leOption1.hide()     
            if output_type == 'Tab delimited file (.tab)':       
                self.rbSingleTable.show()
                self.rbTablePerIndicator.show()
                self.rbTablePerYear.show()
            else:
                self.rbSingleTable.hide()
                self.rbTablePerIndicator.hide()
                self.rbTablePerYear.hide()                
            
                        
        if output_type == 'Fixed field file (.dat)':
            self.twIndicatorsToVisualize.horizontalHeader().showSection(1)            
            self.twIndicatorsToVisualize.resizeColumnsToContents()
        else:
            self.twIndicatorsToVisualize.horizontalHeader().hideSection(1)
            
        if output_type == 'ESRI database':
            self.pbn_set_storage_location.show()
        else:
            self.pbn_set_storage_location.hide()

        if output_type == 'Fixed field file (.dat)':
            self.lblOption1.setText(QString('ID format:'))
            self.lblOption1.setToolTip(QString('The fixed format of all id \ncolumns of the indicator result'))
        elif output_type == 'Export to SQL database':
            self.lblOption1.setText(QString('Database name:'))
            self.lblOption1.setToolTip(QString('The name of the SQL database to \noutput the indicator result.\n The database will be created if \nit does not already exist. If a table with the same name \nas this indicator already exists in the database,\nit will be overwritten.'))
        elif output_type == 'ESRI database':
            self.lblOption1.setText(QString('Path:'))
            self.lblOption1.setToolTip(QString('The location on disk of \na geodatabase file which \ncan then be loaded into ArcMap'))    
        
    def on_buttonBox_accepted(self):
        self.close()

    def on_buttonBox_rejected(self):
        self.close()

    def on_pbn_set_storage_location_released(self):
        start_dir = os.path.join(os.environ['OPUS_HOME'], 'project_configs')
        
        configDialog = QFileDialog()
        filter_str = QString("*.gdb")
        fd = configDialog.getExistingDirectory(self,
                    QString("Please select an ESRI geodatabase (*.gdb)..."), #, *.sde, *.mdb)..."),
                    QString(start_dir), QFileDialog.ShowDirsOnly)
        if len(fd) != 0:
            fileName = QString(fd)
            fileNameInfo = QFileInfo(QString(fd))
            fileNameBaseName = fileNameInfo.completeBaseName()
            self.leOption1.setText(fileName)

    def on_pbnAddIndicator_released(self):
        row = self.twAvailableIndicators.currentRow()
        from_table_widget = self.twAvailableIndicators
        to_table_widget = self.twIndicatorsToVisualize
        
        cur_value = from_table_widget.item(row, 0)
        if cur_value is not None:
            indicator_name = QString(cur_value.text())
            last_row = to_table_widget.rowCount()
            to_table_widget.insertRow(last_row)
            to_table_widget.setItem(last_row, 0, QTableWidgetItem(indicator_name))
            if to_table_widget.columnCount() > 1:
                to_table_widget.setItem(last_row, 1, QTableWidgetItem())
                
        from_table_widget.removeRow(row)        
                
    def on_pbnRemoveIndicator_released(self):
        row = self.twIndicatorsToVisualize.currentRow()
        from_table_widget = self.twIndicatorsToVisualize
        to_table_widget = self.twAvailableIndicators
        
        cur_item = from_table_widget.item(row, 0)
        if cur_item is not None:
            value = QString(cur_item.text())
            
            item = QTableWidgetItem(value) #need to create new item because QT deletes object
            last_row = to_table_widget.rowCount()
            indicator = self.indicators[value]
            new_row = QTableWidgetItem()
            self.twAvailableIndicators.setRowCount(last_row + 1)
            self.twAvailableIndicators.setVerticalHeaderItem(last_row,new_row)
    
            self.twAvailableIndicators.setItem(last_row,0,item)
    
            item = QTableWidgetItem()
            item.setText(indicator['dataset'])
            self.twAvailableIndicators.setItem(last_row,1,item)
        
            item = QTableWidgetItem()
            item.setText(indicator['value'])
            self.twAvailableIndicators.setItem(last_row,2,item)  
                
        from_table_widget.removeRow(row)      
#        if self.twIndicatorsToVisualize.rowCount() == 0:
#            self.dataset_name = None
        

