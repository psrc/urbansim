# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE
from PyQt4.QtCore import QFileInfo, SIGNAL, QObject, QVariant, QString, QTimer, pyqtSlot
from PyQt4.QtGui import QWidget, QIcon, QMessageBox

from opus_gui.models_manager.run.run_estimation import RunEstimationThread
from opus_gui.models_manager.views.ui_estimation_gui_element import Ui_EstimationGuiElement
from opus_gui.main.controllers.dialogs.message_box import MessageBox
from opus_gui.main.controllers.instance_handlers import get_mainwindow_instance
from opus_gui.util.icon_library import IconLibrary

class EstimationGuiElement(QWidget, Ui_EstimationGuiElement):
    def __init__(self, mainwindow, modelsManagerBase, estimation):
        QWidget.__init__(self, mainwindow)
        self.setupUi(self)

        self.mainwindow = mainwindow

        self.estimation = estimation
        self.estimation.guiElement = self
        self.inGui = False

        self.running = False
        self.paused = False
        self.timer = None
        self.runThread = None

        self.manager = modelsManagerBase

        self.tabIcon = IconLibrary.icon('estimation')
        self.tabLabel = QString('%s estimation'%estimation.model_name)

        # LAYOUT FOR THE MODEL ELEMENT IN THE GUI

        self.runProgressBar.setProperty("value",QVariant(0))
        self.runProgressBar.reset()

    def removeElement(self):
        self.on_pbnRemoveModel_clicked()
        return True

    @pyqtSlot()
    def on_pbnRemoveModel_clicked(self):
        if self.runThread:
            self.runThread.cancel()
        if self.timer:
            self.timer.stop()
        self.running = False
        self.paused = False

    @pyqtSlot()
    def on_pbnStartModel_clicked(self):

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
            # Update the XMLConfig
            self.manager.project.update_xml_config()
            # Fire up a new thread and run the estimation
            # References to the GUI elements for status for this run...
            self.progressBar = self.runProgressBar
            self.statusLabel = self.runStatusLabel
            self.pbnStartModel.setText(QString("Pause Estimation..."))
            self.progressBar.setValue(0)
            self.statusLabel.setText(QString("Estimation initializing..."))
            self.runThread = RunEstimationThread(get_mainwindow_instance(), self)
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
        MessageBox.warning(mainwindow = self,
                          text = "There was a problem with the estimation.",
                          detailed_text = errorMessage)
