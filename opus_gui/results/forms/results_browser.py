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

from PyQt4.QtCore import QString, QObject, SIGNAL, Qt
from PyQt4.QtGui import QMessageBox, QComboBox, QGridLayout, \
                        QTextEdit, QTabWidget, QWidget, QPushButton, \
                        QGroupBox, QVBoxLayout, QIcon, QLabel, \
                        QTableWidget, QTableWidgetItem

from opus_gui.results.xml_helper_methods import ResultsManagerXMLHelper

from opus_gui.results.gui_result_interface.opus_gui_thread import OpusGuiThread
from opus_gui.results.gui_result_interface.batch_processor import BatchProcessor

from opus_gui.results.forms.results_browser_ui import Ui_ResultsBrowser
from opus_gui.results.forms.view_image_form import ViewImageForm
from opus_gui.results.forms.view_table_form import ViewTableForm

from copy import copy

class ResultBrowser(QWidget, Ui_ResultsBrowser):
    def __init__(self, mainwindow, gui_result_manager):
        QWidget.__init__(self, mainwindow)
        self.setupUi(self)
        
        #mainwindow is an OpusGui
        self.mainwindow = mainwindow
        self.gui_result_manager = gui_result_manager
        self.toolboxStuff = self.gui_result_manager.mainwindow.toolboxStuff

        self.cbAutoGen.setToolTip(QString(
            '''If checked, indicator results will automatically be
            created for the currently selected simulation run,
            indicator, and years. If unchecked, click
            Generate results in order to make results available.'''))

        self.inGui = False
        self.logFileKey = 0
        self.available_years_for_simulation_runs = {}
        
        self.current_year = None
        self.current_run = None
        self.current_indicator = None
        self.setup = True

        self.xml_helper = ResultsManagerXMLHelper(toolboxStuff = self.toolboxStuff)
        self.setupAvailableIndicators()
        self._setup_simulation_data()
        
        self.setup = False
        

        self.batch_processor = BatchProcessor(
                                    toolboxStuff = self.toolboxStuff)
            
        self.batch_processor.guiElement = self
        

    def setupAvailableIndicators(self):

        indicators = self.xml_helper.get_available_indicator_names(attributes = ['dataset'])

        self.tableWidget.clear()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(len(indicators))
        
        col = QTableWidgetItem()
        col.setText(QString('Name'))
        self.tableWidget.setHorizontalHeaderItem(0,col)
        
        col = QTableWidgetItem()
        col.setText(QString('Dataset'))
        self.tableWidget.setHorizontalHeaderItem(1,col)

        col = QTableWidgetItem()
        col.setText(QString('Definition'))
        self.tableWidget.setHorizontalHeaderItem(2,col)
                    
        for i,indicator in enumerate(indicators):
            row = QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(i,row)
            j = 0

            item = QTableWidgetItem()
            item.setText(indicator['name'])
            self.tableWidget.setItem(i,0,item)

            item = QTableWidgetItem()
            item.setText(indicator['dataset'])
            self.tableWidget.setItem(i,1,item)
        
            item = QTableWidgetItem()
            item.setText(indicator['value'])
            self.tableWidget.setItem(i,2,item)
            
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setCurrentCell(0,0)
        self.on_tableWidget_itemSelectionChanged()

    def _setup_simulation_data(self):
        
        runs = self.xml_helper.get_available_run_info(
                   attributes = ['start_year', 'end_year'])
        
        idx = -1
        for i, run in enumerate(runs):
            run_name = str(run['name'])
            if run_name == 'base_year_data':
                idx = i
            years = (run['start_year'], run['end_year'])
            self.available_years_for_simulation_runs[run_name] = years
            
            self.lstAvailableRuns.addItem(QString(run_name))
                        
        if idx != -1:
            self.lstAvailableRuns.setCurrentRow(idx)
            self.on_lstAvailableRuns_currentRowChanged(idx)
        
    def on_lstAvailableRuns_currentRowChanged(self, ind):
        print 'runs changed'
        current_run = str(self.lstAvailableRuns.currentItem().text())
        if current_run == self.current_run and not self.setup: 
            return
        
        self.current_run = current_run
        
        setup = self.setup
        if current_run in self.available_years_for_simulation_runs:
            self.lstYears.clear()
            (start, end) = self.available_years_for_simulation_runs[current_run]
            (start, end) = (int(start), int(end))
            self.setup = True
            for i in range(start, end + 1):
                yr = QString(repr(i))
                self.lstYears.addItem(yr)
                self.lstYears.setCurrentRow(0)
                self.on_lstYears_currentRowChanged(0)
            self.setup = False
            
        if not setup and self.cbAutoGen.isChecked():
            self.on_pbnGenerateResults_released()
            
            
    def on_lstYears_currentRowChanged(self, ind):
        print 'years changed'
        current_year = int(self.lstYears.currentItem().text())

        if self.current_year == current_year and not self.setup: return 
        self.current_year = current_year
        if not self.setup and self.cbAutoGen.isChecked(): 
            self.on_pbnGenerateResults_released()
        
    def on_tableWidget_itemSelectionChanged(self):
        print 'changed item se'
        indicator_name = str(self.tableWidget.item(self.tableWidget.currentRow(),0).text())
        if self.current_indicator == indicator_name and not self.setup: return
        
        self.current_indicator = indicator_name
        if not self.setup and self.cbAutoGen.isChecked(): 
            self.on_pbnGenerateResults_released()
        
        
    def on_pbnGenerateResults_released(self):

        run_name = self.current_run
        indicator_name = self.current_indicator
        
        start_year = self.current_year
        end_year = start_year
        
        if run_name is None or indicator_name is None or start_year is None: return
        
        self.pbnGenerateResults.setEnabled(False)
        
        print 'Generating results for %s on run %s for year %i'%(run_name, indicator_name, start_year)
        indicators = self.xml_helper.get_available_indicator_names(attributes = ['dataset'])
        dataset = None
        for i in indicators:
            if i['name'] ==QString(indicator_name):
                dataset = str(i['dataset'])
            
        if dataset is None:
            raise Exception('Could not find dataset for indicator %s'%indicator_name)
                
        table_params = {
            'name': None,
            'output_type' : 'tab',
            'indicators' : [indicator_name],
        }
        map_params = {'name':None,
                      'indicator':indicator_name}
        
        visualizations = [
            ('table_per_year', dataset, table_params),
            ('matplotlib_map', dataset, map_params)
        ]
                
        self.batch_processor.set_data(
            visualizations = visualizations, 
            source_data_name = run_name,
            years = range(start_year, end_year + 1))
                        
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
        for (visualization_type, visualizations) in self.batch_processor.get_visualizations():
            if visualization_type == 'matplotlib_map':
                viz = visualizations[0]
                map_widget = ViewImageForm(self.twVisualizations, viz)
                
            elif visualization_type == 'table_per_year':
                viz = visualizations[0]
                tab_widget = ViewTableForm(self.twVisualizations, viz)
                
        self.twVisualizations.removeTab(self.twVisualizations.indexOf(self.tabTable))
        self.twVisualizations.removeTab(self.twVisualizations.indexOf(self.tabMap))
        self.tabMap = None
        self.tabTable = None
                
        self.tabMap = map_widget
        self.tabTable = tab_widget
        
        self.twVisualizations.addTab(self.tabTable, "")
        self.twVisualizations.addTab(self.tabMap, "")
                
        self.twVisualizations.setTabText(self.twVisualizations.indexOf(self.tabTable), QString('Table'))
        self.twVisualizations.setTabText(self.twVisualizations.indexOf(self.tabMap), QString('Map'))
        #self.tabMap.show()
        #self.tabTable.show()
        self.twVisualizations.setCurrentIndex(0)        
        self.pbnGenerateResults.setEnabled(True)


    def runErrorFromThread(self,errorMessage):
        QMessageBox.warning(self.mainwindow, 'warning', errorMessage)
