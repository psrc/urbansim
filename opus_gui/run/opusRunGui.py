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
from PyQt4.QtXml import *
from opusRunModel_ui import *
from opusRunModel import *

from config.opusDataModel import OpusDataModel
from config.opusDataDelegate import OpusDataDelegate

#from runManagerBase import *
import os, sys, time, tempfile, shutil

# This is the main Run Manager pop-up GUI for looking at models in the queue
class RunModelGui(QDialog, Ui_OpusRunModel):
    def __init__(self, parent, fl):
        QDialog.__init__(self, parent, fl)
        self.setupUi(self)
        self.parent = parent
        self.setFixedSize(self.size())
        
        self.modelElements = []
        for model in self.parent.runManagerStuff.getModelList():
            self.modelElements.append(ModelGuiElement(self,model))
        
        self.groupBoxLayout = QVBoxLayout(self.modelFrame)
        self.groupBoxLayout.setObjectName("groupBoxLayout")
        self.groupBoxLayout.setAlignment(Qt.AlignTop)
        # Now add the tabs...
        self.tabWidget = QTabWidget(self)
        self.groupBoxLayout.addWidget(self.tabWidget)

        for modelElement in self.modelElements:
            self.tabWidget.addTab(modelElement,modelElement.tabIcon,modelElement.tabLabel)
            modelElement.inGui = True
        
    def addModelElement(self,model):
        self.modelElements.insert(0,ModelGuiElement(self,model))

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
                self.tabWidget.addTab(modelElement,modelElement.tabIcon,modelElement.tabLabel)
                modelElement.inGui = True

    def on_pbnCancel_released(self):
        self.close()

# This is an element in the Run Manager GUI that is the container for the model
# and the model thread.  If the start button is pressed then the GUI will create
# a thread to execute the given model.
class ModelGuiElement(QWidget):
    def __init__(self, parent, model):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.model = model
        self.model.guiElement = self
        self.inGui = False
        self.logFileKey = 0
        
        # Grab the path to the base XML used to run this model
        self.xml_path = model.xml_path
        self.tabIcon = QIcon(":/Images/Images/cog.png")
        self.tabLabel = "PlaceHolder"
        
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

        # LAYOUT FOR THE MODEL ELEMENT IN THE GUI
        self.widgetLayout = QVBoxLayout(self)
        self.widgetLayout.setAlignment(Qt.AlignTop)
        self.groupBox = QGroupBox(self)
        self.widgetLayout.addWidget(self.groupBox)

        stringToUse = "Time Queued - %s - Original XML Path - %s" % (time.asctime(time.localtime()),
                                                                     str(self.originalFile.absoluteFilePath()))
        self.groupBox.setTitle(QString(stringToUse))
        #self.setTitle(QString("Time Queued - %s - Original XML Path - %s").append(QString(self.originalFile.absoluteFilePath())))
        #self.groupBox.setFixedHeight(100)
        
        self.vboxlayout = QVBoxLayout(self.groupBox)
        self.vboxlayout.setObjectName("vboxlayout")

        self.modelControlWidget = QWidget(self.groupBox)
        self.vboxlayout.addWidget(self.modelControlWidget)
        
        self.hboxlayout = QHBoxLayout(self.modelControlWidget)
        self.hboxlayout.setObjectName("hboxlayout")

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
        self.runStatusLabel.setAlignment(Qt.AlignCenter)
        self.runStatusLabel.setObjectName("runStatusLabel")
        self.runStatusLabel.setText(QString("Press Start to run the model..."))
        self.pbVBoxLayout.addWidget(self.runStatusLabel)
        self.hboxlayout.addWidget(self.progressBarWidget)

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
        self.hboxlayout.addWidget(self.startWidget)

        # Add a tab widget and layer in a tree view and log panel
        self.tabWidget = QTabWidget(self.groupBox)
        
        self.configFile = QFile(self.xml_path)
        if self.configFile.open(QIODevice.ReadOnly):
            self.doc = QDomDocument()
            self.doc.setContent(self.configFile)
            self.dataModel = OpusDataModel(self.doc, self.parent, self.configFile, False)
            self.view = QTreeView(self.parent)
            self.delegate = OpusDataDelegate(self.view)
            self.view.setItemDelegate(self.delegate)
            self.view.setModel(self.dataModel)
            self.view.setExpanded(self.dataModel.index(0,0,QModelIndex()),True)
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
        self.parent.removeModelElement(self)
        self.parent.updateModelElements()
    
    def on_pbnStartModel_released(self):
        # Fire up a new thread and run the model
        #print "Start Model Pressed"

        # References to the GUI elements for status for this run...
        self.progressBar = self.runProgressBar
        self.statusLabel = self.runStatusLabel

        self.pbnRemoveModel.setEnabled(False)
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
        # Get the final logfile update after model finishes...
        self.logFileKey = self.runThread.parent.model._get_current_log(self.logFileKey)
        self.pbnStartModel.setEnabled(True)
        self.pbnRemoveModel.setEnabled(True)

    def runStatusFromThread(self):
        status = self.runThread.parent.model._compute_progress(self.runThread.parent.model.statusfile)
        self.progressBar.setValue(status["percentage"])
        self.statusLabel.setText(status["message"])
        #print "runStatusFromThread from timer with percentage = %d and message = %s" % (status["percentage"],
        #                                                                                status["message"])
        self.logFileKey = self.runThread.parent.model._get_current_log(self.logFileKey)
