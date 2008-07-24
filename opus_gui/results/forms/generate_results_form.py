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
                        QGroupBox, QVBoxLayout, QIcon, QLabel, QDialog

from opus_gui.results.xml_helper_methods import ResultsManagerXMLHelper

from opus_gui.results.gui_result_interface.opus_gui_thread import OpusGuiThread
from opus_gui.results.gui_result_interface.opus_result_generator import OpusResultGenerator

class GenerateResultsForm(QDialog):
    def __init__(self, mainwindow, result_manager, selected_item = None):
        QWidget.__init__(self, mainwindow)
        #mainwindow is an OpusGui
        self.mainwindow = mainwindow
        self.result_manager = result_manager
        self.toolboxStuff = self.result_manager.mainwindow.toolboxStuff

        self.inGui = False
        self.logFileKey = 0

        self.xml_helper = ResultsManagerXMLHelper(toolboxStuff = self.toolboxStuff)
        
        self.available_years_for_simulation_runs = {}
        
        self.result_generator = OpusResultGenerator(
                                    toolboxStuff = self.toolboxStuff)
            
        self.result_generator.guiElement = self
        
        self.tabIcon = QIcon(":/Images/Images/cog.png")
        self.tabLabel = "Generate results"

        self.widgetLayout = QVBoxLayout(self)
        self.widgetLayout.setAlignment(Qt.AlignTop)

        self.indicatorsGroupBox = QGroupBox(self)
        self.widgetLayout.addWidget(self.indicatorsGroupBox)
        
        self.dataGroupBox = QGroupBox(self)
        self.widgetLayout.addWidget(self.dataGroupBox)
        
        self._setup_definition_widget(selected_item)

        self._setup_buttons()
        self._setup_tabs()
        
        
    def _setup_buttons(self):
        # Add Generate button...
        self.pbn_generate_results = QPushButton(self.indicatorsGroupBox)
        self.pbn_generate_results.setObjectName("pbn_generate_results")
        self.pbn_generate_results.setText(QString("Generate results..."))
        
        QObject.connect(self.pbn_generate_results, SIGNAL("released()"),
                        self.on_pbn_generate_results_released)        
        self.widgetLayout.addWidget(self.pbn_generate_results)
        
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
    def _setup_definition_widget(self, selected_item):
        
        #### setup indicators group box ####
        
        self.gridlayout = QGridLayout(self.indicatorsGroupBox)
        self.gridlayout.setObjectName("gridlayout")

        self.lbl_indicator_name = QLabel(self.indicatorsGroupBox)
        self.lbl_indicator_name.setObjectName("lbl_indicator_name")
        self.lbl_indicator_name.setText(QString("Indicator"))
        self.gridlayout.addWidget(self.lbl_indicator_name,0,0,1,1)

        self._setup_co_indicator_name(selected_item)
        self.gridlayout.addWidget(self.co_indicator_name,0,1,1,1)

        self.lbl_dataset_name = QLabel(self.indicatorsGroupBox)
        self.lbl_dataset_name.setObjectName("lbl_dataset_name")
        self.lbl_dataset_name.setText(QString("Dataset"))
        self.gridlayout.addWidget(self.lbl_dataset_name,1,0,1,1)

        self._setup_co_dataset_name()
        self.gridlayout.addWidget(self.co_dataset_name,1,1,1,1)

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

        self._setup_co_source_data(selected_item)
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

    def _setup_co_indicator_name(self, selected_item):
        
        self.co_indicator_name = QComboBox(self.indicatorsGroupBox)
        self.co_indicator_name.setObjectName("co_indicator_name")
        
        self.co_indicator_name.addItem(QString("[select]"))
        
        indicators = self.xml_helper.get_available_indicator_names()
            
        for indicator in indicators:
            self.co_indicator_name.addItem(QString(indicator['name']))
            
        idx = self.co_indicator_name.findText(selected_item)
        if idx != -1:
            self.co_indicator_name.setCurrentIndex(idx)
        
        
    def _setup_co_dataset_name(self):

        self.co_dataset_name = QComboBox(self.indicatorsGroupBox)
        self.co_dataset_name.setObjectName("co_dataset_name")

        available_datasets = self.xml_helper.get_available_datasets()
        for dataset in available_datasets:
            self.co_dataset_name.addItem(QString(dataset))
            
    def _setup_co_source_data(self, selected_item):
        self.co_source_data = QComboBox(self.indicatorsGroupBox)
        self.co_source_data.setObjectName("co_source_data")
        
        self.co_source_data.addItem(QString("[select]"))
        
        runs = self.xml_helper.get_available_run_info(
                   attributes = ['start_year', 'end_year'])
        
        for run in runs:
            run_name = run['name']
            years = (run['start_year'], run['end_year'])
            self.co_source_data.addItem(QString(run_name))
            
            self.available_years_for_simulation_runs[run_name] = years

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
                
    def on_pbn_generate_results_released(self):

        self.pbn_generate_results.setEnabled(False)

        source_text = QString(self.co_source_data.currentText())
        if str(source_text) == '[select]':
            raise Exception('need to select a data source!!')
        
        indicator_text = QString(self.co_indicator_name.currentText())
        if str(indicator_text) == '[select]':
            raise Exception('need to select an indicator!!')
        
        dataset_name = str(self.co_dataset_name.currentText())
        if dataset_name == '[select]':
            raise Exception('need to select a dataset!!')
        
        start_year = int(self.co_start_year.currentText())
        end_year = int(self.co_end_year.currentText())
        increment = int(self.co_every_year.currentText())
        
        years = range(start_year, end_year + 1, increment)
        
        self.result_generator.set_data(
                                   source_data_name = source_text,
                                   indicator_name = indicator_text,
                                   dataset_name = dataset_name,
                                   years = years)
        
#        self.last_computed_result = {
#            'source_data_name': source_text,
#            'indicator_name': indicator_text,
#            'dataset_name': dataset_name,
#            'years': years                           
#        }
        
        self.runThread = OpusGuiThread(
                              parentThread = self.mainwindow,
                              parentGuiElement = self,
                              thread_object = self.result_generator)
        
        # Use this signal from the thread if it is capable of producing its own status signal
        QObject.connect(self.runThread, SIGNAL("runFinished(PyQt_PyObject)"),
                        self.runFinishedFromThread)
        QObject.connect(self.runThread, SIGNAL("runError(PyQt_PyObject)"),
                        self.runErrorFromThread)
        

        # Use this timer to call a function in the thread to check status if the thread is unable
        # to produce its own signal above
        self.timer = QTimer()
        QObject.connect(self.timer, SIGNAL("timeout()"),
                        self.runUpdateLog)
        self.timer.start(1000)
        
        self.runThread.start()

    def runUpdateLog(self):
        self.logFileKey = self.result_generator._get_current_log(self.logFileKey)

    # Called when the model is finished... 
    def runFinishedFromThread(self,success):
        print "Results generated met with success = ", success
        
        #self.update_results_xml()
        
        # Get the final logfile update after model finishes...
        self.logFileKey = self.result_generator._get_current_log(self.logFileKey)
        self.pbn_generate_results.setEnabled(True)
        self.close()
    
    def runErrorFromThread(self,errorMessage):
        QMessageBox.warning(self.mainwindow, 'Warning', errorMessage)
