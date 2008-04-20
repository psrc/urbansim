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

#
# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import *

from opus_gui.run.model.opusrunmodel import *
from opus_gui.run.estimation.opusrunestimation import *
from opus_gui.config.xmlmodelview.opusdataview import OpusDataView
from opus_gui.config.xmlmodelview.opusdatamodel import OpusDataModel
from opus_gui.config.xmlmodelview.opusdatadelegate import OpusDataDelegate
from opus_gui.results.forms.view_image_form import ViewImageForm
from opus_gui.results.forms.view_table_form import ViewTableForm

# General system includes
import os, sys, time, tempfile, shutil, string

from opus_gui.results.xml_helper_methods import elementsByAttributeValue
from opus_gui.results.opus_result_generator import OpusGuiThread, OpusResultGenerator, OpusResultVisualizer  

# Main Run manager class
class RunManagerBase(object):
    def __init__(self, parent):
        self.parent = parent
        self.tabWidget = parent.tabWidget
        self.gui = parent
        # Build a list of the current models... starting empty
        self.modelList = []
        self.modelElements = []
        self.estimationList = []
        self.estimationElements = []

    def addModelElement(self,model):
        self.modelElements.insert(0,ModelGuiElement(self.parent,self,model))

    def removeModelElement(self,modelElement):
        #self.groupBoxLayout.removeWidget(modelElement)
        self.tabWidget.removeTab(self.tabWidget.indexOf(modelElement))
        self.modelElements.remove(modelElement)
        modelElement.hide()

    def updateModelElements(self):
        for modelElement in self.modelElements:
            if modelElement.inGui == False:
                #self.groupBoxLayout.insertWidget(0,modelElement)
                #self.tabWidget.addTab(modelElement,str(modelElement.originalFile.absoluteFilePath()))
                self.tabWidget.insertTab(0,modelElement,modelElement.tabIcon,modelElement.tabLabel)
                self.tabWidget.setCurrentIndex(0)
                modelElement.inGui = True

    def addEstimationElement(self,estimation):
        self.estimationElements.insert(0,EstimationGuiElement(self.parent,self,estimation))

    def removeEstimationElement(self,estimationElement):
        self.tabWidget.removeTab(self.tabWidget.indexOf(estimationElement))
        self.estimationElements.remove(estimationElement)
        estimationElement.hide()

    def updateEstimationElements(self):
        for estimationElement in self.estimationElements:
            if estimationElement.inGui == False:
                self.tabWidget.insertTab(0,estimationElement,estimationElement.tabIcon,estimationElement.tabLabel)
                self.tabWidget.setCurrentIndex(0)
                estimationElement.inGui = True

    def setGui(self, gui):
        self.gui = gui

    def getModelList(self):
        return self.modelList

    def addNewModelRun(self, modelToRun):
        self.modelList.append(modelToRun)
        self.addModelElement(modelToRun)
        self.updateModelElements()
        #self.emit(SIGNAL("newModelAddedToManager()"))

    def removeModelRun(self, modelToRemove):
        self.modelList.remove(modelToRemove)

    def addNewEstimationRun(self, estimationToRun):
        self.estimationList.append(estimationToRun)
        self.addEstimationElement(estimationToRun)
        self.updateEstimationElements()

    def removeEstimationRun(self, estimationToRemove):
        self.estimationList.remove(estimationToRemove)

