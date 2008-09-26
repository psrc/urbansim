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

from PyQt4.QtCore import QFileInfo, SIGNAL, QObject, Qt, QVariant, QString, QTimer
from PyQt4.QtGui import QWidget, QIcon, QDialog, QMessageBox

from opus_core.services.run_server.run_manager import insert_auto_generated_cache_directory_if_needed
from opus_core.database_management.configurations.services_database_configuration import ServicesDatabaseConfiguration

from opus_gui.results_manager.xml_helper_methods import ResultsManagerXMLHelper
from opus_gui.results_manager.run.batch_processor import BatchProcessor

from opus_gui.scenarios_manager.run.opusrunmodel import RunModelThread

from opus_gui.results_manager.controllers.view_image_form import ViewImageForm
from opus_gui.results_manager.controllers.view_table_form import ViewTableForm
from opus_gui.scenarios_manager.views.ui_simulation_gui_element import Ui_SimulationGuiElement
from opus_gui.scenarios_manager.views.ui_overwrite_dialog import Ui_dlgOverwriteRun
from time import localtime, strftime

from opus_gui.results_manager.run.opus_gui_thread import OpusGuiThread

class OverwriteRunDialog(QDialog,Ui_dlgOverwriteRun):
    def __init__(self, parent):
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint

        QDialog.__init__(self, parent.mainwindow, flags)
        self.setupUi(self)
        
# This is an element in the Run Manager GUI that is the container for the model
# and the model thread.  If the start button is pressed then the GUI will create
# a thread to execute the given model.
class SimulationGuiElement(QWidget, Ui_SimulationGuiElement):
    def __init__(self, mainwindow, runManager, model):
        QWidget.__init__(self, mainwindow)

        self.mainwindow = mainwindow
        self.setupUi(self)

        self.runManager = runManager
        self.model = model
        self.model.guiElement = self
        self.inGui = False
        self.logFileKey = 0
        self.running = False
        self.paused = False
        self.timer = None
        self.runThread = None
        self.config = None
        
        self.xml_helper = ResultsManagerXMLHelper(mainwindow.toolboxStuff)
        self.toolboxStuff = self.mainwindow.toolboxStuff
        
        # Grab the path to the base XML used to run this model
        self.xml_path = model.xml_path

        # Bring up the XML file and grab the start year and end year
        fileNameInfo = QFileInfo(self.xml_path)
        fileNameAbsolute = fileNameInfo.absoluteFilePath().trimmed()
        config = self.toolboxStuff.opusXMLTree.get_run_configuration(str(self.model.modeltorun))
        self.config = config
        insert_auto_generated_cache_directory_if_needed(config)
        (self.start_year, self.end_year) = config['years']

        self.tabIcon = QIcon(":/Images/Images/cog.png")
        self.tabLabel = fileNameInfo.fileName()   

        self.setup_run_name_line_edit()
        self.setup_indicator_batch_combobox()

        # Simulation Progress Tab

        self.runProgressBarTotal.setProperty("value",QVariant(0))
        self.runProgressBarTotal.reset()

        ### Year Progress Bar
        self.runProgressBarYear.setProperty("value",QVariant(0))
        self.runProgressBarYear.reset()

        ### Model Progress Bar

        self.runProgressBarModel.setProperty("value",QVariant(0))
        self.runProgressBarModel.reset()

        self.setupDiagnosticIndicatorTab()
        self.runProgressBarModel.hide()
        self.runProgressBarModelLabel.hide()
        self.summaryCurrentPieceValue.hide()
        
    def updateConfigAndGuiForRun(self):
        config = self.toolboxStuff.opusXMLTree.get_run_configuration(str(self.model.modeltorun))
        self.config = config
        insert_auto_generated_cache_directory_if_needed(config)
        (self.start_year, self.end_year) = config['years']
        #self.summaryYearRangeLabel.setText(QString("Running model from "+str(self.start_year)+" to "+str(self.end_year)))

    def on_cbYear_stateChanged(self, state):
        if self.cbYear.isChecked():
            self.runProgressBarYear.show()
            self.runProgressBarYearLabel.show()
            self.summaryCurrentModelValue.show()
            self.cbModel.setChecked(False)
            self.cbModel.show()
