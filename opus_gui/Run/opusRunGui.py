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
#from runManagerBase import *
import os, sys, time, tempfile, shutil

class RunModelGui(QDialog, Ui_OpusRunModel):
    def __init__(self, parent, fl):
        QDialog.__init__(self, parent, fl)
        self.setupUi(self)
        self.parent = parent
        self.modelElements = []
        for model in self.parent.runManagerStuff.getModelList():
            self.modelElements.append(ModelGuiElement(self,model))
        self.groupBoxLayout = QVBoxLayout(self.groupBox)
        self.groupBoxLayout.setObjectName("groupBoxLayout")
        for modelElement in self.modelElements:
            self.groupBoxLayout.addWidget(modelElement)
            modelElement.inGui = True

    def addModelElement(self,model):
        self.modelElements.append(ModelGuiElement(self,model))

    def updateModelElements(self):
        for modelElement in self.modelElements:
            if modelElement.inGui == False:
                self.groupBoxLayout.addWidget(modelElement)
                modelElement.inGui = True

    def on_pbnCancel_released(self):
        self.close()

        
class ModelGuiElement(QWidget):
    def __init__(self, parent, model):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.model = model
        self.inGui = False
        
        # For now grab the first model in the manager
        #xml_path = self.parent.runManagerStuff.modelList[0].xml_file
        self.xml_path = model.xml_path

        # LAYOUT FOR THE MODEL ELEMENT IN THE GUI
        self.hboxlayout = QHBoxLayout(self)
        self.hboxlayout.setObjectName("hboxlayout")

        self.progressBarWidget = QWidget(self)
        self.progressBarWidget.setObjectName("progressBarWidget")

        self.pbVBoxLayout = QVBoxLayout(self.progressBarWidget)
        self.pbVBoxLayout.setObjectName("pbVBoxLayout")

        self.runProgressBar = QProgressBar(self.progressBarWidget)
        self.runProgressBar.setProperty("value",QVariant(0))
        self.runProgressBar.setObjectName("runProgressBar")
        self.runProgressBar.reset()
        self.pbVBoxLayout.addWidget(self.runProgressBar)

        self.runStatusLabel = QLabel(self.progressBarWidget)
        self.runStatusLabel.setAlignment(Qt.AlignCenter)
        self.runStatusLabel.setObjectName("runStatusLabel")
        self.runStatusLabel.setText(QString("Press Start to run the model..."))
        self.pbVBoxLayout.addWidget(self.runStatusLabel)
        self.hboxlayout.addWidget(self.progressBarWidget)

        self.startWidget = QWidget(self)
        self.startWidget.setObjectName("startWidget")

        self.startGridLayout = QGridLayout(self.startWidget)
        self.startGridLayout.setObjectName("startGridLayout")

        self.pbnStartModel = QPushButton(self.startWidget)
        self.pbnStartModel.setObjectName("pbnStartModel")
        self.pbnStartModel.setText(QString("Start..."))
        QObject.connect(self.pbnStartModel, SIGNAL("released()"),
                        self.on_pbnStartModel_released)        
        self.startGridLayout.addWidget(self.pbnStartModel,0,0,1,1)
        self.hboxlayout.addWidget(self.startWidget)
        
    def on_pbnStartModel_released(self):
        # Fire up a new thread and run the model
        print "Start Model Pressed"

        # Need to make a copy of the project environment to work from
        self.originalFile = QFileInfo(self.xml_path)
        self.originalDirName = self.originalFile.dir().dirName()
        self.copyDir = QString(self.parent.parent.tempDir)
        self.projectCopyDir = QDir(QString(tempfile.mkdtemp(prefix='opus_model',dir=str(self.copyDir))))
        # Copy the project dir from original to copy...
        tmpPathDir = self.originalFile.dir()
        tmpPathDir.cdUp()
        #print "%s, %s" % (tmpPathDir.absolutePath(), self.projectCopyDir.absolutePath())
        # Go ahead and copy from one dir up (assumed to be the project space...
        shutil.copytree(str(tmpPathDir.absolutePath()),
                        str(self.projectCopyDir.absolutePath().append(QString("/").append(tmpPathDir.dirName()))))
        # Now we can build the new path to the copy of the original file but in the temp space...
        self.xml_path = self.projectCopyDir.absolutePath().append(QString("/"))
        self.xml_path = self.xml_path.append(tmpPathDir.dirName().append("/").append(self.originalDirName))
        self.xml_path = self.xml_path.append(QString("/"))
        self.xml_path = self.xml_path.append(QFileInfo(self.originalFile.fileName()).fileName())
        # References to the GUI elements for status for this run...
        self.progressBar = self.runProgressBar
        self.statusLabel = self.runStatusLabel

        self.pbnStartModel.setEnabled(False)
        self.progressBar.setValue(0)
        self.statusLabel.setText(QString("Model initializing..."))
        self.runThread = RunModelThread(self.parent,self,self.xml_path)
        # Use this signal from the thread if it is capable of producing its own status signal
        QObject.connect(self.runThread, SIGNAL("runFinished(PyQt_PyObject)"),
                        self.runFinishedFromThread)
        # Use this timer to call a function in the thread to check status if the thread is unable
        # to produce its own signal above
        self.timer = QTimer()
        QObject.connect(self.timer, SIGNAL("timeout()"),
                        self.runStatusFromThread)
        self.timer.start(1000)
        self.runThread.start()
            
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
        status = self.runThread.parent.model._compute_progress(self.runThread.parent.model.statusfile)
        self.progressBar.setValue(status["percentage"])
        self.statusLabel.setText(status["message"])
        print "runStatusFromThread from timer with percentage = %d and message = %s" % (status["percentage"],
                                                                                        status["message"])
