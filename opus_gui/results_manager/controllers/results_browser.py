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
from PyQt4.QtGui import QMessageBox, QTabWidget, QWidget, \
                        QTableWidgetItem, QSizePolicy

from opus_gui.results_manager.xml_helper_methods import ResultsManagerXMLHelper

from opus_gui.results_manager.run.opus_gui_thread import OpusGuiThread
from opus_gui.results_manager.run.batch_processor import BatchProcessor

from opus_gui.results_manager.views.results_browser_ui import Ui_ResultsBrowser
from opus_gui.results_manager.controllers.view_image_form import ViewImageForm
from opus_gui.results_manager.controllers.view_table_form import ViewTableForm
from opus_core.logger import logger


class ResultBrowser(QWidget, Ui_ResultsBrowser):
    def __init__(self, mainwindow, gui_result_manager):
        QWidget.__init__(self, mainwindow)
        self.setupUi(self)
        #self.setFocusPolicy()
        
        #mainwindow is an OpusGui
        self.mainwindow = mainwindow
        self.gui_result_manager = gui_result_manager
        self.toolboxBase = self.gui_result_manager.mainwindow.toolboxBase
        QObject.connect(self.toolboxBase.generalManagerTree.model, SIGNAL("layoutChanged()"),
                self.setupAvailableIndicators)

        QObject.connect(self.toolboxBase.resultsManagerTree.model, SIGNAL("layoutChanged()"),
                self._setup_simulation_data)

                    
        self.cbAutoGen.setToolTip(QString(
            ('If checked, indicator results will automatically be\n'
            'created for the currently selected simulation run,\n'
            'indicator, and years. If unchecked, click\n'
            'Generate results in order to make results available.')
            ))

        self.inGui = False
        self.logFileKey = 0
        self.available_years_for_simulation_runs = {}
        
        self.current_indicator = None
        self.current_run = None
        self.current_year = None
        
        self.running_key = None
        self.queued_results = None
        
        self.setup = True

        self.xml_helper = ResultsManagerXMLHelper(toolboxBase = self.toolboxBase)
        self.setupAvailableIndicators()
        self._setup_simulation_data()
        
        self.setup = False
        
        self.already_browsed = {}
        
        self.generating_results = False
        if self.cbAutoGen.isChecked():
            self.on_pbnGenerateResults_released()
        self.pbnExportResults.setEnabled(False)
        self.twVisualizations.removeTab(0)
        
    def setupAvailableIndicators(self):
        print 'setting up available indicators!'

        indicators = self.xml_helper.get_available_indicator_names(attributes = ['dataset'])

        current_row = self.tableWidget.currentRow()
        
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
            
        if current_row is None or current_row == -1:
            current_row = 0
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.resizeColumnsToContents()
        
        self.tableWidget.setCurrentCell(current_row,0)
        self.on_tableWidget_itemSelectionChanged()

    def _setup_simulation_data(self):
        current_row = self.lstAvailableRuns.currentRow()
        
        runs = self.xml_helper.get_available_run_info(
                   attributes = ['years'])
        
        self.lstAvailableRuns.clear()
        idx = -1
        for i, run in enumerate(runs):
            run_name = str(run['name'])
            if run_name == 'base_year_data':
                idx = i
            
            years = run['years']
            self.available_years_for_simulation_runs[run_name] = years
            
            self.lstAvailableRuns.addItem(QString(run_name))
                        
        if current_row is None or current_row == -1:
            current_row = idx
        if current_row != -1:
            self.lstAvailableRuns.setCurrentRow(current_row)
            self.on_lstAvailableRuns_currentRowChanged(current_row)
        
    def on_lstAvailableRuns_currentRowChanged(self, ind):
        currentItem = self.lstAvailableRuns.currentItem()
        if currentItem is None: return
        
        current_run = str(currentItem.text())
        if current_run == self.current_run and not self.setup: return
        
        self.current_run = current_run
        
        setup = self.setup
        if current_run in self.available_years_for_simulation_runs:
            self.setup = True
            self.lstYears.clear()
            
            years = self.available_years_for_simulation_runs[current_run]
            for yr in sorted(years):
                self.lstYears.addItem(QString(str(yr)))
                
            self.lstYears.setCurrentRow(0)
            self.on_lstYears_currentRowChanged(0)
            self.setup = False

        if not setup and self.cbAutoGen.isChecked():
            self.on_pbnGenerateResults_released()
        else:
            self.pbnGenerateResults.setEnabled(True)
            self.pbnGenerateResults.setText(QString('Generate Results'))
            
            
    def on_lstYears_currentRowChanged(self, ind):
        currentItem = self.lstYears.currentItem()
        if currentItem is None: return
        
        current_year = int(currentItem.text())

        if self.current_year == current_year and not self.setup: return 
        self.current_year = current_year

        if not self.setup and self.cbAutoGen.isChecked(): 
            self.on_pbnGenerateResults_released()
        else:
            self.pbnGenerateResults.setEnabled(True)
            self.pbnGenerateResults.setText(QString('Generate Results'))
        
    def on_tableWidget_itemSelectionChanged(self):
        currentRow = self.tableWidget.currentRow()
        if currentRow is None: return
        
        indicator_name = str(self.tableWidget.item(currentRow,0).text())
        if self.current_indicator == indicator_name and not self.setup: return
        
        self.current_indicator = indicator_name

        if not self.setup and self.cbAutoGen.isChecked(): 
            self.on_pbnGenerateResults_released()
        else:
            self.pbnGenerateResults.setEnabled(True)
            self.pbnGenerateResults.setText(QString('Generate Results'))

        
        
    def on_pbnGenerateResults_released(self):

        run_name = self.current_run
        indicator_name = self.current_indicator
        
        start_year = self.current_year
        end_year = start_year
        
        if run_name is None or indicator_name is None or start_year is None: return
        
        key = (run_name, indicator_name, start_year)

        if key in self.already_browsed:
            if not self.generating_results:
                (tab_widget,map_widget) = self.already_browsed[key]
