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

from PyQt4.QtCore import QString, QObject, SIGNAL, \
                         Qt, QTimer, QModelIndex
from PyQt4.QtGui import QMessageBox, QComboBox, QGridLayout, \
                        QTextEdit, QTabWidget, QWidget, QPushButton, \
                        QGroupBox, QVBoxLayout, QIcon, QLabel

from opus_gui.results.xml_helper_methods import elementsByAttributeValue, get_child_values

from opus_gui.results.gui_result_interface.opus_gui_thread import OpusGuiThread
from opus_gui.results.gui_result_interface.opus_result_generator import OpusResultGenerator
from opus_gui.results.gui_result_interface.opus_result_visualizer import OpusResultVisualizer
from opus_gui.results.gui_result_interface.opus_indicator_group_processor import OpusIndicatorGroupProcessor

from opus_gui.config.xmlmodelview.opusdataitem import OpusDataItem

class IndicatorGroupRunForm(QWidget):
    def __init__(self, parent, result_manager, selected_item = None, simulation_run = None):
        QWidget.__init__(self, parent)
        #parent is an OpusGui
        self.parent = parent
        self.result_manager = result_manager
        self.toolboxStuff = self.result_manager.parent.toolboxStuff

        self.inGui = False
        self.logFileKey = 0
        self.domDocument = self.toolboxStuff.doc
        
        self.available_years_for_simulation_runs = {}

        self.result_generator = OpusIndicatorGroupProcessor(
                                    xml_path = self.toolboxStuff.xml_file,
                                    domDocument = self.domDocument,
                                    model = self.toolboxStuff.resultsManagerTree.model)
            
        self.result_generator.guiElement = self
        
        self.tabIcon = QIcon(":/Images/Images/cog.png")
        self.tabLabel = "Run indicator group"

        self.widgetLayout = QVBoxLayout(self)
        self.widgetLayout.setAlignment(Qt.AlignTop)

        self.indicatorsGroupBox = QGroupBox(self)
        self.widgetLayout.addWidget(self.indicatorsGroupBox)
        
        self.dataGroupBox = QGroupBox(self)
        self.widgetLayout.addWidget(self.dataGroupBox)
        
        self._setup_definition_widget(selected_item, simulation_run)

        self._setup_buttons()
        self._setup_tabs()
        
        
    def _setup_buttons(self):
        # Add Generate button...
        self.pbn_run_indicator_group = QPushButton(self.indicatorsGroupBox)
        self.pbn_run_indicator_group.setObjectName("pbn_run_indicator_group")
        self.pbn_run_indicator_group.setText(QString("Run indicator group..."))
        
        QObject.connect(self.pbn_run_indicator_group, SIGNAL("released()"),
                        self.on_pbn_run_indicator_group_released)        
        self.widgetLayout.addWidget(self.pbn_run_indicator_group)
        
    def _setup_tabs(self):
        # Add a tab widget and layer in a tree view and log panel
        self.tabWidget = QTabWidget(self.indicatorsGroupBox)
    
        # Log panel
        self.logText = QTextEdit(self.indicatorsGroupBox)
        self.logText.setReadOnly(True)
        self.logText.setLineWidth(0)
        self.tabWidget.addTab(self.logText,"Log")

        # Finally add the tab to the model page
        self.widgetLayout.addWidget(self.tabWidget)
        
