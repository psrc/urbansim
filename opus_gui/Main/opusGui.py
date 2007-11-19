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

# UI specific includes
from opusMain_ui import Ui_MainWindow

from Util.consoleBase import *
from Config.toolboxBase import *
from Run.runManagerBase import *

# General system includes
import sys,time,tempfile

  
# Main window used for houseing the canvas, toolbars, and dialogs
class OpusGui(QMainWindow, Ui_MainWindow):

  def __init__(self):
    QMainWindow.__init__(self)
    
    # required by Qt4 to initialize the UI
    self.setupUi(self)
    
    self.splashPix = QPixmap(QString("Main/Images/new-logo-medium.png"))
    self.splashPixScaled = self.splashPix.scaled(210,180,Qt.KeepAspectRatio)
    self.splash = QSplashScreen(self.splashPixScaled)
    self.splash.show()

    # We need to initialize the window sizes
    self.splitter.setSizes([450,550])

    # Play with the project and config load/save
    QObject.connect(self.actionOpen_Project, SIGNAL("triggered()"), self.openProject)
    QObject.connect(self.actionOpen_Config, SIGNAL("triggered()"), self.openConfig)
    QObject.connect(self.actionSave_Project, SIGNAL("triggered()"), self.saveProject)
    QObject.connect(self.actionSave_Project_As, SIGNAL("triggered()"), self.saveProjectAs)
    QObject.connect(self.actionSave_Config, SIGNAL("triggered()"), self.saveConfig)
    QObject.connect(self.actionSave_Config_As, SIGNAL("triggered()"), self.saveConfigAs)
    # Exit
    QObject.connect(self.actionExit, SIGNAL("triggered()"), self.exitOpus)

    QObject.connect(self.actionRun_Manager, SIGNAL("triggered()"), self.openRunManager)

    self.tempDir = tempfile.mkdtemp(prefix='opus_gui')

    try:
      import qgis.core
      import Map.mapBase
      # Only load the map stuff if QGIS is loadable
      self.mapStuff = Map.mapBase.MapBase(self)
    except ImportError:
      pass
    
    self.consoleStuff = ConsoleBase(self)

    self.toolboxStuff = ToolboxBase(self)

    self.runManagerStuff = RunManagerBase(self)
    flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | \
            Qt.WindowMaximizeButtonHint 
    self.runManagerGui = RunModelGui(self,flags)
    self.runManagerStuff.setGui(self.runManagerGui)

    time.sleep(2)
    self.splash.hide()

  def openRunManager(self):
    print "Open Run Manager pressed..."
    self.runManagerGui.show()

  def openProject(self):
    print "Open Project pressed..."
    projectDialog = QFileDialog()
    fd = projectDialog.getExistingDirectory(self,QString("Please select project directory..."),
                                            QString(), QFileDialog.ShowDirsOnly)
    # Check for cancel
    if len(fd) == 0:
      return
    dirName = QString(fd)
    dirNameInfo = QFileInfo(QString(fd))
    dirNameBaseName = dirNameInfo.completeBaseName()
    print "Dirname = ", dirName
    # Now we recursively loop through and create an XML file tree
    
  def openConfig(self):
    print "Open Config pressed..."
    configDialog = QFileDialog()
    filter_str = QString("*.xml")
    fd = configDialog.getOpenFileName(self,QString("Please select an xml config file..."),
                                      QString(), filter_str)
    # Check for cancel
    if len(fd) == 0:
      return
    fileName = QString(fd)
    fileNameInfo = QFileInfo(QString(fd))
    fileNameBaseName = fileNameInfo.completeBaseName()
    print "Filename = ", fileName
    # Open the file and add to the Run tab...
    self.toolboxStuff.openXMLTree(fileName)
    
  def saveProject(self):
    print "Save Project pressed..."
    
  def saveProjectAs(self):
    print "Save Project As pressed..."
    
  def saveConfig(self):
    print "Save Config pressed..."
    
  def saveConfigAs(self):
    print "Save Config As pressed..."
    
  def exitOpus(self):
    print "Exit pressed..."
    self.close()
