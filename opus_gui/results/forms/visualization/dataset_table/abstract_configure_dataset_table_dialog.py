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
from PyQt4.QtGui import QDialog


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
        self.leVizName.setText(QString('DATASET-table per year'))
        
        
    def _setup_indicators(self, existing_indicators = []):
        indicators = self.xml_helper.get_available_indicator_names()
        for indicator in indicators:
            indicator_name = indicator['name']
            if str(indicator_name) not in existing_indicators:
                self.lstAvailableIndicators.addItem(indicator_name)
            else:
                self.lstIndicatorsToVisualize.addItem(indicator_name)        
        
    def _setup_co_output_type(self, value = None):

        available_output_types = {
            'Tab delimited':'tab',
            'Comma separated':'csv',
            'Esri':'esri',
            'Fixed format':'fixed_field' 
        }
        
        for otype in sorted(available_output_types.keys()):
            self.cboOutputType.addItem(QString(otype))
            
        if value is not None:
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
                           
    def _get_indicators(self):
        indicators = []
        for i in range(self.lstIndicatorsToVisualize.count()):
            item = self.lstIndicatorsToVisualize.item(i)
            indicators.append(str(item.text()))
        return indicators
            
    def on_buttonBox_accepted(self):
        self.close()

    def on_buttonBox_rejected(self):
        self.close()

    def on_pbnAddIndicator_released(self):
        item = self.lstAvailableIndicators.takeItem(self.lstAvailableIndicators.currentRow())
        if item is not None:
            self.lstIndicatorsToVisualize.addItem(item.text())
        
    def on_pbnRemoveIndicator_released(self):
        item = self.lstIndicatorsToVisualize.takeItem(self.lstIndicatorsToVisualize.currentRow())
        if item is not None:
            self.lstAvailableIndicators.addItem(item.text())
        

