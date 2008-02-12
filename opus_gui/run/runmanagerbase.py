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

from run.model.opusrunmodel import *
from run.estimation.opusrunestimation import *
from config.xmlmodelview.opusdataview import OpusDataView
from config.xmlmodelview.opusdatamodel import OpusDataModel
from config.xmlmodelview.opusdatadelegate import OpusDataDelegate

# General system includes
import os, sys, time, tempfile, shutil, string

  
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
    
    # Grab the path to the base XML used to run this model
    self.xml_path = model.xml_path
    
    # Need to make a copy of the project environment to work from
    self.originalFile = QFileInfo(self.xml_path)
    self.originalDirName = self.originalFile.dir().dirName()
    self.copyDir = QString(self.parent.tempDir)
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
    
    self.tabIcon = QIcon(":/Images/Images/cog.png")
    self.tabLabel = self.originalFile.fileName()
    
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
    #self.runStatusLabel.setAlignment(Qt.AlignCenter)
    self.runStatusLabel.setObjectName("runStatusLabel")
    self.runStatusLabel.setMinimumWidth(300)
    self.runStatusLabel.setText(QString("Press Start to run the model..."))
    self.pbVBoxLayout.addWidget(self.runStatusLabel)
    self.vboxlayout2.addWidget(self.progressBarWidget)
    
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
    self.simprogressWidget = QWidget(self.groupBox)
    self.simprogressWidget.setObjectName("simprogressWidget")
    self.simprogressLayout = QGridLayout(self.simprogressWidget)
    self.simprogressGroupBox = QGroupBox(self)
    self.simprogressLayout2 = QGridLayout(self.simprogressGroupBox)
    self.simprogressLayout.addWidget(self.simprogressGroupBox)
    self.simprogressText = QTextEdit(self.simprogressGroupBox)
    self.simprogressText.setReadOnly(True)
    self.simprogressText.setFrameStyle(QFrame.NoFrame)
    self.simprogressLayout2.addWidget(self.simprogressText)
    self.tabWidget.addTab(self.simprogressWidget,"Simulation Progress")

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
    
  def on_pbnRemoveModel_released(self):
    self.runManager.removeModelElement(self)
    self.runManager.updateModelElements()
    
  def on_pbnStartModel_released(self):
    # Fire up a new thread and run the model
    #print "Start Model Pressed"
    
    # References to the GUI elements for status for this run...
    self.progressBar = self.runProgressBar
    self.statusLabel = self.runStatusLabel
    
    #self.pbnRemoveModel.setEnabled(False)
    self.pbnStartModel.setEnabled(False)
    self.progressBar.setValue(0)
    self.statusLabel.setText(QString("Model initializing..."))
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
    #self.pbnRemoveModel.setEnabled(True)
    
  def runStatusFromThread(self):
    status = self.runThread.parent.model._compute_progress(self.runThread.parent.model.statusfile)
    self.progressBar.setValue(status["percentage"])
    newString = QString(status["message"])
    newString.leftJustified(60)
    self.statusLabel.setText(newString)
    self.simprogressGroupBox.setTitle(newString)
    self.simprogressText.insertPlainText(QString("."))
    self.logFileKey = self.runThread.parent.model._get_current_log(self.logFileKey)
    
  def runErrorFromThread(self,errorMessage):
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
    
    # Grab the path to the base XML used to run this model
    self.xml_path = estimation.xml_path
    
    # Need to make a copy of the project environment to work from
    self.originalFile = QFileInfo(self.xml_path)
    self.originalDirName = self.originalFile.dir().dirName()
    self.copyDir = QString(self.parent.tempDir)
    self.projectCopyDir = QDir(QString(tempfile.mkdtemp(prefix='opus_estimation',dir=str(self.copyDir))))
    # Copy the project dir from original to copy...
    tmpPathDir = self.originalFile.dir()
    tmpPathDir.cdUp()
    # Go ahead and copy from one dir up (assumed to be the project space...
    shutil.copytree(str(tmpPathDir.absolutePath()),
                    str(self.projectCopyDir.absolutePath().append(QString("/").append(tmpPathDir.dirName()))))
    # Now we can build the new path to the copy of the original file but in the temp space...
    self.xml_path = self.projectCopyDir.absolutePath().append(QString("/"))
    self.xml_path = self.xml_path.append(tmpPathDir.dirName().append("/").append(self.originalDirName))
    self.xml_path = self.xml_path.append(QString("/"))
    self.xml_path = self.xml_path.append(QFileInfo(self.originalFile.fileName()).fileName())
    
    self.tabIcon = QIcon(":/Images/Images/cog.png")
    self.tabLabel = self.originalFile.fileName()
    
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
    self.pbnRemoveModel.setText(QString("Remove From Queue"))
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
    self.runManager.removeEstimationElement(self)
    self.runManager.updateEstimationElements()
    
  def on_pbnStartModel_released(self):
    # Fire up a new thread and run the model
    # References to the GUI elements for status for this run...
    self.progressBar = self.runProgressBar
    self.statusLabel = self.runStatusLabel
    
    #self.pbnRemoveModel.setEnabled(False)
    self.pbnStartModel.setEnabled(False)
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
    self.runThread.start()
    
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
    self.pbnStartModel.setEnabled(True)
    
  def runStatusFromThread(self):
    status = self.runThread.parent.estimation._compute_progress(self.runThread.parent.estimation.statusfile)
    self.progressBar.setValue(status["percentage"])
    newString = QString(status["message"])
    newString.leftJustified(60)
    self.statusLabel.setText(newString)
    self.logFileKey = self.runThread.parent.estimation._get_current_log(self.logFileKey)
    
  def runErrorFromThread(self,errorMessage):
    QMessageBox.warning(self.parent,"Warning",errorMessage)
    