#            self.runProgressBarModel.show()
#            self.runProgressBarModelLabel.show()
#            self.summaryCurrentPieceValue.show()
        else:
            self.runProgressBarYear.hide()
            self.cbModel.hide()
            self.runProgressBarYearLabel.hide()
            self.summaryCurrentModelValue.hide()

            self.runProgressBarModel.hide()
            self.runProgressBarModelLabel.hide()
            self.summaryCurrentPieceValue.hide()
        
    def on_cbModel_stateChanged(self, state):
        if self.cbModel.isChecked():
            self.runProgressBarModel.show()
            self.runProgressBarModelLabel.show()
            self.summaryCurrentPieceValue.show()
        else:
            self.runProgressBarModel.hide()
            self.runProgressBarModelLabel.hide()
            self.summaryCurrentPieceValue.hide()

    def setupDiagnosticIndicatorTab(self):

        config = self.toolboxStuff.opusXMLTree.get_run_configuration(str(self.model.modeltorun))

        years = range(config["years"][0],config["years"][1]+1)
        self.yearItems = []
        for year in years:
            #the second value in the list determines if it is already added to the drop down
            self.yearItems.append([year, False]); 

        datasets = self.xml_helper.get_available_datasets()        
        
        for dataset in datasets:
            self.diagnostic_dataset_name.addItem(QString(dataset))

        self.setup_diagnostic_indicators()
        self.indicatorResultsTab.removeTab(0)
        QObject.connect(self.diagnostic_go_button,SIGNAL("released()"),self.on_indicatorBox)
        QObject.connect(self.diagnostic_dataset_name, SIGNAL("currentIndexChanged(QString)"), self.on_diagnostic_dataset_name_currentIndexChanged)       
        
    def setup_diagnostic_indicators(self):
        indicators = self.xml_helper.get_available_indicator_names(attributes = ['dataset'])
        dataset = self.diagnostic_dataset_name.currentText()
        self.diagnostic_indicator_name.clear()
        for indicator in indicators:
            if indicator['dataset'] == dataset:
                self.diagnostic_indicator_name.addItem(indicator['name'])

    def on_diagnostic_dataset_name_currentIndexChanged(self, param):
        if isinstance(param, int):
            return #qt sends two signals for the same event; only process one
        self.setup_diagnostic_indicators()
        
    def setup_indicator_batch_combobox(self):        
        self.cboOptionalIndicatorBatch.addItem(QString('(None)'))
        batches = self.xml_helper.get_available_batches()
        for batch in batches:
            self.cboOptionalIndicatorBatch.addItem(QString(batch['name']))
        
    def setup_run_name_line_edit(self):
        run_name = 'run_%s'%strftime('%Y_%m_%d_%H_%M', localtime())
        self.leRunName.setText(QString(run_name))
            
    def on_indicatorBox(self):
        indicator_name = str(self.diagnostic_indicator_name.currentText())

        dataset_name = self.diagnostic_dataset_name.currentText()
        year = self.diagnostic_year.currentText()
        if year is None: return
        
        year = int(str(year))
        cache_directory = self.model.config['cache_directory']
        indicator_type = str(self.diagnostic_indicator_type.currentText())
        
        if indicator_type == 'table':
            indicator_type = 'tab'
        else:
            indicator_type = 'matplotlib_map'

        visualizations = [
            (indicator_type, str(dataset_name), {'indicators':[indicator_name]})
        ]

        self.batch_processor = BatchProcessor(
                                    toolboxStuff = self.toolboxStuff)
            
        self.batch_processor.guiElement = self
             
        self.batch_processor.set_data(
            visualizations = visualizations, 
            source_data_name = self.model.run_name,
            years = [year, year],
            cache_directory = cache_directory)

        self.diagnosticThread = OpusGuiThread(
                              parentThread = self.mainwindow,
                              parentGuiElement = self,
                              thread_object = self.batch_processor)
        
        # Use this signal from the thread if it is capable of producing its own status signal
        QObject.connect(self.diagnosticThread, SIGNAL("runFinished(PyQt_PyObject)"),
                        self.visualizationsCreated)
        QObject.connect(self.diagnosticThread, SIGNAL("runError(PyQt_PyObject)"),
                        self.runErrorFromThread)
        
        self.diagnosticThread.start()

    def visualizationsCreated(self):
        all_visualizations = self.batch_processor.get_visualizations()
        for indicator_type, visualizations in all_visualizations:            
            for visualization in visualizations:
                if indicator_type == 'matplotlib_map':
                    form = ViewImageForm(mainwindow = self.mainwindow,
                                         visualization = visualization)
                else:        
                    form = ViewTableForm(mainwindow = self.mainwindow,
                         visualization = visualization)
                self.indicatorResultsTab.insertTab(0,form,form.tabIcon,form.tabLabel)


    def on_pbnRemoveModel_released(self):
        #    if(self.running == True):
        success = True
        if self.runThread:
            success = self.runThread.cancel()

        if success:
            if self.timer:
                self.timer.stop()
            self.running = False
            self.paused = False
            self.runManager.removeModelElement(self)
            self.runManager.updateModelElements()

    def on_pbnStartModel_released(self):
        proceed = True
        duplicate = False
        
        run_name = str(self.leRunName.text())
        if run_name == '':
            run_name = None
        else:
            run_id = None
            for run in self.xml_helper.get_available_run_info(attributes = ['run_id']):
                existing_run_name = run['name']
                if run_name == existing_run_name:
                    duplicate = True
                    if 'run_id' in run: run_id = int(run['run_id'])
                    break
            if duplicate:
                dlg_dup = OverwriteRunDialog(self)
            
                if dlg_dup.exec_() == QDialog.Rejected:
                    proceed = False
                
        if not proceed: return
        
        
        if self.running and not self.paused:
            # Take care of pausing a run
            success = self.runThread.pause()
            if success: 
                self.paused = True
                self.timer.stop()
                self.pbnStartModel.setText(QString("Resume simulation run..."))
        elif self.running and self.paused:
            # Need to resume a paused run
            success = self.runThread.resume()
            if success: 
                self.paused = False
                self.timer.start(1000)
                self.pbnStartModel.setText(QString("Pause simulation run..."))
        elif not self.running:
            # Update the XML
            self.toolboxStuff.updateOpusXMLTree()
            self.updateConfigAndGuiForRun()

            # Fire up a new thread and run the model
            self.pbnStartModel.setText(QString("Pause simulation run..."))
            # References to the GUI elements for status for this run...
            self.progressBarTotal = self.runProgressBarTotal
            self.progressBarYear = self.runProgressBarYear
            self.progressBarModel = self.runProgressBarModel

            #self.pbnRemoveModel.setEnabled(False)
            #self.pbnStartModel.setEnabled(False)

            # Initializing values
            self.progressBarTotal.setValue(0)
            self.progressBarYear.setValue(0)
            self.progressBarModel.setValue(0)
            self.progressBarTotal.setRange(0,0)
            self.progressBarYear.setRange(0,0)
            self.progressBarModel.setRange(0,0)
            
            batch_name = str(self.cboOptionalIndicatorBatch.currentText())
            if batch_name == '(None)':
                batch_name = None            
            
            self.runThread = RunModelThread(self.mainwindow,
                                            self,
                                            self.xml_path,
                                            batch_name,
                                            run_name)
            
            if duplicate and run_id is not None:
                from opus_core.services.run_server.run_manager import RunManager as ServicesRunManager
                run_manager = ServicesRunManager(ServicesDatabaseConfiguration())
                run_manager.delete_everything_for_this_run(run_id = run_id)
                run_manager.close()
                
            
            # Use this signal from the thread if it is capable of producing its own status signal
            QObject.connect(self.runThread, SIGNAL("runFinished(PyQt_PyObject)"),
                            self.runFinishedFromThread)
            QObject.connect(self.runThread, SIGNAL("runError(PyQt_PyObject)"),
                            self.runErrorFromThread)
            # Use this timer to call a function in the thread to check status if the thread is unable
            # to produce its own signal above
            self.timer = QTimer()
            QObject.connect(self.timer, SIGNAL("timeout()"),
                            self.runStatusFromThread)
            self.timer.start(1000)
            self.running = True
            self.paused = False
            self.runThread.start()
        else:
            print "Unexpected state in the model run..."


    # This is not used currently since the model can not return status... instead we use a timer to
    # check the status from a log file.
    def runPingFromThread(self,value):
        self.progressBar.setValue(value)
        #print "Ping from thread!"

    # Called when the model is finished... peg the percentage to 100% and stop the timer.
    def runFinishedFromThread(self,success):
        print "Simulation run finished with success = ", success
        self.progressBarTotal.setValue(100)
        self.progressBarYear.setValue(100)
        self.progressBarModel.setValue(100)
        
        if success: msg = 'Simulation ran successfully!'
        else: msg = 'Simulation failed.'
        self.summaryCurrentYearValue.setText(QString(msg))
        self.summaryCurrentModelValue.setText(QString("Finished"))
        self.summaryCurrentPieceValue.setText(QString("Finished"))
        
        self.timer.stop()
        # Get the final logfile update after model finishes...
        self.logFileKey = self.runThread.modelguielement.model._get_current_log(self.logFileKey)
        
        self.running = False
        self.paused = False
        self.pbnStartModel.setText(QString("Start Simulation Run..."))

        #get the last year to show up in the diagnostics tab.
        self.yearItems[-1][1] = True
        self.diagnostic_year.addItem(QString(str(self.yearItems[-1][0])))

        if self.runThread.batch_name is not None:
            all_visualizations = self.runThread.batch_processor.get_visualizations()
            for indicator_type, visualizations in all_visualizations:
                form_generator = None
                if indicator_type == 'matplotlib_map' or \
                   indicator_type == 'matplotlib_chart':
                    form_generator = self.mainwindow.resultManagerStuff.addViewImageIndicator
                elif indicator_type == 'table_per_year' or \
                     indicator_type == 'table_per_attribute':    
                    form_generator = self.mainwindow.resultManagerStuff.addViewTableIndicator            
            
                if form_generator is not None:    
                    for visualization in visualizations:
                        form_generator(visualization = visualization, indicator_type = indicator_type)    


        
    # GUI elements that show progress go here.  Note that they have to be set
    # up first in the constructor of this class, then optionally initialized in
    # on_pbnStartModel_released(), then calculated and updated here, and finally
    # when the simulation is done running, finalized values are optionally
    # defined in runFinishedFromThread (because status.txt doesn't refresh at
    # end of the simulation.
    def runStatusFromThread(self):
        totalProgress = 0
        yearProgress = 0
        modelProgress = 0
        boxTitle = "Simulation run initializing..." # TODO:  this is for the old prog bar

        if self.runThread.modelguielement.model.statusfile is None:
            boxTitle = "Simulation run initializing..."
        else:
            # Compute percent progress for the progress bar.
            # The statusfile is written by the _write_status_for_gui method
            # in class ModelSystem in urbansim.model_coordinators.model_system
            # The file is ascii, with the following format (1 item per line):
            #   current year
            #   total number of models
            #   number of current model that is about to run (starting with 0)
            #   name of current model
            #   total number of pieces of current model (could be 1)
            #   number of current piece
            #   description of current piece (empty string if no description)
            statusfile = self.runThread.modelguielement.model.statusfile
            try:

                f = open(statusfile)
                lines = f.readlines()
                f.close()

                # use float for all numbers to help with percent computation
                if len(lines) > 0:
                    current_year = float(lines[0])
                    total_models = float(lines[1])
                    current_model = float(lines[2])
                    current_model_names = lines[3]
                    current_model_display_name = current_model_names#current_model_names[0]
                    total_pieces = float(lines[4])
                    current_piece = float(lines[5])
                    current_piece_name = lines[6].strip()
                    total_years = float(self.end_year - self.start_year + 1)
                    # For each year, we need to run all of the models.
                    # year_fraction_completed is the fraction completed (ignoring the currently running year)
                    # model_fraction_completed is the additional fraction completed for the current year
    
                    modelProgress = 100.0 * (current_piece / total_pieces)
                    yearProgress = modelProgress / total_models + 100.0 * (current_model / total_models)
                    totalProgress = yearProgress / total_years + 100.0 * ((current_year - self.start_year) / total_years)
    
                    currentYearString = "("+str(int((current_year - self.start_year))+1)+"/"+str(int(total_years))+") "+str(int(current_year))
                    self.summaryCurrentYearValue.setText(QString(currentYearString))
    
                    currentModelString = "("+str(int(current_model)+1)+"/"+str(int(total_models))+") "+current_model_display_name
                    self.summaryCurrentModelValue.setText(QString(currentModelString))
    
                    currentPieceString = "("+str(int(current_piece)+1)+"/"+str(int(total_pieces))+") "+current_piece_name
                    self.summaryCurrentPieceValue.setText(QString(currentPieceString))
    
                    boxTitle = current_model_display_name
                    
                    #detect if a year has been completed
                    for item in self.yearItems:
                        if (int(item[0]) < int(current_year) and not item[1]) :
                            self.diagnostic_year.addItem(QString(str(item[0])))
                            item[1] = True 
                            #hook into indicator group computation here
    
                    if (self.progressBarTotal.maximum() == 0):
                        self.progressBarTotal.setRange(0,100)
                        self.progressBarYear.setRange(0,100)
                        self.progressBarModel.setRange(0,100)

            except IOError:
                boxTitle = "Simulation run is initializing..."

        newString = QString(boxTitle)

        newString.leftJustified(60)
#        self.simprogressGroupBox.setTitle(newString)
        self.progressBarTotal.setValue(totalProgress)
        self.progressBarYear.setValue(yearProgress)
        self.progressBarModel.setValue(modelProgress)


        self.logFileKey = self.runThread.modelguielement.model._get_current_log(self.logFileKey)

    def runErrorFromThread(self,errorMessage):
        self.running = False
        self.paused = False
        self.pbnStartModel.setText(QString("Start Simulation Run..."))
        QMessageBox.warning(self.mainwindow,'Warning', errorMessage)
