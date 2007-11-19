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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from opusRunModel_ui import *
from opusRunModel import *
import os, sys, time

class RunModelThread(QThread):
    def __init__(self, parent, xml_file):
        QThread.__init__(self, parent)
        self.parent = parent
        self.xml_file = xml_file
        
    def run(self):
        self.parent.progressBar.setRange(0,100)
        self.model = OpusModel(self,self.xml_file)
        self.model.run()

    def progressCallback(self,percent):
        print "Ping From Model"
        self.emit(SIGNAL("runPing(PyQt_PyObject)"),percent)

    def finishedCallback(self,success):
        if success:
            print "Success returned from Model"
        else:
            print "Error returned from Model"
        self.emit(SIGNAL("runFinished(PyQt_PyObject)"),success)
            

class RunModelGui(QDialog, Ui_OpusRunModel):
    def __init__(self, parent, fl, xml_path):
        QDialog.__init__(self, parent, fl)
        self.setupUi(self)
        self.parent = parent
        self.xml_path = xml_path
        self.progressBar = self.runProgressBar
        self.statusLabel = self.runStatusLabel
        self.progressBar.reset()
        self.statusLabel.setText(QString("Press Start to run the model..."))

    def on_pbnStartModel_released(self):
        # Fire up a new thread and run the model
        print "Start Model Pressed"
        self.pbnStartModel.setEnabled(False)
        self.progressBar.setValue(0)
        self.statusLabel.setText(QString("Model initializing..."))
        self.runThread = RunModelThread(self, self.xml_path)
        # Use this signal from the thread if it is capable of producing its own status signal
        #QObject.connect(self.runThread, SIGNAL("runPing(PyQt_PyObject)"),
        #                self.runPingFromThread)
        QObject.connect(self.runThread, SIGNAL("runFinished(PyQt_PyObject)"),
                        self.runFinishedFromThread)
        # Use this timer to call a function in the thread to check status if the thread is unable
        # to produce its own signal above
        self.timer = QTimer()
        QObject.connect(self.timer, SIGNAL("timeout()"),
                        self.runStatusFromThread)
        self.timer.start(1000)
        self.runThread.start()
            
    def on_pbnCancel_released(self):
        self.close()

    # This is not used currently since the model can not return status... instead we use a timer to
    # check the status from a log file.
    def runPingFromThread(self,value):
        self.progressBar.setValue(value)
        #print "Ping from thread!"

    # Called when the model is finished... peg the percentage to 100% and stop the timer.
    def runFinishedFromThread(self,success):
        print "Model Finished with sucess = ", success
        self.progressBar.setValue(100)
        self.statusLabel.setText(QString("Model finished with status = %s" % (success)))
        self.timer.stop()
        self.pbnStartModel.setEnabled(True)

    def runStatusFromThread(self):
        status = self.runThread.model._compute_progress(self.runThread.model.statusfile)
        self.progressBar.setValue(status["percentage"])
        self.statusLabel.setText(status["message"])
        print "runStatusFromThread from timer with percentage = %d and message = %s" % (status["percentage"],
                                                                                        status["message"])
