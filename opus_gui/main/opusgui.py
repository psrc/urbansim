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

from opus_gui.config.xmlmodelview.opusallvariablestablemodel import OpusAllVariablesTableModel

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
        self.setWindowTitle(self.application_title)

        self.splitter.setSizes([400,500])

        # Play with the project and config load/save
        QObject.connect(self.actionOpen_Project_2, SIGNAL("triggered()"), self.openConfig)
        QObject.connect(self.actionSave_Project_2, SIGNAL("triggered()"), self.saveConfig)
        QObject.connect(self.actionClose_Project, SIGNAL("triggered()"), self.closeConfig)
        QObject.connect(self.actionSave_Project_As_2, SIGNAL("triggered()"), self.saveConfigAs)
        # Exit
        QObject.connect(self.actionExit, SIGNAL("triggered()"), self.close)
        # About
        QObject.connect(self.actionAbout, SIGNAL("triggered()"), self.openAbout)

        # Model System menus
        QObject.connect(self.actionEdit_all_variables, SIGNAL("triggered()"), self.editAllVariables)
        self.allVariablesWidget = QWidget(self)
        self.allVariablesWidgetLayout = QVBoxLayout(self.allVariablesWidget)
        self.allVariablesWidgetLayout.setAlignment(Qt.AlignTop)
        self.allVariablesGroupBox = QGroupBox(self)
        self.allVariablesGroupBoxLayout = QVBoxLayout(self.allVariablesGroupBox)
        #Add a default table
        tv = QTableView()
        header = ["Name","Vlaue"]
        tabledata = [("","")]
        tm = OpusAllVariablesTableModel(tabledata, header, self.allVariablesWidget) 
        tv.setModel(tm)
        tv.setSortingEnabled(True)
        self.allVariablesGroupBoxLayout.addWidget(tv)
        self.allVariablesWidgetLayout.addWidget(self.allVariablesGroupBox)
        self.allVariablesWidget.hide()
        
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

        # This stuff adds the 'X' button for closing tabs
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
        
    def editAllVariables(self):
        #print "Edit all_variables pressed..."
        if self.tabWidget.indexOf(self.allVariablesWidget) == -1:
            tabIcon = QIcon(":/Images/Images/cog.png")
            tabLabel = QString("all_variables")
            self.tabWidget.insertTab(0,self.allVariablesWidget,tabIcon,tabLabel)
            self.tabWidget.setCurrentIndex(0)

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

    def openConfig(self, config=None):
        # config should be a path to an .xml config file

        # Check to see if there are changes to the current project, if a project is open
        self._saveOrDiscardChanges()

        if config:
            self.toolboxStuff.openXMLTree(config)
            # Add the project file's path to the title bar
            self.setWindowTitle(self.application_title + " - " + QFileInfo(self.toolboxStuff.runManagerTree.parentTool.xml_file).filePath())
        else:
            import os
            start_dir = ''
            opus_home = os.environ.get('OPUS_HOME')
            if opus_home:
                start_dir_test = os.path.join(opus_home, 'project_configs')
                if start_dir_test:
                    start_dir = start_dir_test
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
            # Add the project file's path to the title bar
            self.setWindowTitle(self.application_title + " - " + QFileInfo(self.toolboxStuff.runManagerTree.parentTool.xml_file).filePath())
            self.resultManagerStuff.scan_for_runs()

    def saveConfig(self):
        try:
            domDocument = self.toolboxStuff.doc
            opusXMLTree = self.toolboxStuff.opusXMLTree
            indentSize = 2
            opusXMLTree.update(str(domDocument.toString(indentSize)))
            opusXMLTree.save()
            self.toolboxStuff.runManagerTree.model.markAsClean()
            self.toolboxStuff.dataManagerTree.model.markAsClean()
            self.toolboxStuff.dataManagerDBSTree.model.markAsClean()
            self.toolboxStuff.modelManagerTree.model.markAsClean()
            self.toolboxStuff.resultsManagerTree.model.markAsClean()
            self.toolboxStuff.generalManagerTree.model.markAsClean()
        except:
            print "Unexpected error:", sys.exc_info()[0]

    def saveConfigAs(self):
        try:
            # get the location for the new config file on disk
            from opus_core.misc import directory_path_from_opus_path
            start_dir = directory_path_from_opus_path('opus_gui.projects')
            configDialog = QFileDialog()
            filter_str = QString("*.xml")
            fd = configDialog.getSaveFileName(self,QString("Save As..."),
                                              QString(start_dir), filter_str)
            # Check for cancel
            if len(fd) == 0:
                return
            fileName = QString(fd)

            domDocument = self.toolboxStuff.doc
            opusXMLTree = self.toolboxStuff.opusXMLTree
            indentSize = 2
            opusXMLTree.update(str(domDocument.toString(indentSize)))
            opusXMLTree.save_as(str(fileName))
            self.toolboxStuff.runManagerTree.model.markAsClean()
            self.toolboxStuff.dataManagerTree.model.markAsClean()
            self.toolboxStuff.dataManagerDBSTree.model.markAsClean()
            self.toolboxStuff.modelManagerTree.model.markAsClean()
            self.toolboxStuff.resultsManagerTree.model.markAsClean()
            self.toolboxStuff.generalManagerTree.model.markAsClean()
        except:
            print "Unexpected error:", sys.exc_info()[0]

    def _saveOrDiscardChanges(self):
        """
        Checks for changes to the currently open project (if any)
        and prompts user to save or discard changes.
        """
        saveBeforeOpen = QMessageBox.Discard
        if self.toolboxStuff.resultsManagerTree and self.toolboxStuff.resultsManagerTree.model.isDirty():
            saveBeforeOpen = QMessageBox.question(self,"Warning",
                                            "Current project contains changes... \nShould we save or discard those changes?",
                                            QMessageBox.Discard,QMessageBox.Save)
        elif self.toolboxStuff.modelManagerTree and self.toolboxStuff.modelManagerTree.model.isDirty():
            saveBeforeOpen = QMessageBox.question(self,"Warning",
                                            "Current project contains changes... \nShould we save or discard those changes?",
                                            QMessageBox.Discard,QMessageBox.Save)
        elif self.toolboxStuff.runManagerTree and self.toolboxStuff.runManagerTree.model.isDirty():
            saveBeforeOpen = QMessageBox.question(self,"Warning",
                                            "Current project contains changes... \nShould we save or discard those changes?",
                                            QMessageBox.Discard,QMessageBox.Save)
        elif self.toolboxStuff.dataManagerTree and self.toolboxStuff.dataManagerTree.model.isDirty():
            saveBeforeOpen = QMessageBox.question(self,"Warning",
                                            "Current project contains changes... \nShould we save or discard those changes?",
                                            QMessageBox.Discard,QMessageBox.Save)
        elif self.toolboxStuff.dataManagerDBSTree and self.toolboxStuff.dataManagerDBSTree.model.isDirty():
            saveBeforeOpen = QMessageBox.question(self,"Warning",
                                            "Current project contains changes... \nShould we save or discard those changes?",
                                            QMessageBox.Discard,QMessageBox.Save)
        elif self.toolboxStuff.generalManagerTree and self.toolboxStuff.generalManagerTree.model.isDirty():
            saveBeforeOpen = QMessageBox.question(self,"Warning",
                                            "Current project contains changes... \nShould we save or discard those changes?",
                                            QMessageBox.Discard,QMessageBox.Save)

        if saveBeforeOpen == QMessageBox.Save:
            self.saveConfig()
        else:
            #if we have an existing tree we need to remove the dirty bit since we are discarding
            if self.toolboxStuff.runManagerTree:
                self.toolboxStuff.runManagerTree.model.markAsClean()
            if self.toolboxStuff.dataManagerTree:
                self.toolboxStuff.dataManagerTree.model.markAsClean()
            if self.toolboxStuff.dataManagerDBSTree:
                self.toolboxStuff.dataManagerDBSTree.model.markAsClean()
            if self.toolboxStuff.modelManagerTree:
                self.toolboxStuff.modelManagerTree.model.markAsClean()
            if self.toolboxStuff.resultsManagerTree:
                self.toolboxStuff.resultsManagerTree.model.markAsClean()
            if self.toolboxStuff.generalManagerTree:
                self.toolboxStuff.generalManagerTree.model.markAsClean()

    def closeConfig(self):
        """
        Closes the current project, if one is open.
        """

        try:
            configFile = self.toolboxStuff.runManagerTree.model.configFile
        except:
            pass

        # Check to see if there are changes to the current project, if a project is open
        self._saveOrDiscardChanges()
        self.toolboxStuff.closeXMLTree()
        self.setWindowTitle(self.application_title)

    def closeEvent(self, event):
        # Check to see if there are changes to the current project, if a project is open
        self._saveOrDiscardChanges()
        # Save application geometry on shut down
        settings = QSettings()
        settings.setValue("Geometry", QVariant(self.saveGeometry()))