#
    def _setup_definition_widget(self, selected_item, simulation_run):
        
        #### setup indicators group box ####
        
        self.gridlayout = QGridLayout(self.indicatorsGroupBox)
        self.gridlayout.setObjectName("gridlayout")

        self.lbl_indicator_name = QLabel(self.indicatorsGroupBox)
        self.lbl_indicator_name.setObjectName("lbl_indicator_name")
        self.lbl_indicator_name.setText(QString("Indicator group"))
        self.gridlayout.addWidget(self.lbl_indicator_name,0,0,1,1)

        self._setup_co_indicator_group_name(selected_item)
        self.gridlayout.addWidget(self.co_indicator_group_name,0,1,1,1)

        ##### setup data group box ####
        self.gridlayout2 = QGridLayout(self.dataGroupBox)
        self.gridlayout2.setObjectName("gridlayout2")
                
        self.lbl_source_data = QLabel(self.indicatorsGroupBox)
        self.lbl_source_data.setObjectName("lbl_source_data")
        self.lbl_source_data.setText(QString("Simulation data"))
        self.gridlayout2.addWidget(self.lbl_source_data,0,0,1,3)
                
        self.lbl_yr1 = QLabel(self.indicatorsGroupBox)
        self.lbl_yr1.setObjectName("lbl_yr1")
        self.lbl_yr1.setText(QString("From"))
                
        self.lbl_yr2 = QLabel(self.indicatorsGroupBox)
        self.lbl_yr2.setObjectName("lbl_yr2")
        self.lbl_yr2.setText(QString("<center>to</center>"))

        self.lbl_yr3 = QLabel(self.indicatorsGroupBox)
        self.lbl_yr3.setObjectName("lbl_yr3")
        self.lbl_yr3.setText(QString("<center>every</center>"))

        self.lbl_yr4 = QLabel(self.indicatorsGroupBox)
        self.lbl_yr4.setObjectName("lbl_yr4")
        self.lbl_yr4.setText(QString("<center>years</center>"))
        
        self._setup_co__years()

        self._setup_co_source_data(simulation_run)
        self.gridlayout2.addWidget(self.co_source_data,0,3,1,4) 
        
        self.gridlayout2.addWidget(self.lbl_yr1,1,0,1,1)
        self.gridlayout2.addWidget(self.co_start_year,1,1,1,1)
        self.gridlayout2.addWidget(self.lbl_yr2,1,2,1,1)
        self.gridlayout2.addWidget(self.co_end_year,1,3,1,1)
        self.gridlayout2.addWidget(self.lbl_yr3,1,4,1,1)
        self.gridlayout2.addWidget(self.co_every_year,1,5,1,1)
        self.gridlayout2.addWidget(self.lbl_yr4,1,6,1,1)
        
        QObject.connect(self.co_source_data, SIGNAL("currentIndexChanged(int)"),
                self.on_co_source_data_value_changed)

    def _setup_co_indicator_group_name(self, selected_item):
        
        self.co_indicator_group_name = QComboBox(self.indicatorsGroupBox)
        self.co_indicator_group_name.setObjectName("co_indicator_group_name")
                
        node_list = elementsByAttributeValue(domDocument = self.domDocument, 
                                              attribute = 'type', 
                                              value = 'indicator_group')

        for element, node in node_list:
            self.co_indicator_group_name.addItem(QString(element.nodeName()))
            
        idx = self.co_indicator_group_name.findText(selected_item)
        if idx != -1:
            self.co_indicator_group_name.setCurrentIndex(idx)
            
    def _setup_co_source_data(self, selected_item):
        self.co_source_data = QComboBox(self.indicatorsGroupBox)
        self.co_source_data.setObjectName("co_source_data")
                
        node_list = elementsByAttributeValue(domDocument = self.domDocument, 
                                              attribute = 'type', 
                                              value = 'source_data')
        
        for element, node in node_list:
            self.co_source_data.addItem(QString(element.nodeName()))
            vals = get_child_values(parent = node, 
                                    child_names = ['start_year', 'end_year'])
            
            self.available_years_for_simulation_runs[element.nodeName()] = (vals['start_year'],
                                                                         vals['end_year'])

        idx = self.co_source_data.findText(selected_item)
        if idx != -1:
            self.co_source_data.setCurrentIndex(idx)
            self.on_co_source_data_value_changed(idx)
            
            
    def _setup_co__years(self):     
        self.co_start_year = QComboBox(self.dataGroupBox)
        self.co_start_year.setObjectName("co_start_year")
        
        self.co_end_year = QComboBox(self.dataGroupBox)
        self.co_end_year.setObjectName("co_end_year")
        
        self.co_every_year = QComboBox(self.dataGroupBox)
        self.co_every_year.setObjectName("co_every_year")

                    
    def on_pbnRemoveModel_released(self):
        self.result_manager.removeTab(self)
        self.result_manager.updateGuiElements()
        
    def on_co_source_data_value_changed(self, ind):
        print 'source_data value changed!'
        txt = self.co_source_data.currentText()
        if txt in self.available_years_for_simulation_runs:
            self.co_start_year.clear()
            self.co_end_year.clear()
            self.co_every_year.clear()
            (start, end) = self.available_years_for_simulation_runs[txt]
            (start, end) = (int(start), int(end))
            for i in range(start, end + 1):
                yr = QString(repr(i))
                self.co_start_year.addItem(yr)
                self.co_end_year.addItem(yr)
            for i in range(1, end - start + 2):
                yr = QString(repr(i))
                self.co_every_year.addItem(yr)

    def _get_indicators_for_group(self, parent):
        viz_map = {
            'Map (per indicator per year)':'matplotlib_map',
            'Chart (per indicator, spans years)':'matplotlib_chart',
            'Table (per indicator, spans years)':'table_per_attribute',
            'Table (per year, spans indicators)':'table_per_year',
            'ESRI table (for loading in ArcGIS)':'table_esri'
        }
        
        indicators = {}
        node = parent.firstChild()
        while not node.isNull():
            indicator_name = str(node.nodeName())
            vals = get_child_values(node, ['visualization_type','dataset_name'])
            visualization_type = viz_map[str(vals['visualization_type'])]
            dataset_name = str(vals['dataset_name'])

            if (visualization_type, dataset_name) not in indicators:
                indicators[(visualization_type, dataset_name)] = [indicator_name]
            else:
                indicators[(visualization_type, dataset_name)].append(indicator_name)
            node = node.nextSibling()
        return indicators

    def on_pbn_run_indicator_group_released(self):
        # Fire up a new thread and run the model
        print "Generate results button pressed"

        # References to the GUI elements for status for this run...
        #self.statusLabel = self.runStatusLabel
        #self.statusLabel.setText(QString("Model initializing..."))

        source_text = QString(self.co_source_data.currentText())
        indicator_group = QString(self.co_indicator_group_name.currentText())
        indicator_group_node = self.domDocument.elementsByTagName(indicator_group).item(0)
        
        indicators_to_run = self._get_indicators_for_group(parent = indicator_group_node)
                
        self.pbn_run_indicator_group.setEnabled(False)

        start_year = int(self.co_start_year.currentText())
        end_year = int(self.co_end_year.currentText())
        increment = int(self.co_every_year.currentText())
        
        years = range(start_year, end_year + 1, increment)
        
        self.result_generator.set_data(
            indicator_defs = indicators_to_run, 
            source_data_name = source_text,
            years = years)
                    
            
        self.runThread = OpusGuiThread(
                              parentThread = self.parent,
                              parent = self,
                              thread_object = self.result_generator)
        
        # Use this signal from the thread if it is capable of producing its own status signal
        QObject.connect(self.runThread, SIGNAL("runFinished(PyQt_PyObject)"),
                        self.runFinishedFromThread)
        QObject.connect(self.runThread, SIGNAL("runError(PyQt_PyObject)"),
                        self.runErrorFromThread)
        

        self.runThread.start()

    # Called when the model is finished... 
    def runFinishedFromThread(self,success):
        print "Results generated met with success = ", success
            
        all_visualizations = self.result_generator.get_visualizations()
        for indicator_type, visualizations in all_visualizations:
            if indicator_type == 'matplotlib_map' or \
               indicator_type == 'matplotlib_chart':
                form_generator = self.result_manager.addViewImageIndicator
            elif indicator_type == 'table_per_year' or \
                 indicator_type == 'table_per_attribute':
                form_generator = self.result_manager.addViewTableIndicator            
        
            if form_generator is not None:    
                for visualization in visualizations:
                    form_generator(visualization = visualization, indicator_type = indicator_type)    
            
        # Get the final logfile update after model finishes...
#        self.logFileKey = self.result_generator._get_current_log(self.logFileKey)
        self.pbn_run_indicator_group.setEnabled(True)
    

    def runErrorFromThread(self,errorMessage):
        QMessageBox.warning(self.parent,"Warning",errorMessage)