#                self.swap_visualizations(map_widget, tab_widget)
                self.pbnGenerateResults.setText(QString('Results Generated'))
            else:
                self.queued_results = ('swap', (map_widget, tab_widget))
                
            return
        
        self.pbnGenerateResults.setEnabled(False)
        self.pbnGenerateResults.setText(QString('Generating Results...'))      

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
                      'indicators':[indicator_name]}
        
        visualizations = [
            ('table_per_year', dataset, table_params),
            ('matplotlib_map', dataset, map_params)
        ]
                
        batch_processor = BatchProcessor(
                            toolboxBase = self.toolboxBase)
        batch_processor.guiElement = self
        
        
        batch_processor.set_data(
            visualizations = visualizations, 
            source_data_name = run_name,
            years = range(start_year, end_year + 1))
        
        if not self.generating_results:
            self.generating_results = True
            logger.log_note('Generating results for %s on run %s for year %i'%(run_name, indicator_name, start_year))
            self.running_key = key
            self.batch_processor = batch_processor
            runThread = OpusGuiThread(
                                  parentThread = self.mainwindow,
                                  parentGuiElement = self,
                                  thread_object = self.batch_processor)
            
            # Use this signal from the thread if it is capable of producing its own status signal
            QObject.connect(runThread, SIGNAL("runFinished(PyQt_PyObject)"),
                            self.runFinishedFromThread)
            QObject.connect(runThread, SIGNAL("runError(PyQt_PyObject)"),
                            self.runErrorFromThread)
            
            runThread.start()
        else:
            self.queued_results = (key, batch_processor)
            


    # Called when the model is finished... 
    def runFinishedFromThread(self,success):             
        key = self.running_key
        self.running_key = None
                   
        size = QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.twVisualizations.setSizePolicy(size)

        name = '%s/%s/%s'%key
        new_tab = QTabWidget(self.twVisualizations)
        self.twVisualizations.addTab(new_tab, QString(name))

        map_widget = None
        tab_widget = None
        for (visualization_type, visualizations) in self.batch_processor.get_visualizations():
            if len(visualizations) > 0:
                if visualization_type == 'matplotlib_map':
                    viz = visualizations[0]
                    map_widget = ViewImageForm(new_tab, viz)
                    map_widget.setSizePolicy(size)
                elif visualization_type == 'table_per_year':
                    viz = visualizations[0]
                    tab_widget = ViewTableForm(new_tab, viz)
                    tab_widget.setSizePolicy(size)
#            else:
#                map_widget = self.tabMap
#                tab_widget = self.tabTable
            
        if not map_widget or not tab_widget: return
        
        self.tabMap = map_widget
        self.tabTable = tab_widget
        
        new_tab.addTab(self.tabTable, "Table")
        new_tab.addTab(self.tabMap, "Map")
        
        
        self.already_browsed[key] = (tab_widget, map_widget)  
        
#        self.lblViewIndicator.setText(QString(key[1]))
#        self.lblViewRun.setText(QString(key[0]))
#        self.lblViewYear.setText(QString(repr(key[2])))
          
        swap = self.queued_results is not None and self.queued_results[0] == 'swap'
        
        if self.queued_results is not None and not swap:
            self.running_key = self.queued_results[0]

            logger.log_note('Generating queued results for %s on run %s for year %i'%self.running_key)
            self.batch_processor = self.queued_results[1]
            self.queued_results = None
            
            runThread = OpusGuiThread(
                                  parentThread = self.mainwindow,
                                  parentGuiElement = self,
                                  thread_object = self.batch_processor)
            
            # Use this signal from the thread if it is capable of producing its own status signal
            QObject.connect(runThread, SIGNAL("runFinished(PyQt_PyObject)"),
                            self.runFinishedFromThread)
            QObject.connect(runThread, SIGNAL("runError(PyQt_PyObject)"),
                            self.runErrorFromThread)
            runThread.start()
        else:
            if swap:
                (map_widget, tab_widget) = self.queued_results[1]
                
#                self.swap_visualizations(map_widget, tab_widget)
                name = '%s/%s/%s'%key
        #        self.swap_visualizations(map_widget, tab_widget)
                self.add_visualization(map_widget = map_widget, tab_widget = tab_widget, name = name)
                    
            self.queued_results = None
                
            self.generating_results = False
            self.pbnGenerateResults.setText(QString('Results Generated'))
            
    def swap_visualizations(self, map_widget, tab_widget):
        cur_index = self.twVisualizations.currentIndex()
        
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
        
        self.twVisualizations.setCurrentIndex(cur_index)
    
    def runErrorFromThread(self,errorMessage):
        QMessageBox.warning(self.mainwindow, 'warning', errorMessage)