# This is an element in the Run Manager GUI that is the container for the model
# and the model thread.  If the start button is pressed then the GUI will create
# a thread to execute the given model.
class ModelGuiElement(QWidget):
    def __init__(self, parent, runManager, model):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.runManager = runManager
        self.model = model
        self.model.guiElement = self
        self.inGui = False
        self.logFileKey = 0
        self.running = False
        self.paused = False
        self.timer = None
        self.runThread = None
        
        # Grab the path to the base XML used to run this model
        self.xml_path = model.xml_path

        # Bring up the XML file and grab the start year and end year
        fileNameInfo = QFileInfo(self.xml_path)
        fileNameAbsolute = fileNameInfo.absoluteFilePath().trimmed()
        config = XMLConfiguration(str(fileNameAbsolute)).get_run_configuration(str(self.model.modeltorun))
        insert_auto_generated_cache_directory_if_needed(config)
        (self.start_year, self.end_year) = config['years']

        self.tabIcon = QIcon(":/Images/Images/cog.png")
        self.tabLabel = fileNameInfo.fileName()

        # LAYOUT FOR THE MODEL ELEMENT IN THE GUI
        self.widgetLayout = QVBoxLayout(self)
        self.widgetLayout.setAlignment(Qt.AlignTop)
        self.groupBox = QGroupBox(self)
        self.groupBox.setTitle(QString("main_groupBox"))
        self.widgetLayout.addWidget(self.groupBox)

        stringToUse = "Time Queued - %s" % (time.asctime(time.localtime()))
        self.groupBox.setTitle(QString(stringToUse))

        self.vboxlayout = QVBoxLayout(self.groupBox)
        self.vboxlayout.setObjectName("vboxlayout")

        self.modelControlWidget = QWidget(self.groupBox)
        self.vboxlayout.addWidget(self.modelControlWidget)

        self.vboxlayout2 = QVBoxLayout(self.modelControlWidget)
        self.vboxlayout2.setObjectName("vboxlayout2")

        ### Code for the buttons that start the simulation and remove from queue

        self.startWidget = QWidget(self.groupBox)
        self.startWidget.setObjectName("startWidget")

        self.startVBoxLayout = QGridLayout(self.startWidget)
        self.startVBoxLayout.setObjectName("startGridLayout")

        self.pbnStartModel = QPushButton(self.startWidget)
        self.pbnStartModel.setObjectName("pbnStartModel")
        self.pbnStartModel.setText(QString("Start Model..."))
        QObject.connect(self.pbnStartModel, SIGNAL("released()"),
                        self.on_pbnStartModel_released)        
        #self.startVBoxLayout.addWidget(self.pbnStartModel,0,0,1,1)
        self.startVBoxLayout.addWidget(self.pbnStartModel)
        self.pbnRemoveModel = QPushButton(self.startWidget)
        self.pbnRemoveModel.setObjectName("pbnRemoveModel")
        self.pbnRemoveModel.setText(QString("Remove From Queue"))
        QObject.connect(self.pbnRemoveModel, SIGNAL("released()"),
                        self.on_pbnRemoveModel_released)        
        self.startVBoxLayout.addWidget(self.pbnRemoveModel)
        self.vboxlayout2.addWidget(self.startWidget)

        # Add a tab widget and layer in a tree view and log panel
        self.tabWidget = QTabWidget(self.groupBox)

        # Simulation Progress Tab

        # Overall widget in the large group box
        self.simprogressWidget = QWidget(self.groupBox)
        self.simprogressWidget.setObjectName("simprogressWidget")
        self.simprogressLayout = QVBoxLayout(self.simprogressWidget)
        self.simprogressGroupBox = QGroupBox(self.simprogressWidget)
        self.simprogressGroupBox.setObjectName("simprogressGroupBox")
        self.simprogressGroupBox.setTitle("Progress Display")

        ### Progress display stuff goes in here
        self.simprogressLayoutInner = QGridLayout(self.simprogressGroupBox)    

        ### Year Range Label

        self.summaryYearRangeLabel = QLabel()
        self.summaryYearRangeLabel.setAlignment(Qt.AlignLeft)
        self.summaryYearRangeLabel.setObjectName("summaryYearRange")
        self.summaryYearRangeLabel.setText(QString("Running model from "+str(self.start_year)+" to "+str(self.end_year)))
        self.summaryYearRangeLabel.setMinimumWidth(300)
        self.simprogressLayoutInner.addWidget(self.summaryYearRangeLabel,0,0)

        # Begin Progress Simulation Display Bars

        # Layouts needs to be wrapped in a QWidget in order to be added to
        # a QVBoxLayout
        self.progressBarWidget = QWidget(self.groupBox)
        self.progressBarWidget.setObjectName("progressBarWidget")

        ### Total Progress Bar

        self.totalProgressBarLayout = QGridLayout()

        self.runProgressBarTotal = QProgressBar(self.progressBarWidget)
        self.runProgressBarTotal.setProperty("value",QVariant(0))
        self.runProgressBarTotal.setObjectName("runProgressBarTotal")
        self.runProgressBarTotal.setMinimumWidth(300)
        self.runProgressBarTotal.reset()

        self.runProgressBarTotalLabel = QLabel(self.runProgressBarTotal)
        self.runProgressBarTotalLabel.setAlignment(Qt.AlignRight)
        self.runProgressBarTotalLabel.setObjectName("runProgressBarTotalLabel")
        self.runProgressBarTotalLabel.setText(QString("Total Progress"))

        ### Current Year

        self.summaryCurrentYearValue = QLabel()
        self.summaryCurrentYearValue.setAlignment(Qt.AlignLeft)
        self.summaryCurrentYearValue.setObjectName("summaryCurrentYearValue")
        self.summaryCurrentYearValue.setText(QString("-"))
        self.summaryCurrentYearValue.setMinimumWidth(300)

        self.summaryCurrentYearLabel = QLabel(self.summaryCurrentYearValue)
        self.summaryCurrentYearLabel.setAlignment(Qt.AlignRight)
        self.summaryCurrentYearLabel.setObjectName("summaryCurrentYearLabel")
        self.summaryCurrentYearLabel.setText(QString("Current Year:"))

        ### Year Progress Bar
        self.yearProgressBarLayout = QGridLayout()

        self.runProgressBarYear = QProgressBar(self.progressBarWidget)
        self.runProgressBarYear.setProperty("value",QVariant(0))
        self.runProgressBarYear.setObjectName("runProgressBarYear")
        self.runProgressBarYear.setMinimumWidth(300)
        self.runProgressBarYear.reset()

        self.runProgressBarYearLabel = QLabel(self.runProgressBarYear)
        self.runProgressBarYearLabel.setAlignment(Qt.AlignRight)
        self.runProgressBarYearLabel.setObjectName("runProgressBarYearLabel")
        self.runProgressBarYearLabel.setText(QString("Year Progress"))

        ### Current Model

        self.summaryCurrentModelValue = QLabel()
        self.summaryCurrentModelValue.setAlignment(Qt.AlignLeft)
        self.summaryCurrentModelValue.setObjectName("summaryCurrentModelValue")
        self.summaryCurrentModelValue.setText(QString("-"))
        self.summaryCurrentModelValue.setMinimumWidth(300)

        self.summaryCurrentModelLabel = QLabel(self.summaryCurrentModelValue)
        self.summaryCurrentModelLabel.setAlignment(Qt.AlignRight)
        self.summaryCurrentModelLabel.setObjectName("summaryCurrentModelLabel")
        self.summaryCurrentModelLabel.setText(QString("Current Model:"))

        ### Model Progress Bar

        self.modelProgressBarLayout = QGridLayout()

        self.runProgressBarModel = QProgressBar(self.progressBarWidget)
        self.runProgressBarModel.setProperty("value",QVariant(0))
        self.runProgressBarModel.setObjectName("runProgressBarModel")
        self.runProgressBarModel.setMinimumWidth(300)
        self.runProgressBarModel.reset()

        self.runProgressBarModelLabel = QLabel(self.runProgressBarModel)
        self.runProgressBarModelLabel.setAlignment(Qt.AlignRight)
        self.runProgressBarModelLabel.setObjectName("runProgressBarModelLabel")
        self.runProgressBarModelLabel.setText(QString("Model Progress"))

        ### Current Piece

        self.summaryCurrentPieceValue = QLabel()
        self.summaryCurrentPieceValue.setAlignment(Qt.AlignLeft)
        self.summaryCurrentPieceValue.setObjectName("summaryCurrentPieceValue")
        self.summaryCurrentPieceValue.setText(QString("-"))
        self.summaryCurrentPieceValue.setMinimumWidth(300)

        self.summaryCurrentPieceLabel = QLabel(self.summaryCurrentPieceValue)
        self.summaryCurrentPieceLabel.setAlignment(Qt.AlignRight)
        self.summaryCurrentPieceLabel.setObjectName("summaryCurrentPieceLabel")
        self.summaryCurrentPieceLabel.setText(QString("Current Piece:"))

        # Forming the layout with the total progress and the year label
        self.totalProgressBarLayout.addWidget(self.runProgressBarTotalLabel,0,0)
        self.totalProgressBarLayout.addWidget(self.runProgressBarTotal,0,1)    
        self.totalProgressBarLayout.addWidget(self.summaryCurrentYearLabel,1,0)
        self.totalProgressBarLayout.addWidget(self.summaryCurrentYearValue,1,1) 

        # Forming the layout with the year progress and the model label
        self.yearProgressBarLayout.addWidget(self.runProgressBarYearLabel,0,0)
        self.yearProgressBarLayout.addWidget(self.runProgressBarYear,0,1)    
        self.yearProgressBarLayout.addWidget(self.summaryCurrentModelLabel,1,0)
        self.yearProgressBarLayout.addWidget(self.summaryCurrentModelValue,1,1) 

        # Forming the layout with model progress and the piece label
        self.modelProgressBarLayout.addWidget(self.runProgressBarModelLabel,0,0)
        self.modelProgressBarLayout.addWidget(self.runProgressBarModel,0,1)
        self.modelProgressBarLayout.addWidget(self.summaryCurrentPieceLabel,1,0)
        self.modelProgressBarLayout.addWidget(self.summaryCurrentPieceValue,1,1)

        self.progressBarLayout = QGridLayout(self.progressBarWidget)

        self.yearLayout = QHBoxLayout()
        self.yearLayout.addSpacing(20)
        self.yearLayout.addLayout(self.yearProgressBarLayout)
        self.modelLayout = QHBoxLayout()
        self.modelLayout.addSpacing(40)
        self.modelLayout.addLayout(self.modelProgressBarLayout)
        self.progressBarLayout.addLayout(self.totalProgressBarLayout,0,0)
        self.progressBarLayout.addLayout(self.yearLayout,1,0)
        self.progressBarLayout.addLayout(self.modelLayout,2,0)    

        # Place progress bars
        self.simprogressLayoutInner.addWidget(self.progressBarWidget,1,0)
        self.simprogressLayoutInner.setRowStretch(0,0) # row, weight
        self.simprogressLayoutInner.setRowStretch(1,1)  


        ###

        self.simprogressLayout.addWidget(self.simprogressGroupBox)
        self.tabWidget.addTab(self.simprogressWidget,"Simulation Progress")

        # End Progress Simulation Display

        self.configFile = QFile(self.xml_path)
        if self.configFile.open(QIODevice.ReadOnly):
            self.doc = QDomDocument()
            self.doc.setContent(self.configFile)
            self.dataModel = OpusDataModel(self, self.doc, self.parent, self.configFile,
                                           "scenario_manager", False)
            self.view = OpusDataView(self.parent)
            self.delegate = OpusDataDelegate(self.view)
            self.view.setItemDelegate(self.delegate)
            self.view.setModel(self.dataModel)
            self.view.expandAll()
            self.view.setAnimated(True)
            self.view.setColumnWidth(0,200)
            self.view.setColumnWidth(1,50)
            self.view.setMinimumHeight(200)
            self.tabWidget.addTab(self.view,"Tree View")

        # Log panel
        self.logText = QTextEdit(self.groupBox)
        self.logText.setReadOnly(True)
        self.logText.setLineWidth(0)
        self.tabWidget.addTab(self.logText,"Log")

        # Finally add the tab to the model page
        self.vboxlayout.addWidget(self.tabWidget)

        # start indicator tab 

        self.toolboxStuff = self.parent.toolboxStuff
        self.domDocument = self.toolboxStuff.doc


        # initialize indicator selection combobox
        #
        #    self.co_indicator_name = QComboBox()
        #    self.co_indicator_name.setObjectName("co_indicator_name")
        #    self.co_indicator_name.addItem(QString("[select]"))
        #        
        #    node_list = elementsByAttributeValue(domDocument = self.domDocument, 
        #                                              attribute = 'type', 
        #                                              value = 'indicator')
        #            
        #    for element, node in node_list:
        #        self.co_indicator_name.addItem(QString(element.nodeName()))
        #
        # end indicator combo box
        #
        # initialize source combobox
        #
        #    self.co_source_data = QComboBox()
        #    self.co_source_data.setObjectName("co_source_data")
        #    self.co_source_data.addItem(QString("[select]"))
        #        
        #    node_list = elementsByAttributeValue(domDocument = self.domDocument, 
        #                                              attribute = 'type', 
        #                                              value = 'source_data')
        #        
        #    for element, node in node_list:
        #        self.co_source_data.addItem(QString(element.nodeName()))
        #        vals = get_child_values(parent = node, 
        #                                    child_names = ['start_year', 'end_year'])
        #            
        #        self.available_years_for_simulation_runs[element.nodeName()] = (vals['start_year'],
        #                                                                         vals['end_year'])

        # end source combobox
        self.result_generator = OpusResultGenerator(
                                        xml_path = self.toolboxStuff.xml_file,
                                        domDocument = self.domDocument)  

        self.result_generator.guiElement = self



        self.indicatorWidget = QWidget() 
        #    self.indicatorVBoxLayout = QVBoxLayout(self.indicatorWidget)  
        self.indicatorGridBoxLayout = QGridLayout(self.indicatorWidget)
        #    self.indicatorWidget.addLayout(self.indicatorVBoxLayout)

        self.indicatorComboBox = QComboBox()
        #self.tabWidget.addTab(self.indicatorWidget,"Diagnostics")

        config = XMLConfiguration(str(self.xml_path)).get_run_configuration(str(self.model.modeltorun))
        #    QComboBox.addItem(self.indicatorComboBox, QString("<Select Year>"), QVariant())
        years = range(config["years"][0],config["years"][1]+1)
        self.yearItems = []
        for year in years:
            #        self.string = QString(year)
            #        QComboBox.addItem(self.indicatorComboBox, QString(str(year)), QVariant(year))
            self.yearItems.append([year, False]); 
            #the second value in the list determines if it is already added to the drop down

        #combo box for selecting indicators for diagnostic
        self.diagnostic_indicator_name = QComboBox()
        self.diagnostic_indicator_name.setObjectName("diagnostic_indicator_name")
        self.diagnostic_indicator_name.addItem(QString("[select indicator]"))

        node_list = elementsByAttributeValue(domDocument = self.domDocument, 
                                             attribute = 'type', 
                                             value = 'indicator')

        for element, node in node_list:
            self.diagnostic_indicator_name.addItem(QString(element.nodeName()))

        #combo box for selecting the dataset
        available_datasets = [
                '[select dataset]', 
                'gridcell', 
                'zone', 
                #'taz',
                #'county',
                #'alldata'
            ]
        self.diagnostic_dataset_name = QComboBox()
        self.diagnostic_dataset_name.setObjectName("diagnostic_dataset_name")

        for dataset in available_datasets:
            self.diagnostic_dataset_name.addItem(QString(dataset))


        #    self.indicatorText = QTextEdit(self.groupBox)
        #    self.indicatorText.setReadOnly(True)
        #    self.indicatorText.setLineWidth(0)
        #    self.indicatorText.insertPlainText("<No year selected>")
        self.indicatorResultsTab = QTabWidget()

        QObject.connect(self.indicatorComboBox,SIGNAL("activated(QString)"),self.on_indicatorBox)

        #    self.testvariant = QVariant(1)
        #    self.indicatorText.insertPlainText(self.testvariant.toString())

        #    self.indicatorVBoxLayout.addWidget(self.indicatorComboBox)
        #    self.indicatorVBoxLayout.addWidget(self.indicatorText)
        self.indicatorGridBoxLayout.addWidget(self.indicatorComboBox,0,0)
        self.indicatorGridBoxLayout.addWidget(self.diagnostic_indicator_name,0,1)
        self.indicatorGridBoxLayout.addWidget(self.diagnostic_dataset_name,0,2)
        # new combo boxes
        #    self.indicatorGridBoxLayout.addWidget(self.co_indicator_name,1,0)
        #    self.indicatorGridBoxLayout.addWidget(self.co_source_data,2,0)

        #    self.indicatorGridBoxLayout.addWidget(self.indicatorText,1,0,3,3)
        self.indicatorGridBoxLayout.addWidget(self.indicatorResultsTab,1,0,3,3)

        # end indicator tab

        # For use when printing the year and model
        self.yearString = ""
        self.modelString = ""
    def on_indicatorBox(self,val):
        #    self.indicatorText.clear()
        #    self.indicatorText.insertPlainText("Year: ")
        #    self.indicatorText.insertPlainText(val)
        #    source_text = QString(self.co_source_data.currentText())
        #    if str(source_text) == '[select]':
        #        raise 'need to select a data source!!'
        #       
        indicator_name = QString(self.diagnostic_indicator_name.currentText())
        if str(indicator_name) == '[select indicator]':
            raise 'need to select an indicator!!'

        dataset_name = str(self.diagnostic_dataset_name.currentText())
        if dataset_name == '[select dataset]':
            raise 'need to select a dataset!!' 

        self.result_generator.set_data(
                                       source_data_name = 'Eugene_baseline.run1900',
                                       indicator_name = indicator_name,
                                       dataset_name = dataset_name, 
                                       years = [int(val), int(val)])


        self.resultThread = OpusGuiThread(
                                          parentThread = self.parent,
                                          parent = self,
                                          thread_object = self.result_generator)

        self.resultThread.start()

        self.domDocument = self.parent.toolboxStuff.doc
        self.visualizer = OpusResultVisualizer(
                                               xml_path = self.parent.toolboxStuff.xml_file,
                                               domDocument = self.domDocument,
                                               indicator_type = 'table_per_year',
                                               source_data_name = 'Eugene_baseline.run1900',
                                               indicator_name = indicator_name,
                                               dataset_name = dataset_name,
                                               years = [int(val), int(val)])


        self.visualization_thread = OpusGuiThread(
                                                  parentThread = self.parent,
                                                  parent = self,
                                                  thread_object = self.visualizer)
        self.visualization_thread.start()

        QObject.connect(self.visualization_thread, SIGNAL("runFinished(PyQt_PyObject)"),
                            self.visualizationsCreated)

    def visualizationsCreated(self):
        self.visualizations = self.visualizer.get_visualizations()
        for visualization in self.visualizations:
            guiElement = ViewTableForm(parent = self.parent,
                                       visualization = visualization)
            self.indicatorResultsTab.insertTab(0,guiElement,guiElement.tabIcon,guiElement.tabLabel)

    def on_pbnRemoveModel_released(self):
        #    if(self.running == True):
        if self.runThread:
            self.runThread.cancel()
        if self.timer:
            self.timer.stop()
        self.running = False
        self.paused = False
        self.runManager.removeModelElement(self)
        self.runManager.updateModelElements()

    def on_pbnStartModel_released(self):
        if self.running == True and self.paused == False:
            # Take care of pausing a run
            self.paused = True
            self.timer.stop()
            self.runThread.pause()
            self.pbnStartModel.setText(QString("Resume Model..."))
        elif self.running == True and self.paused == True:
            # Need to resume a paused run
            self.paused = False
            self.timer.start(1000)
            self.runThread.resume()
            self.pbnStartModel.setText(QString("Pause Model..."))
        elif self.running == False:
            # Fire up a new thread and run the model
            self.pbnStartModel.setText(QString("Pause Model..."))
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
            self.simprogressGroupBox.setTitle(QString("Model initializing..."))
            self.runThread = RunModelThread(self.parent,self,self.xml_path)
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
        print "Model Finished with success = ", success
        self.progressBarTotal.setValue(100)
        self.progressBarYear.setValue(100)
        self.progressBarModel.setValue(100)
        self.summaryCurrentYearValue.setText(QString("Finished"))
        self.summaryCurrentModelValue.setText(QString("Finished"))
        self.summaryCurrentPieceValue.setText(QString("Finished"))
        if success:
            self.simprogressGroupBox.setTitle(QString("Model Finished Successfully"))
        else:
            self.simprogressGroupBox.setTitle(QString("Model Unsuccessfully!"))

        self.timer.stop()
        # Get the final logfile update after model finishes...
        self.logFileKey = self.runThread.parent.model._get_current_log(self.logFileKey)
        self.running = False
        self.paused = False
        self.pbnStartModel.setText(QString("Start Model..."))

        #get the last year to show up in the diagnostics tab.
        self.yearItems[len(self.yearItems) - 1][1] = True;
        QComboBox.addItem(self.indicatorComboBox, 
                          QString(str(self.yearItems[len(self.yearItems) - 1][0])),
                          QVariant(self.yearItems[len(self.yearItems) - 1][0]))

    # GUI elements that show progress go here.  Note that they have to be set
    # up first in the constructor of this class, then optionally initialized in
    # on_pbnStartModel_released(), then calculated and updated here, and finally
    # when the simulation is done running, finalized values are optionally
    # defined in runFinishedFromThread (because status.txt doesn't refresh at
    # end of the simulation.
    def runStatusFromThread(self):
