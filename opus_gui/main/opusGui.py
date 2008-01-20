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
from opusAbout import UrbansimAboutGui

from util.consolebase import *
from config.toolboxBase import *
from run.runManagerBase import *
from results.resultManagerBase import *

# General system includes
import sys,time,tempfile


# Main window used for houseing the canvas, toolbars, and dialogs
class OpusGui(QMainWindow, Ui_MainWindow):

  def __init__(self):
    QMainWindow.__init__(self)

    # required by Qt4 to initialize the UI
    self.setupUi(self)

    #self.splashPix = QPixmap(QString("main/Images/new-logo-medium.png"))
    self.splashPix = QPixmap(QString("main/Images/az-smart.bmp"))
    #self.splashPixScaled = self.splashPix.scaled(210,180,Qt.KeepAspectRatio)
    self.splashPixScaled = self.splashPix.scaled(600,252,Qt.KeepAspectRatio)
    self.splash = QSplashScreen(self.splashPixScaled)
    self.splash.show()

    # We need to initialize the window sizes
    self.splitter.setSizes([550,550])

    # Play with the project and config load/save
    QObject.connect(self.actionOpen_Project_2, SIGNAL("triggered()"), self.openConfig)
    QObject.connect(self.actionSave_Project_2, SIGNAL("triggered()"), self.saveConfig)
    QObject.connect(self.actionSave_Project_As_2, SIGNAL("triggered()"), self.saveConfigAs)
    # Exit
    QObject.connect(self.actionExit, SIGNAL("triggered()"), self.exitOpus)
    # About
    QObject.connect(self.actionAbout, SIGNAL("triggered()"), self.openAbout)

    self.tempDir = tempfile.mkdtemp(prefix='opus_gui')

    try:
      import qgis.core
      import map.mapbase
      # Only load the map stuff if QGIS is loadable
      self.mapStuff = map.mapbase.MapBase(self)
    except ImportError:
      self.mapStuff = None

    self.consoleStuff = ConsoleBase(self)
    self.toolboxStuff = ToolboxBase(self)
    self.runManagerStuff = RunManagerBase(self)
    self.runManagerStuff.setGui(self)

    self.resultManagerStuff = ResultManagerBase(self)
    self.resultManagerStuff.setGui(self)

    try:
      import util.editorbase
      self.editorStatusLabel = QLabel(self)
      self.editorStatusLabel.setAlignment(Qt.AlignCenter)
      self.editorStatusLabel.setObjectName("editorStatusLabel")
      self.editorStatusLabel.setText(QString("No files currently loaded..."))
      self.tab_editorView.layout().addWidget(self.editorStatusLabel)
      self.editorStuff = util.editorbase.EditorBase(self)
      self.tab_editorView.layout().addWidget(self.editorStuff)
    except ImportError:
      self.editorStuff = None

    time.sleep(1)
    self.splash.hide()

  def openAbout(self):
    flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
    wnd = UrbansimAboutGui(self,flags)
    wnd.show()

  def openConfig(self):
    saveBeforeOpen = QMessageBox.Discard
    if self.toolboxStuff.resultsManagerTree and self.toolboxStuff.resultsManagerTree.model.dirty:
      saveBeforeOpen = QMessageBox.question(self,"Warning",
                                      "Current project contains changes... \nShould we save or discard those changes before opening?",
                                      QMessageBox.Discard,QMessageBox.Save)
    elif self.toolboxStuff.modelManagerTree and self.toolboxStuff.modelManagerTree.model.dirty:
      saveBeforeOpen = QMessageBox.question(self,"Warning",
                                      "Current project contains changes... \nShould we save or discard those changes before opening?",
                                      QMessageBox.Discard,QMessageBox.Save)
    elif self.toolboxStuff.runManagerTree and self.toolboxStuff.runManagerTree.model.dirty:
      saveBeforeOpen = QMessageBox.question(self,"Warning",
                                      "Current project contains changes... \nShould we save or discard those changes before opening?",
                                      QMessageBox.Discard,QMessageBox.Save)
    elif self.toolboxStuff.dataManagerTree and self.toolboxStuff.dataManagerTree.model.dirty:
      saveBeforeOpen = QMessageBox.question(self,"Warning",
                                      "Current project contains changes... \nShould we save or discard those changes before opening?",
                                      QMessageBox.Discard,QMessageBox.Save)

    if saveBeforeOpen == QMessageBox.Save:
      self.saveConfig()
    else:
      #if we have an existing tree we need to remove the dirty bit since we are discarding
      if self.toolboxStuff.runManagerTree:
        self.toolboxStuff.runManagerTree.model.dirty = False
      if self.toolboxStuff.dataManagerTree:
        self.toolboxStuff.dataManagerTree.model.dirty = False
      if self.toolboxStuff.modelManagerTree:
        self.toolboxStuff.modelManagerTree.model.dirty = False
      if self.toolboxStuff.resultsManagerTree:
        self.toolboxStuff.resultsManagerTree.model.dirty = False

    from opus_core.misc import directory_path_from_opus_path
    start_dir = directory_path_from_opus_path('opus_gui.projects')
    #print "Open Config pressed..."
    configDialog = QFileDialog()
    filter_str = QString("*.xml")
    fd = configDialog.getOpenFileName(self,QString("Please select an xml config file..."),
                                      QString(start_dir), filter_str)
    # Check for cancel
    if len(fd) == 0:
      return
    fileName = QString(fd)
    fileNameInfo = QFileInfo(QString(fd))
    fileNameBaseName = fileNameInfo.completeBaseName()
    #print "Filename = ", fileName
    # Open the file and add to the Run tab...
    self.toolboxStuff.openXMLTree(fileName)

  def saveConfig(self):
    #print "Save Config pressed..."
    configFile = self.toolboxStuff.runManagerTree.model.configFile
    domDocument = self.toolboxStuff.runManagerTree.model.domDocument
    indentSize = 2
    configFile.close()
    configFile.open(QIODevice.ReadWrite | QIODevice.Truncate)
    out = QTextStream(configFile)
    domDocument.save(out, indentSize)
    self.toolboxStuff.runManagerTree.model.dirty = False
    self.toolboxStuff.runManagerTree.groupBox.setTitle(QFileInfo(self.toolboxStuff.runManagerTree.parentTool.xml_file).filePath())
    self.toolboxStuff.dataManagerTree.model.dirty = False
    self.toolboxStuff.dataManagerTree.groupBox.setTitle(QFileInfo(self.toolboxStuff.dataManagerTree.parentTool.xml_file).filePath())
    self.toolboxStuff.modelManagerTree.model.dirty = False
    self.toolboxStuff.modelManagerTree.groupBox.setTitle(QFileInfo(self.toolboxStuff.modelManagerTree.parentTool.xml_file).filePath())
    self.toolboxStuff.resultsManagerTree.model.dirty = False
    self.toolboxStuff.resultsManagerTree.groupBox.setTitle(QFileInfo(self.toolboxStuff.resultsManagerTree.parentTool.xml_file).filePath())
    #print "Save Config finished..."

  def saveConfigAs(self):
    print "Save Config As is not implemented yet..."
    #qd = QFileDialog()
    #filter_str = QString("*.xml")
    #f2=qd.getSaveFileName(self,QString(),QString(),filter_str)
    #if f2.count(".xml")==0:
    #  f = f2 + ".xml"
    #else:
    #  f = f2
    #write_string = QString(f)
    #configFile = QFile(write_string)
    #domDocument = self.toolboxStuff.runManagerTree.model.domDocument
    #indentSize = 2
    #configFile.open(QIODevice.ReadWrite | QIODevice.Truncate)
    #out = QTextStream(configFile)
    #domDocument.save(out, indentSize)
    #self.toolboxStuff.runManagerTree.model.dirty = False
    #self.toolboxStuff.dataManagerTree.model.dirty = False
    #self.toolboxStuff.modelManagerTree.model.dirty = False
    #self.toolboxStuff.resultsManagerTree.model.dirty = False
    ##### TODO - Now need to close existing project and re-open the newly
    ##### saved one...

  def exitOpus(self):
    print "Exit pressed..."
    saveBeforeClose = QMessageBox.Discard
    if self.toolboxStuff.resultsManagerTree and self.toolboxStuff.resultsManagerTree.model.dirty:
      saveBeforeClose = QMessageBox.question(self,"Warning",
                                      "Current project contains changes... \nShould we save or discard those changes before closing?",
                                      QMessageBox.Discard,QMessageBox.Save)
    elif self.toolboxStuff.modelManagerTree and self.toolboxStuff.modelManagerTree.model.dirty:
      saveBeforeClose = QMessageBox.question(self,"Warning",
                                      "Current project contains changes... \nShould we save or discard those changes before closing?",
                                      QMessageBox.Discard,QMessageBox.Save)
    elif self.toolboxStuff.runManagerTree and self.toolboxStuff.runManagerTree.model.dirty:
      saveBeforeClose = QMessageBox.question(self,"Warning",
                                      "Current project contains changes... \nShould we save or discard those changes before closing?",
                                      QMessageBox.Discard,QMessageBox.Save)
    elif self.toolboxStuff.dataManagerTree and self.toolboxStuff.dataManagerTree.model.dirty:
      saveBeforeClose = QMessageBox.question(self,"Warning",
                                      "Current project contains changes... \nShould we save or discard those changes before closing?",
                                      QMessageBox.Discard,QMessageBox.Save)

    if saveBeforeClose == QMessageBox.Save:
      self.saveConfig()

    self.close()
