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

from PyQt4.QtCore import QString, QObject, SIGNAL, Qt
from PyQt4.QtGui import QMessageBox, QComboBox, QGridLayout, \
                        QTextEdit, QTabWidget, QDialog, QPushButton, \
                        QGroupBox, QVBoxLayout, QIcon, QLabel

from opus_gui.results_manager.xml_helper_methods import ResultsManagerXMLHelper

from opus_gui.results_manager.run.opus_gui_thread import OpusGuiThread
from opus_gui.results_manager.run.batch_processor import BatchProcessor

class IndicatorBatchRunForm(QDialog):
    def __init__(self, mainwindow, result_manager, batch_name = None, simulation_run = None):
        QDialog.__init__(self, mainwindow)
        #mainwindow is an OpusGui
        self.mainwindow = mainwindow
        self.result_manager = result_manager
        self.toolboxBase = self.result_manager.mainwindow.toolboxBase

        
        self.inGui = False
        self.logFileKey = 0

        self.xml_helper = ResultsManagerXMLHelper(toolboxBase = self.toolboxBase)
        
        self.available_years_for_simulation_runs = {}

        self.batch_processor = BatchProcessor(
                                    toolboxBase = self.toolboxBase)
            
        self.batch_processor.guiElement = self
        
        self.setWindowTitle('Run indicator batch')
        self.widgetLayout = QVBoxLayout(self)
        self.widgetLayout.setAlignment(Qt.AlignTop)
        
        self.dataGroupBox = QGroupBox(self)
        self.widgetLayout.addWidget(self.dataGroupBox)
        
        self.simulation_run = simulation_run
        self.batch_name = batch_name

        self._setup_definition_widget()


        self._setup_buttons()
        #self._setup_tabs()
        
        
    def _setup_buttons(self):
        # Add Generate button...
        self.pbn_run_indicator_group = QPushButton(self)
        self.pbn_run_indicator_group.setObjectName("pbn_run_indicator_group")
        self.pbn_run_indicator_group.setText(QString("Run indicator group..."))
        
        QObject.connect(self.pbn_run_indicator_group, SIGNAL("released()"),
                        self.on_pbn_run_indicator_group_released)        
        self.widgetLayout.addWidget(self.pbn_run_indicator_group)
        
    def _setup_tabs(self):
        # Add a tab widget and layer in a tree view and log panel
        self.tabWidget = QTabWidget(self)
    
        # Log panel
        self.logText = QTextEdit(self)
        self.logText.setReadOnly(True)
        self.logText.setLineWidth(0)
        self.tabWidget.addTab(self.logText,"Log")

        # Finally add the tab to the model page
        self.widgetLayout.addWidget(self.tabWidget)
        
#
    def _setup_definition_widget(self):
                
        ##### setup data group box ####
        self.gridlayout2 = QGridLayout(self.dataGroupBox)
        self.gridlayout2.setObjectName("gridlayout2")
                
        self.lbl_yr1 = QLabel(self)
        self.lbl_yr1.setObjectName("lbl_yr1")
        self.lbl_yr1.setText(QString("From"))
                
        self.lbl_yr2 = QLabel(self)
        self.lbl_yr2.setObjectName("lbl_yr2")
        self.lbl_yr2.setText(QString("<center>to</center>"))

        self.lbl_yr3 = QLabel(self)
        self.lbl_yr3.setObjectName("lbl_yr3")
        self.lbl_yr3.setText(QString("<center>every</center>"))

        self.lbl_yr4 = QLabel(self)
        self.lbl_yr4.setObjectName("lbl_yr4")
        self.lbl_yr4.setText(QString("<center>years</center>"))
        
        self._setup_co__years()
        
        self.gridlayout2.addWidget(self.lbl_yr1,0,0,1,1)
        self.gridlayout2.addWidget(self.co_start_year,0,1,1,1)
        self.gridlayout2.addWidget(self.lbl_yr2,0,2,1,1)
        self.gridlayout2.addWidget(self.co_end_year,0,3,1,1)
        self.gridlayout2.addWidget(self.lbl_yr3,0,4,1,1)
        self.gridlayout2.addWidget(self.co_every_year,0,5,1,1)
        self.gridlayout2.addWidget(self.lbl_yr4,0,6,1,1)
        
    def _setup_co__years(self):     
        self.co_start_year = QComboBox(self.dataGroupBox)
        self.co_start_year.setObjectName("co_start_year")
        
        self.co_end_year = QComboBox(self.dataGroupBox)
        self.co_end_year.setObjectName("co_end_year")
        
        self.co_every_year = QComboBox(self.dataGroupBox)
        self.co_every_year.setObjectName("co_every_year")

        runs = self.xml_helper.get_available_run_info(
                   attributes = ['start_year', 'end_year'])
        
        for run in runs:
            if run['name'] == self.simulation_run:
                (start, end) = (run['start_year'], run['end_year'])
                break

        (start, end) = (int(start), int(end))
        for i in range(start, end + 1):
            yr = QString(repr(i))
            self.co_start_year.addItem(yr)
            self.co_end_year.addItem(yr)
        for i in range(1, end - start + 2):
            yr = QString(repr(i))
            self.co_every_year.addItem(yr)
                
    def on_pbnRemoveModel_released(self):
        self.result_manager.removeTab(self)
        self.result_manager.updateGuiElements()

    def on_pbn_run_indicator_group_released(self):

        self.pbn_run_indicator_group.setEnabled(False)
        
        start_year = int(self.co_start_year.currentText())
        end_year = int(self.co_end_year.currentText())
        increment = int(self.co_every_year.currentText())
        
        years = range(start_year, end_year + 1, increment)
        
        visualizations = self.xml_helper.get_batch_configuration(
                                batch_name = self.batch_name)
        
        self.batch_processor.set_data(
            visualizations = visualizations, 
            source_data_name = self.simulation_run,
            years = years)
                        
        self.runThread = OpusGuiThread(
                              parentThread = self.mainwindow,
                              parentGuiElement = self,
                              thread_object = self.batch_processor)
        
        # Use this signal from the thread if it is capable of producing its own status signal
        QObject.connect(self.runThread, SIGNAL("runFinished(PyQt_PyObject)"),
                        self.runFinishedFromThread)
        QObject.connect(self.runThread, SIGNAL("runError(PyQt_PyObject)"),
                        self.runErrorFromThread)
        
        self.runThread.start()

    # Called when the model is finished... 
    def runFinishedFromThread(self,success):            
        all_visualizations = self.batch_processor.get_visualizations()
        for indicator_type, visualizations in all_visualizations:
            if indicator_type == 'matplotlib_map' or \
               indicator_type == 'matplotlib_chart':
                form_generator = self.result_manager.addViewImageIndicator
            elif indicator_type == 'tab':
                form_generator = self.result_manager.addViewTableIndicator            
        
            if form_generator is not None:    
                for visualization in visualizations:
                    form_generator(visualization = visualization, indicator_type = indicator_type)    
            
        # Get the final logfile update after model finishes...
#        self.logFileKey = self.batch_processor._get_current_log(self.logFileKey)
        self.pbn_run_indicator_group.setEnabled(True)
        self.close()
    

    def runErrorFromThread(self,errorMessage):
        QMessageBox.warning(self.mainwindow, 'warning', errorMessage)
