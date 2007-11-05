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
import sys,time

class OpusModelTest():
    def __init__(self,parent):
        self.parent = parent

    def run(self):
        for i in range(101):
            self.parent.progressCallback(i)
            time.sleep(0.1)
        self.parent.finishedCallback(True)
        
    
class RunModelThread(QThread):
    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.parent = parent
        
    def run(self):
        self.parent.progressBar.setRange(0,100)
        self.model = OpusModelTest(self)
        self.model.run()

    def progressCallback(self,percent):
        print "Ping From Model"
        self.emit(SIGNAL("runPing(PyQt_PyObject)"),percent)

    def finishedCallback(self,success):
        if success:
            print "Success retruned from Model"
        else:
            print "Error retruned from Model"
        self.emit(SIGNAL("runFinished(PyQt_PyObject)"),success)
            

class RunModelGui(QDialog, Ui_OpusRunModel):
    def __init__(self, parent, fl):
        QDialog.__init__(self, parent, fl)
        self.setupUi(self)
        self.parent = parent
        self.progressBar = self.runProgressBar
        self.progressBar.reset()

    def on_pbnStartModel_released(self):
	# Fire up a new thread and run the model
        print "Start Model Pressed"
	self.runThread = RunModelThread(self)
        QObject.connect(self.runThread, SIGNAL("runPing(PyQt_PyObject)"),
                        self.runPingFromThread)
        QObject.connect(self.runThread, SIGNAL("runFinished(PyQt_PyObject)"),
                        self.runFinishedFromThread)
        self.runThread.start()
            
    def on_pbnCancel_released(self):
        self.close()

    def runPingFromThread(self,value):
        self.progressBar.setValue(value)
        print "Ping from thread!"

    def runFinishedFromThread(self,success):
        print "Model Finished!"

