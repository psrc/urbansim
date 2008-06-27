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
from PyQt4.QtCore import QString, Qt, QFileInfo
from PyQt4.QtGui import QDialog, QTableWidgetItem, QHeaderView, QFileDialog


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
        self.pbn_set_storage_location.hide()
        self.setToolTip(QString('In this visualization, a table of values \nwill be output for every simulation year. \nThe table consists of the ID columns \nof the specified dataset and \nthe values for each of the indicators \nspecified in this form.'))
                    
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
            'ESRI table':'esri',
            'Database':'sql',
            'Fixed field':'fixed_field' 
        }
        
        if value is None:
            value = QString('Tab delimited')
        
        for otype in sorted(available_output_types.keys()):
            self.cboOutputType.addItem(QString(otype))
            
        for k,v in available_output_types.items():
            if v == value:
                idx = self.cboOutputType.findText(k)
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
                           
    def _get_viz_spec(self, convert_to_node_dictionary = True):
        translation = {
            'Tab delimited':'tab',
            'Comma separated':'csv',
            'ESRI table':'esri',
            'Fixed field':'fixed_field',
            'Database':'sql'
        }
        dataset_name = self.cboDataset.currentText()
        output_type = QString(translation[str(self.cboOutputType.currentText())])
        indicators = QString(str(self._get_column_values(column = 0)))
                        
        vals = {
                'indicators': indicators,
                'output_type': output_type,
                'dataset_name': dataset_name
        }
        
        if output_type == 'fixed_field':
            fixed_field_params = QString(str(self._get_column_values(column = 1)))
            vals['fixed_field_specification'] = fixed_field_params
            vals['id_format'] = self.leOption1.text()
        elif output_type == 'sql':
            vals['database_name'] = self.leOption1.text()
        elif output_type == 'esri':
            vals['storage_location'] = self.leOption1.text()
        
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

        if output_type in ['Fixed field', 'Database', 'ESRI table']:
            self.lblOption1.show()
            self.leOption1.show()
        else:
            self.lblOption1.hide()
            self.leOption1.hide()            
            
        if output_type == 'Fixed field':
            self.twIndicatorsToVisualize.horizontalHeader().showSection(1)            
        else:
            self.twIndicatorsToVisualize.horizontalHeader().hideSection(1)
            
        if output_type == 'ESRI table':
            self.pbn_set_storage_location.show()
        else:
            self.pbn_set_storage_location.hide()

        if output_type == 'Fixed field':
            self.lblOption1.setText(QString('ID format:'))
            self.lblOption1.setToolTip(QString('The fixed format of all id \ncolumns of the indicator result'))
        elif output_type == 'Database':
            self.lblOption1.setText(QString('Database\nname:'))
            self.lblOption1.setToolTip(QString('The name of the SQL database to \noutput the indicator result.\n The database will be created if \nit does not already exist. If a table with the same name \nas this indicator already exists in the database,\nit will be overwritten.'))
        elif output_type == 'ESRI table':
            self.lblOption1.setText(QString('Database\npath'))
            self.lblOption1.setToolTip(QString('The location on disk of \na geodatabase file which \ncan then be loaded into ArcMap'))    
        
    def on_buttonBox_accepted(self):
        self.close()

    def on_buttonBox_rejected(self):
        self.close()
        

    def on_pbn_set_storage_location_released(self):
        from opus_core.misc import directory_path_from_opus_path
        start_dir = directory_path_from_opus_path('opus_gui.projects')
        
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
        