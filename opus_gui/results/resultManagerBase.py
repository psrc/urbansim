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

from PyQt4.QtCore import QString, QObject, SIGNAL, QFileInfo, \
                         QDir, Qt, QTimer
from PyQt4.QtGui import QMessageBox, QLineEdit, QComboBox, QGridLayout, \
                        QTextEdit, QTabWidget, QWidget, QPushButton, \
                        QGroupBox, QVBoxLayout, QIcon, QLabel, \
                        QImage, QPainter

from opus_gui.results.opus_result_generator \
    import OpusResultThread

# General system includes
import os, sys, tempfile, shutil


class AbstractManagerBase(object):
    def __init__(self, parent):
        self.parent = parent
        self.tabWidget = parent.tabWidget
        self.gui = parent
        self.guiElements = []
    
    def removeTab(self,guiElement):
        self.tabWidget.removeTab(self.tabWidget.indexOf(guiElement))
        self.guiElements.remove(guiElement)
        guiElement.hide()
    
    def updateGuiElements(self):
        for guiElement in self.guiElements:
            if guiElement.inGui == False:
                self.tabWidget.insertTab(0,guiElement,guiElement.tabIcon,guiElement.tabLabel)
                self.tabWidget.setCurrentIndex(0)
                guiElement.inGui = True
    
    def setGui(self, gui):
        self.gui = gui
    
# Main Run manager class
class ResultManagerBase(AbstractManagerBase):        
                
    def addGenerateIndicatorForm(self, result_run):
        new_form = GenerateResultsForm(parent = self.parent,
                                       result_manager = self,
                                       result_generator = result_run)
        self.guiElements.insert(0, new_form)
        self.updateGuiElements()
    
    def addViewImageIndicator(self, visualization):
        new_form = ViewImageForm(parent = self.parent,
                                 visualization = visualization)
        self.guiElements.insert(0, new_form)
        self.updateGuiElements()

class ViewImageForm(QWidget):
    def __init__(self, parent, visualization):
        QWidget.__init__(self, parent)
        self.inGui = False
        self.visualization = visualization
        
        self.widgetLayout = QVBoxLayout(self)
        self.widgetLayout.setAlignment(Qt.AlignTop)

        self.groupBox = QGroupBox(self)
        self.widgetLayout.addWidget(self.groupBox)

        file_path = self.visualization.get_file_path()
        print file_path, os.path.exists(file_path)
        self.lbl_image = QImage(QString(file_path))
        
        self.tabIcon = QIcon(":/Images/Images/map.png")
        self.tabLabel = visualization.table_name
    
    def paintEvent(self, Event):
        print Event
        self.pntr_painter = QPainter(self.groupBox)
        self.pntr_painter.drawImage(0,0,self.lbl_image) 


# This is an element in the Run Manager GUI that is the container for the model
# and the model thread.  If the start button is pressed then the GUI will create
# a thread to execute the given model.
class GenerateResultsForm(QWidget):
    def __init__(self, parent, result_manager, result_generator):
        #element is a OpusResultGenerator
        QWidget.__init__(self, parent)
        self.parent = parent
        self.result_manager = result_manager
        self.result_generator = result_generator
        self.result_generator.guiElement = self
        self.inGui = False
        self.logFileKey = 0
        
        # Grab the path to the base XML used to run this model
        self.xml_path = result_generator.xml_path
        
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
        self.tabLabel = "Generate results"

        # LAYOUT FOR THE MODEL ELEMENT IN THE GUI

        self.widgetLayout = QVBoxLayout(self)
        self.widgetLayout.setAlignment(Qt.AlignTop)

        self.groupBox = QGroupBox(self)
        self.widgetLayout.addWidget(self.groupBox)
        
        self._setup_definition_widget()

        self._setup_buttons()
        self._setup_tabs()
        
    def _setup_buttons(self):
        # Add Generate button...
        self.pbn_generate_results = QPushButton(self.groupBox)
        self.pbn_generate_results.setObjectName("pbn_generate_results")
        self.pbn_generate_results.setText(QString("Create results..."))
        
        QObject.connect(self.pbn_generate_results, SIGNAL("released()"),
                        self.on_pbn_generate_results_released)        
        self.widgetLayout.addWidget(self.pbn_generate_results)
        
    def _setup_tabs(self):
        # Add a tab widget and layer in a tree view and log panel
        self.tabWidget = QTabWidget(self.groupBox)
    
        # Log panel
        self.logText = QTextEdit(self.groupBox)
        self.logText.setReadOnly(True)
        self.logText.setLineWidth(0)
        self.tabWidget.addTab(self.logText,"Log")

        # Finally add the tab to the model page
        self.widgetLayout.addWidget(self.tabWidget)
        
