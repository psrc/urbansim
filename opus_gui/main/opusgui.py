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
from opus_gui.main.opusmain_ui import Ui_MainWindow
from opus_gui.main.opusabout import UrbansimAboutGui

from opus_gui.util.consolebase import *
from opus_gui.config.toolboxbase import *
from opus_gui.run.runmanagerbase import *
from opus_gui.results.resultManagerBase import *
from opus_gui.results.xml_helper_methods import get_child_values

# General system includes
import sys,time,tempfile


# Main window used for houseing the canvas, toolbars, and dialogs
class OpusGui(QMainWindow, Ui_MainWindow):

  def __init__(self):
    QMainWindow.__init__(self)

    # required by Qt4 to initialize the UI
    self.setupUi(self)
    
    self.toolboxStuff = ToolboxBase(self)
    
    # Loading startup options from gui configuration xml file
    startup_node = self.toolboxStuff.gui_configuration_doc.elementsByTagName('startup_options').item(0)
    splash_pix = get_child_values(parent = startup_node, 
                             child_names = ['splash_logo'])
    
    splash_pix = os.path.join('main','Images',str(splash_pix['splash_logo']))
    self.splashPix = QPixmap(QString(splash_pix))
    self.splashPixScaled = self.splashPix.scaled(600,252,Qt.KeepAspectRatio)
    self.splash = QSplashScreen(self.splashPixScaled)
    self.splash.show()
    
    # Loading main window title from gui configuration xml file
    application_options_node = self.toolboxStuff.gui_configuration_doc.elementsByTagName('application_options').item(0)
    application_title_dict = get_child_values(parent = application_options_node,
                                         child_names = ['application_title'])
    self.application_title = application_title_dict['application_title']
    self.setWindowTitle(application_title_dict['application_title'])

    # Play with the project and config load/save
    QObject.connect(self.actionOpen_Project_2, SIGNAL("triggered()"), self.openConfig)
    QObject.connect(self.actionSave_Project_2, SIGNAL("triggered()"), self.saveConfig)
    QObject.connect(self.actionSave_Project_As_2, SIGNAL("triggered()"), self.saveConfigAs)
    # Exit
    QObject.connect(self.actionExit, SIGNAL("triggered()"), self.exitOpus)
    # About
    QObject.connect(self.actionAbout, SIGNAL("triggered()"), self.openAbout)
    
    # QGIS References are removed for the time being...
    #Add map tab
    #QObject.connect(self.actionMap_View, SIGNAL("triggered()"), self.openMapTab)
    
    #Add editor tab
    QObject.connect(self.actionEditor_View, SIGNAL("triggered()"), self.openEditorTab)
    #Add python tab
    QObject.connect(self.actionPython_View, SIGNAL("triggered()"), self.openPythonTab)
    #Add log tab
    QObject.connect(self.actionLog_View, SIGNAL("triggered()"), self.openLogTab)

    self.tempDir = tempfile.mkdtemp(prefix='opus_gui')

    # QGIS References are removed for the time being...
    #try:
    #  import qgis.core
    #  import map.mapbase
    #  # Only load the map stuff if QGIS is loadable
    #  self.mapStuff = map.mapbase.MapBase(self)
    #except ImportError:
    #  self.mapStuff = None

    self.consoleStuff = ConsoleBase(self)
    self.runManagerStuff = RunManagerBase(self)
    self.runManagerStuff.setGui(self)

    self.resultManagerStuff = ResultManagerBase(self)
    self.resultManagerStuff.setGui(self)

    try:
      import opus_gui.util.editorbase
      self.editorStatusLabel = QLabel(self)
      self.editorStatusLabel.setAlignment(Qt.AlignCenter)
      self.editorStatusLabel.setObjectName("editorStatusLabel")
      self.editorStatusLabel.setText(QString("No files currently loaded..."))
      self.tab_editorView.layout().addWidget(self.editorStatusLabel)
      self.editorStuff = opus_gui.util.editorbase.EditorBase(self)
      self.tab_editorView.layout().addWidget(self.editorStuff)
    except ImportError:
      self.editorStuff = None

    time.sleep(1)
    self.splash.hide()

    self.actionCloseCurrentTab = QAction(self)
    self.actionCloseCurrentTab.setIcon(QIcon(":/Images/Images/cross.png"))
    self.actionCloseCurrentTab.setObjectName("actionCloseCurrentTab")
    self.tabCornerWidget = QToolButton()
    self.tabCornerWidget.setDefaultAction(self.actionCloseCurrentTab)
    self.tabCornerWidget.setWhatsThis(QString("Close Current Tab"))
    self.tabCornerWidget.setToolTip(QString("Close Current Tab"))
    self.tabWidget.setCornerWidget(self.tabCornerWidget)
    QObject.connect(self.actionCloseCurrentTab,
                    SIGNAL("triggered()"), self.closeCurrentTab)
    
    # Restoring application geometry from last shut down
    settings = QSettings()
    self.restoreGeometry(settings.value("Geometry").toByteArray())
    
    


  def closeCurrentTab(self):
    widget = self.tabWidget.currentWidget()
    self.tabWidget.removeTab(self.tabWidget.currentIndex())
    try:
      widget.hide()
    except:
      pass
    # Do something with the widget if we need to...

  def openMapTab(self):
    if self.tabWidget.indexOf(self.tab_mapView) == -1:
      self.tab_mapView.show()
      self.tabWidget.insertTab(0,self.tab_mapView,
                               QIcon(":/Images/Images/map.png"),"Map View")
      self.tabWidget.setCurrentWidget(self.tab_mapView)

  def openPythonTab(self):
    if self.tabWidget.indexOf(self.tab_pythonView) == -1:
      self.tab_pythonView.show()
      self.tabWidget.insertTab(0,self.tab_pythonView,
                               QIcon(":/Images/Images/python_type.png"),"Python Console")
      self.tabWidget.setCurrentWidget(self.tab_pythonView)

  def openEditorTab(self):
    if self.tabWidget.indexOf(self.tab_editorView) == -1:
      self.tab_editorView.show()
      self.tabWidget.insertTab(0,self.tab_editorView,
                               QIcon(":/Images/Images/table.png"),"Editor View")
      self.tabWidget.setCurrentWidget(self.tab_editorView)

  def openLogTab(self):
    if self.tabWidget.indexOf(self.tab_logView) == -1:
      self.tab_logView.show()
      self.tabWidget.insertTab(0,self.tab_logView,
                               QIcon(":/Images/Images/folder.png"),"Log View")
      self.tabWidget.setCurrentWidget(self.tab_logView)

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
    # Open the file and add to the Run tab...
    self.toolboxStuff.openXMLTree(fileName)
    # Jesse
    self.setWindowTitle(self.application_title + " - " + QFileInfo(self.toolboxStuff.runManagerTree.parentTool.xml_file).filePath())

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
    self.setWindowTitle(self.windowTitle().replace("*", ""))
    self.toolboxStuff.dataManagerTree.model.dirty = False
    self.setWindowTitle(self.windowTitle().replace("*", ""))
    self.toolboxStuff.dataManagerDBSTree.model.dirty = False
    self.setWindowTitle(self.windowTitle().replace("*", ""))
    self.toolboxStuff.modelManagerTree.model.dirty = False
    self.setWindowTitle(self.windowTitle().replace("*", ""))
    self.toolboxStuff.resultsManagerTree.model.dirty = False
    self.setWindowTitle(self.windowTitle().replace("*", ""))
    #print "Save Config finished..."

  def saveConfigAs(self):
    print "Save Config As is not implemented yet..."

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

  def closeEvent(self, event):
    # Saving application geometry on shut down
    settings = QSettings()
    settings.setValue("Geometry", QVariant(self.saveGeometry()))
    
    
