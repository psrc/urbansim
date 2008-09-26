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
from PyQt4.QtCore import QFileInfo, SIGNAL, QObject, QVariant, QString, QTimer
from PyQt4.QtGui import QWidget, QIcon, QMessageBox

from opus_gui.models_manager.run.opusrunestimation import RunEstimationThread
from opus_gui.models_manager.views.ui_estimation_gui_element import Ui_EstimationGuiElement

class EstimationGuiElement(QWidget, Ui_EstimationGuiElement):
    def __init__(self, mainwindow, modelsManagerBase, estimation):
        QWidget.__init__(self, mainwindow)
        self.setupUi(self)
        
        self.mainwindow = mainwindow
        self.mainwindow = mainwindow
        self.modelsManagerBase = modelsManagerBase
        self.estimation = estimation
        self.estimation.guiElement = self
        self.inGui = False
        
        self.running = False
        self.paused = False
        self.timer = None
        self.runThread = None

        # Grab the path to the base XML used to run this model
        self.xml_path = estimation.xml_path

        fileNameInfo = QFileInfo(self.xml_path)
        fileNameAbsolute = fileNameInfo.absoluteFilePath().trimmed()
        self.toolboxBase = self.mainwindow.toolboxBase

        self.tabIcon = QIcon(":/Images/Images/cog.png")
        self.tabLabel = QString('%s estimation'%estimation.model_name)

        # LAYOUT FOR THE MODEL ELEMENT IN THE GUI

        self.runProgressBar.setProperty("value",QVariant(0))
        self.runProgressBar.reset()
     

    def on_pbnRemoveModel_released(self):
        if self.runThread:
            self.runThread.cancel()
        if self.timer:
            self.timer.stop()
        self.running = False
        self.paused = False
        self.modelsManagerBase.removeGuiElement(self)
        self.modelsManagerBase.updateGuiElements()

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
            self.logFileKey = 0
            # Update the XML
            self.toolboxBase.updateOpusXMLTree()
            # Fire up a new thread and run the estimation
            # References to the GUI elements for status for this run...
            self.progressBar = self.runProgressBar
            self.statusLabel = self.runStatusLabel
            self.pbnStartModel.setText(QString("Pause Estimation..."))
            self.progressBar.setValue(0)
            self.statusLabel.setText(QString("Estimation initializing..."))
            self.runThread = RunEstimationThread(self.mainwindow,self,self.xml_path)
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
        if success:
            self.statusLabel.setText(QString("Estimation finished successfully"))
        else:
            self.statusLabel.setText(QString("Estimation failed"))
        self.timer.stop()
        # Get the final logfile update after model finishes...
        self.logFileKey = self.runThread.estimationguielement.estimation._get_current_log(self.logFileKey)
        
        
        self.running = False
        self.paused = False
        self.pbnStartModel.setText(QString("Start Estimation..."))

    def runStatusFromThread(self):
        status = self.runThread.estimationguielement.estimation._compute_progress()
        self.progressBar.setValue(status["percentage"])
        newString = QString(status["message"])
        newString.leftJustified(60)
        self.statusLabel.setText(newString)
        self.logFileKey = self.runThread.estimationguielement.estimation._get_current_log(self.logFileKey)

    def runErrorFromThread(self,errorMessage):
        self.running = False
        self.paused = False
        self.pbnStartModel.setText(QString("Start Estimation..."))
        QMessageBox.warning(self.mainwindow,"Warning",errorMessage)