#    status = self.runThread.parent.model._compute_progress(self.runThread.parent.model.statusfile)
#    self.progressBar.setValue(status["percentage"])
#    newString = QString(status["message"])
        totalProgress = 0
        yearProgress = 0
        modelProgress = 0
        boxTitle = "Model initializing..." # TODO:  this is for the old prog bar

        if self.runThread.parent.model.statusfile is None:
            boxTitle = "Model initializing..."
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
            statusfile = self.runThread.parent.model.statusfile
            try:

                f = open(statusfile)
                lines = f.readlines()
                f.close()

                # use float for all numbers to help with percent computation
                current_year = float(lines[0])
                total_models = float(lines[1])
                current_model = float(lines[2])
#            current_model_names = lines[3].strip().split('(from')
                current_model_names = lines[3]
                current_model_display_name = current_model_names#current_model_names[0]
#            current_model_detailed_name = current_model_names[1].split(')')[0]
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

                for item in self.yearItems:
                    if (int(item[0]) < int(current_year) and not item[1]) :
                        QComboBox.addItem(self.indicatorComboBox, QString(str(item[0])), QVariant(item[0]))
                        item[1] = True;

                if (self.progressBarTotal.maximum() == 0):
                    self.progressBarTotal.setRange(0,100)
                    self.progressBarYear.setRange(0,100)
                    self.progressBarModel.setRange(0,100)

            except IOError:
                boxTitle = "Model is initializing..."

        newString = QString(boxTitle)

        newString.leftJustified(60)
        self.simprogressGroupBox.setTitle(newString)
        self.progressBarTotal.setValue(totalProgress)
        self.progressBarYear.setValue(yearProgress)
        self.progressBarModel.setValue(modelProgress)


        self.logFileKey = self.runThread.parent.model._get_current_log(self.logFileKey)

    def runErrorFromThread(self,errorMessage):
        self.running = False
        self.paused = False
        self.pbnStartModel.setText(QString("Start Model..."))
        QMessageBox.warning(self.parent,"Warning",errorMessage)