#
    def _setup_definition_widget(self):
        self.gridlayout = QGridLayout(self.groupBox)
        self.gridlayout.setObjectName("gridlayout")

        self.lbl_indicator_name = QLabel(self.groupBox)
        self.lbl_indicator_name.setObjectName("lbl_indicator_name")
        self.lbl_indicator_name.setText(QString("Indicator"))
        self.gridlayout.addWidget(self.lbl_indicator_name,0,0,1,1)

        self._setup_co_indicator_name()
        self.gridlayout.addWidget(self.co_indicator_name,0,1,1,1)

        self.lbl_dataset_name = QLabel(self.groupBox)
        self.lbl_dataset_name.setObjectName("lbl_dataset_name")
        self.lbl_dataset_name.setText(QString("Dataset"))
        self.gridlayout.addWidget(self.lbl_dataset_name,1,0,1,1)

        self._setup_co_dataset_name()
        
        self.gridlayout.addWidget(self.co_dataset_name,1,1,1,1)

        self.lbl_source_data = QLabel(self.groupBox)
        self.lbl_source_data.setObjectName("lbl_source_data")
        self.lbl_source_data.setText(QString("Source data"))
        self.gridlayout.addWidget(self.lbl_source_data,2,0,1,1)

        self._setup_co_source_data()
        self.gridlayout.addWidget(self.co_source_data,2,1,1,1) 

    def _setup_co_indicator_name(self):
        self.co_indicator_name = QComboBox(self.groupBox)
        self.co_indicator_name.setObjectName("co_indicator_name")
        self.co_indicator_name.addItem(QString("[select]"))
        
    def _setup_co_dataset_name(self):
        available_datasets = [
            '[select]',
            'gridcell',
            'zone',
            'taz',
            'county',
            'all_data'
        ]
        self.co_dataset_name = QComboBox(self.groupBox)
        self.co_dataset_name.setObjectName("co_dataset_name")
        
        for dataset in available_datasets:
            self.co_dataset_name.addItem(QString(dataset))
            
    def _setup_co_source_data(self):
        self.co_source_data = QComboBox(self.groupBox)
        self.co_source_data.setObjectName("co_source_data")
        self.co_source_data.addItem(QString("[select]"))
                
    def on_pbnRemoveModel_released(self):
        self.result_manager.removeTab(self)
        self.result_manager.updateGuiElements()
    
    def on_pbn_generate_results_released(self):
        # Fire up a new thread and run the model
        print "Generate results button pressed"

        # References to the GUI elements for status for this run...
        #self.statusLabel = self.runStatusLabel
        #self.statusLabel.setText(QString("Model initializing..."))
        
        self.pbn_generate_results.setEnabled(False)
        
        self.runThread = OpusResultThread(
                              parentThread = self.parent,
                              parent = self,
                              xml_file = self.xml_path)
        # Use this signal from the thread if it is capable of producing its own status signal
        QObject.connect(self.runThread, SIGNAL("runFinished(PyQt_PyObject)"),
                        self.runFinishedFromThread)
        QObject.connect(self.runThread, SIGNAL("runError(PyQt_PyObject)"),
                        self.runErrorFromThread)

        # Use this timer to call a function in the thread to check status if the thread is unable
        # to produce its own signal above
        self.timer = QTimer()
        QObject.connect(self.timer, SIGNAL("timeout()"),
                        self.runUpdateLog)
        self.timer.start(1000)
        
        self.runThread.start()

    def runUpdateLog(self):
        self.logFileKey = self.runThread.parent.element._get_current_log(self.logFileKey)

    # Called when the model is finished... 
    def runFinishedFromThread(self,success):
        print "Model Finished with sucess = ", success
#        self.statusLabel.setText(QString("Model finished with status = %s" % (success)))

        # Get the final logfile update after model finishes...
        self.logFileKey = self.runThread.parent.element._get_current_log(self.logFileKey)
        self.pbn_generate_results.setEnabled(True)

    def runErrorFromThread(self,errorMessage):
        QMessageBox.warning(self.parent,"Warning",errorMessage)
  