class EstimationGuiElement(QWidget):
    def __init__(self, parent, runManager, estimation):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.runManager = runManager
        self.estimation = estimation
        self.estimation.guiElement = self
        self.inGui = False
        self.logFileKey = 0
        self.running = False
        self.paused = False
        self.timer = None
        self.runThread = None

        # Grab the path to the base XML used to run this model
        self.xml_path = estimation.xml_path

        fileNameInfo = QFileInfo(self.xml_path)
        fileNameAbsolute = fileNameInfo.absoluteFilePath().trimmed()

        self.tabIcon = QIcon(":/Images/Images/cog.png")
        self.tabLabel = fileNameInfo.fileName()

        # LAYOUT FOR THE MODEL ELEMENT IN THE GUI
        self.widgetLayout = QVBoxLayout(self)
        self.widgetLayout.setAlignment(Qt.AlignTop)
        self.groupBox = QGroupBox(self)
        self.widgetLayout.addWidget(self.groupBox)

        stringToUse = "Time Queued - %s" % (time.asctime(time.localtime()))
        self.groupBox.setTitle(QString(stringToUse))

        self.vboxlayout = QVBoxLayout(self.groupBox)
        self.vboxlayout.setObjectName("vboxlayout")

        self.modelControlWidget = QWidget(self.groupBox)
        self.vboxlayout.addWidget(self.modelControlWidget)

        self.vboxlayout2 = QVBoxLayout(self.modelControlWidget)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.progressBarWidget = QWidget(self.groupBox)
        self.progressBarWidget.setObjectName("progressBarWidget")

        self.pbVBoxLayout = QVBoxLayout(self.progressBarWidget)
        self.pbVBoxLayout.setObjectName("pbVBoxLayout")

        self.runProgressBar = QProgressBar(self.progressBarWidget)
        self.runProgressBar.setProperty("value",QVariant(0))
        self.runProgressBar.setObjectName("runProgressBar")
        self.runProgressBar.reset()
        self.pbVBoxLayout.addWidget(self.runProgressBar)

        self.runStatusLabel = QLabel(self.progressBarWidget)
        self.runStatusLabel.setObjectName("runStatusLabel")
        self.runStatusLabel.setMinimumWidth(300)
        self.runStatusLabel.setText(QString("Press Start to run the estimation..."))
        self.pbVBoxLayout.addWidget(self.runStatusLabel)
        self.vboxlayout2.addWidget(self.progressBarWidget)

        self.startWidget = QWidget(self.groupBox)
        self.startWidget.setObjectName("startWidget")

        self.startVBoxLayout = QGridLayout(self.startWidget)
        self.startVBoxLayout.setObjectName("startGridLayout")

        self.pbnStartModel = QPushButton(self.startWidget)
        self.pbnStartModel.setObjectName("pbnStartModel")
        self.pbnStartModel.setText(QString("Start Estimation..."))
        QObject.connect(self.pbnStartModel, SIGNAL("released()"),
                        self.on_pbnStartModel_released)        
        self.startVBoxLayout.addWidget(self.pbnStartModel)
        self.pbnRemoveModel = QPushButton(self.startWidget)
        self.pbnRemoveModel.setObjectName("pbnRemoveModel")
        self.pbnRemoveModel.setText(QString("Cancel/Remove From Queue"))
        QObject.connect(self.pbnRemoveModel, SIGNAL("released()"),
                        self.on_pbnRemoveModel_released)        
        self.startVBoxLayout.addWidget(self.pbnRemoveModel)
        self.vboxlayout2.addWidget(self.startWidget)

        # Add a tab widget and layer in a tree view and log panel
        self.tabWidget = QTabWidget(self.groupBox)

        self.configFile = QFile(self.xml_path)
        if self.configFile.open(QIODevice.ReadOnly):
            self.doc = QDomDocument()
            self.doc.setContent(self.configFile)
            self.dataModel = OpusDataModel(self, self.doc, self.parent, self.configFile,
                                           "model_manager", False)
            self.view = OpusDataView(self.parent)
            self.delegate = OpusDataDelegate(self.view)
            self.view.setItemDelegate(self.delegate)
            self.view.setModel(self.dataModel)
            self.view.expandAll()
            self.view.setAnimated(True)
            self.view.setColumnWidth(0,200)
            self.view.setColumnWidth(1,50)
            self.view.setMinimumHeight(200)
            self.tabWidget.addTab(self.view,"Tree View")

        # Log panel
        self.logText = QTextEdit(self.groupBox)
        self.logText.setReadOnly(True)
        self.logText.setLineWidth(0)
        self.tabWidget.addTab(self.logText,"Log")

        # Finally add the tab to the model page
        self.vboxlayout.addWidget(self.tabWidget)

    def on_pbnRemoveModel_released(self):
        if self.runThread:
            self.runThread.cancel()
        if self.timer:
            self.timer.stop()
        self.running = False
        self.paused = False
        self.runManager.removeEstimationElement(self)
        self.runManager.updateEstimationElements()

    def on_pbnStartModel_released(self):
        if self.running == True and self.paused == False:
            # Take care of pausing a run
            self.paused = True
            self.timer.stop()
            self.runThread.pause()
            self.pbnStartModel.setText(QString("Resume Estimation..."))
        elif self.running == True and self.paused == True:
            # Need to resume a paused run
            self.paused = False
            self.timer.start(1000)
            self.runThread.resume()
            self.pbnStartModel.setText(QString("Pause Estimation..."))
        elif self.running == False:
            # Fire up a new thread and run the estimation
            # References to the GUI elements for status for this run...
            self.progressBar = self.runProgressBar
            self.statusLabel = self.runStatusLabel
            self.pbnStartModel.setText(QString("Pause Estimation..."))
            self.progressBar.setValue(0)
            self.statusLabel.setText(QString("Estimation initializing..."))
            self.runThread = RunEstimationThread(self.parent,self,self.xml_path)
            # Use this signal from the thread if it is capable of producing its own status signal
            QObject.connect(self.runThread, SIGNAL("estimationFinished(PyQt_PyObject)"),
                            self.runFinishedFromThread)
            QObject.connect(self.runThread, SIGNAL("estimationError(PyQt_PyObject)"),
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
            print "Unexpected state in the estimation run..."

    # This is not used currently since the model can not return status... instead we use a timer to
    # check the status from a log file.
    def runPingFromThread(self,value):
        self.progressBar.setValue(value)
        #print "Ping from thread!"

    # Called when the model is finished... peg the percentage to 100% and stop the timer.
    def runFinishedFromThread(self,success):
        print "Estimation Finished with sucess = ", success
        self.progressBar.setValue(100)
        self.statusLabel.setText(QString("Estimation finished with status = %s" % (success)))
        self.timer.stop()
        # Get the final logfile update after model finishes...
        self.logFileKey = self.runThread.parent.estimation._get_current_log(self.logFileKey)
        self.running = False
        self.paused = False
        self.pbnStartModel.setText(QString("Start Estimation..."))

    def runStatusFromThread(self):
        status = self.runThread.parent.estimation._compute_progress()
        self.progressBar.setValue(status["percentage"])
        newString = QString(status["message"])
        newString.leftJustified(60)
        self.statusLabel.setText(newString)
        self.logFileKey = self.runThread.parent.estimation._get_current_log(self.logFileKey)

    def runErrorFromThread(self,errorMessage):
        self.running = False
        self.paused = False
        self.pbnStartModel.setText(QString("Start Estimation..."))
        QMessageBox.warning(self.parent,"Warning",errorMessage)

