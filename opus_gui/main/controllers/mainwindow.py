# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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
from PyQt4.QtCore import Qt, QVariant, QThread, QString, QObject, SIGNAL , QFile, QSettings, QRegExp, QFileInfo
from PyQt4.QtGui import QSpinBox, QMenu, QMainWindow, QPixmap, QMessageBox, QSplashScreen, QLabel, \
     QWidget, QPushButton, QHBoxLayout, QAction, QFileDialog, QToolButton, QIcon
from PyQt4.QtXml import QDomDocument

# UI specific includes
from opus_gui.main.views.ui_mainwindow import Ui_MainWindow
from opus_gui.main.controllers.dialogs.opusabout import UrbansimAboutGui
from opus_gui.main.controllers.dialogs.opuspreferences import UrbansimPreferencesGui
from opus_gui.main.controllers.dialogs.databasesettings import DatabaseSettingsEditGui
from opus_gui.main.controllers.toolboxbase import ToolboxBase

#from opus_gui.util.consolebase import ConsoleBase

from opus_gui.scenarios_manager.scenario_manager_base import ScenariosManagerBase
from opus_gui.results_manager.results_manager_base import ResultsManagerBase
from opus_gui.models_manager.models_manager_base import ModelsManagerBase

from opus_gui.results_manager.xml_helper_methods import get_child_values
from opus_gui.util.exception_formatter import formatExceptionInfo

from opus_gui.general_manager.controllers.all_variables import AllVariablesEditGui

# General system includes
import time, tempfile, os


# Main window used for houseing the canvas, toolbars, and dialogs
class OpusGui(QMainWindow, Ui_MainWindow):

    # This is the output override for the app to catch stdout and stderr and
    # placing it in the log tab
    class Output:
        def __init__( self, writefunc ):
            self.writefunc = writefunc
        def write( self, line ):
            if line != "\n":
                self.writefunc(line)

    def __init__(self):
        QMainWindow.__init__(self)

        # required by Qt4 to initialize the UI
        self.setupUi(self)
        for i in range(2,-1,-1):
            self.tabWidget.removeTab(i)
        
        self.thread().setPriority(QThread.HighestPriority)

        # This is the output for stdout
        self.output = OpusGui.Output(self.writeOutput)
        #sys.stdout, sys.stderr = self.output, self.output

        self.toolboxBase = ToolboxBase(self)

        # Loading startup options from gui configuration xml file
        startup_node = self.toolboxBase.gui_configuration_doc.elementsByTagName('startup_options').item(0)
        splash_pix = get_child_values(parent = startup_node, 
                                 child_names = ['splash_logo'])

        splash_pix = os.path.join('main','views','Images',str(splash_pix['splash_logo']))
        self.splashPix = QPixmap(QString(splash_pix))
        self.splashPixScaled = self.splashPix.scaled(600,252,Qt.KeepAspectRatio)
        self.splash = QSplashScreen(self.splashPixScaled)
        self.splash.show()

        # Loading main window title from gui configuration xml file
        application_options_node = self.toolboxBase.gui_configuration_doc.elementsByTagName('application_options').item(0)
        application_title_dict = get_child_values(parent = application_options_node,
                                             child_names = ['application_title'])
        self.application_title = application_title_dict['application_title']
        # self.setWindowTitle(self.application_title)
        self.updateWindowTitle()

        # Loading settings from gui configuration xml file regarding font sizes
        try:
            #font settings
            font_settings_node = self.toolboxBase.gui_configuration_doc.elementsByTagName('font_settings').item(0)
            
            self.menu_font_size = int(get_child_values(parent = font_settings_node,
                                              child_names = ['menu_font_size'])['menu_font_size'])
            self.main_tabs_font_size = int(get_child_values(parent = font_settings_node,
                                              child_names = ['main_tabs_font_size'])['main_tabs_font_size'])
            self.general_text_font_size = int(get_child_values(parent = font_settings_node,
                                              child_names = ['general_text_font_size'])['general_text_font_size'])
            
            
        except:
            #font settings
            self.toolboxBase.reemit_reinit_default_gui_configuration_file()
            font_settings_node = self.toolboxBase.gui_configuration_doc.elementsByTagName('font_settings').item(0)
            
            self.menu_font_size = int(get_child_values(parent = font_settings_node,
                                              child_names = ['menu_font_size'])['menu_font_size'])
            self.main_tabs_font_size = int(get_child_values(parent = font_settings_node,
                                              child_names = ['main_tabs_font_size'])['main_tabs_font_size'])
            self.general_text_font_size = int(get_child_values(parent = font_settings_node,
                                              child_names = ['general_text_font_size'])['general_text_font_size'])
        
        #loading settings from gui xml regarding previous project   
        try:
            prev_proj_node = self.toolboxBase.gui_configuration_doc.elementsByTagName('project_history').item(0)
            self.latest_project_file_name = QString(get_child_values(parent = prev_proj_node,
                                              child_names = ['previous_project'])['previous_project'])
            self.open_latest_project = "True" == str(get_child_values(parent = prev_proj_node,
                                              child_names = ['open_latest_project_on_start'])['open_latest_project_on_start'])
        except:
            self.latest_project_file_name = ' '
            self.open_latest_project = False
            self.toolboxBase.reemit_reinit_default_gui_configuration_file()
            self.updateFontSettingsNode()
            self.saveGuiConfig()
            
        self.splitter.setSizes([400,500])

        self.actionOpen_Project_2.setShortcut(QString('Ctrl+O'))
        self.actionSave_Project_2.setShortcut(QString('Ctrl+S'))
        self.actionSave_Project_As_2.setShortcut(QString('Ctrl+Shift+S'))
        self.actionClose_Project.setShortcut(QString('Ctrl+W'))
        self.actionEdit_all_variables.setShortcut(QString('Ctrl+V'))
        self.actLaunchResultBrowser.setShortcut(QString('Ctrl+R'))
        self.actionDatabaseSettings.setShortcut(QString('Ctrl+D'))
        self.actionPreferences.setShortcut(QString('Ctrl+P'))
        
        # Play with the project and config load/save
        QObject.connect(self.actionOpen_Project_2, SIGNAL("triggered()"), self.openConfig)
        QObject.connect(self.actionSave_Project_2, SIGNAL("triggered()"), self.saveConfig)
        QObject.connect(self.actionClose_Project, SIGNAL("triggered()"), self.closeConfig)
        QObject.connect(self.actionSave_Project_As_2, SIGNAL("triggered()"), self.saveConfigAs)
        # Exit
        QObject.connect(self.actionExit, SIGNAL("triggered()"), self.close)
        # About
        QObject.connect(self.actionAbout, SIGNAL("triggered()"), self.openAbout)
        # Preferences
        QObject.connect(self.actionPreferences, SIGNAL("triggered()"), self.openPreferences)
        # Database Settings
        QObject.connect(self.actionDatabaseSettings, SIGNAL("triggered()"), self.openDatabaseSettings)
        
        # Model System menus
        QObject.connect(self.actionEdit_all_variables, SIGNAL("triggered()"), self.editAllVariables)
        self.actionEdit_all_variables.setEnabled(False)
        self.actLaunchResultBrowser.setEnabled(False)
        
        # QGIS References are removed for the time being...
        #Add map tab
        #QObject.connect(self.actionMap_View, SIGNAL("triggered()"), self.openMapTab)

        #Add editor tab
        QObject.connect(self.actionEditor_View, SIGNAL("triggered()"), self.openEditorTab)
        #Add python tab
        QObject.connect(self.actionPython_View, SIGNAL("triggered()"), self.openPythonTab)
        #Add result browser tab
        QObject.connect(self.actLaunchResultBrowser, SIGNAL("triggered()"), self.openResultBrowser)
        #Add log tab
        QObject.connect(self.actionLog_View, SIGNAL("triggered()"), self.openLogTab)
        
#        QObject.connect(self.tabWidget, SIGNAL("currentChanged(int)"), self.tab_changed)

        self.tempDir = tempfile.mkdtemp(prefix='opus_gui')

        # QGIS References are removed for the time being...
        #try:
        #  import qgis.core
        #  import map.mapbase
        #  # Only load the map stuff if QGIS is loadable
        #  self.mapStuff = map.mapbase.MapBase(self)
        #except ImportError:
        #  self.mapStuff = None

#        self.consoleStuff = ConsoleBase(self)
        self.scenariosManagerBase = ScenariosManagerBase(self)
        self.scenariosManagerBase.setGui(self)

        self.resultsManagerBase = ResultsManagerBase(self)
        self.resultsManagerBase.setGui(self)
        
        self.modelsManagerBase = ModelsManagerBase(self)
        self.modelsManagerBase.setGui(self)

        try:
            import opus_gui.util.editorbase
            self.editorStatusLabel = QLabel(self)
            self.editorStatusLabel.setAlignment(Qt.AlignCenter)
            self.editorStatusLabel.setObjectName("editorStatusLabel")
            self.editorStatusLabel.setText(QString(" - No files currently loaded..."))
            self.tab_editorView.layout().addWidget(self.editorStatusLabel)
            self.editorStuff = opus_gui.util.editorbase.EditorBase(self)
            self.tab_editorView.layout().addWidget(self.editorStuff)
            # Some buttons to control open,save,saveas,close
            # First the container and layout
            self.editorButtonWidget = QWidget(self)
            self.editorButtonWidgetLayout = QHBoxLayout(self.editorButtonWidget)
            # Make it center justified

            # Now we add the buttons
            # Open File
            self.editorOpenFileButton = QPushButton(self.editorButtonWidget)
            self.editorOpenFileButton.setObjectName("editorOpenFileButton")
            self.editorOpenFileButton.setText(QString("Open File"))
            QObject.connect(self.editorOpenFileButton, SIGNAL("released()"),
                            self.editorOpenFileButton_released)        
            self.editorButtonWidgetLayout.addWidget(self.editorOpenFileButton)
            # Save File
            self.editorSaveFileButton = QPushButton(self.editorButtonWidget)
            self.editorSaveFileButton.setObjectName("editorSaveFileButton")
            self.editorSaveFileButton.setText(QString("Save File"))
            QObject.connect(self.editorSaveFileButton, SIGNAL("released()"),
                            self.editorSaveFileButton_released)        
            self.editorButtonWidgetLayout.addWidget(self.editorSaveFileButton)
            # Save As File
            self.editorSaveAsFileButton = QPushButton(self.editorButtonWidget)
            self.editorSaveAsFileButton.setObjectName("editorSaveAsFileButton")
            self.editorSaveAsFileButton.setText(QString("Save File As"))
            # Gray out for now until implemented
            self.editorSaveAsFileButton.setDisabled(True)
            QObject.connect(self.editorSaveAsFileButton, SIGNAL("released()"),
                            self.editorSaveAsFileButton_released)        
            self.editorButtonWidgetLayout.addWidget(self.editorSaveAsFileButton)
            self.tab_editorView.layout().addWidget(self.editorButtonWidget)
            QObject.connect(self.editorStuff, SIGNAL("textChanged()"),
                            self.editorStuffTextChanged)        
            self.editorDirty = False

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
        self.changeFontSize()
        self.setFocus()

        self.all_variables = None
                
        if os.path.exists(self.latest_project_file_name) and self.open_latest_project:
            self.openConfig(self.latest_project_file_name)
        
        ###T: removing these until they serve a purpose
        self.menuUtilities.removeAction(self.actionPython_View)
        #self.menuUtilities.removeAction(self.actionLog_View)
        self.menuUtilities.removeAction(self.actionEditor_View)

        
    def getDbConnectionNames(self):
        '''
        Returns a list of the names of database connections available in the
        database_server_configurations.xml document
        '''
        settings_directory = os.path.join(os.environ['OPUS_HOME'], 'settings')
        database_server_configuration_file = os.path.join(settings_directory, 'database_server_configurations.xml')
        configFile = QFile(database_server_configuration_file)
        doc = QDomDocument()
        doc.setContent(configFile)

        list_of_db_connections = []
        for i in range(0, doc.documentElement().childNodes().length()):
            db_connection_name = doc.documentElement().childNodes().item(i).nodeName()
            if db_connection_name != '#comment':
                list_of_db_connections.append(str(db_connection_name))
        return list_of_db_connections

    def writeOutput(self,result):
        if result == "":
            return
        self.logViewTextBrowser.append(result)

    def editAllVariables(self):
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        self.all_variables = AllVariablesEditGui(self,flags)
        
        self.all_variables.setModal(True)
        self.all_variables.show()
            
    def closeCurrentTab(self):
        widget = self.tabWidget.currentWidget()

        if widget in self.resultsManagerBase.guiElements:
            self.resultsManagerBase.removeGuiElement(guiElement = widget)
        elif widget in self.modelsManagerBase.guiElements:
            self.resultsManagerBase.removeGuiElement(guiElement = widget)
        elif widget in self.scenariosManagerBase.guiElements:
            self.resultsManagerBase.removeGuiElement(guiElement = widget)
        else: 
            self.tabWidget.removeTab(self.tabWidget.currentIndex())
        try:
            widget.hide()
        except:
            pass
        # Do something with the widget if we need to...
        
        


    def openMapTab(self):
        if self.tabWidget.indexOf(self.tab_mapView) == -1:
            self.tab_mapView.show()
            self.changeFontSize()
            self.tabWidget.insertTab(0,self.tab_mapView,
                                     QIcon(":/Images/Images/map.png"),"Map View")
            self.tabWidget.setCurrentWidget(self.tab_mapView)


    def openPythonTab(self):
        if self.tabWidget.indexOf(self.tab_pythonView) == -1:
            self.tab_pythonView.show()
            self.changeFontSize()
            self.tabWidget.insertTab(0,self.tab_pythonView,
                                     QIcon(":/Images/Images/python_type.png"),"Python Console")
            self.tabWidget.setCurrentWidget(self.tab_pythonView)

    def openResultBrowser(self):
        self.resultsManagerBase.add_result_browser()
        
    def openEditorTab(self):
        if self.tabWidget.indexOf(self.tab_editorView) == -1:
            self.tab_editorView.show()
            self.changeFontSize()
            self.tabWidget.insertTab(0,self.tab_editorView,
                                     QIcon(":/Images/Images/table_lightning.png"),"Editor View")
            self.tabWidget.setCurrentWidget(self.tab_editorView)
        

    def openLogTab(self):
        if self.tabWidget.indexOf(self.tab_logView) == -1:
            self.tab_logView.show()
            self.changeFontSize()
            self.tabWidget.insertTab(0,self.tab_logView,
                                     QIcon(":/Images/Images/table.png"),"Log View")
            self.tabWidget.setCurrentWidget(self.tab_logView)
        


    def openAbout(self):
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        wnd = UrbansimAboutGui(self,flags)
        wnd.setModal(True)
        wnd.show()
        self.changeFontSize()

    def openPreferences(self):
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        wnd = UrbansimPreferencesGui(self, flags)
        wnd.setModal(True)
        wnd.show()
        self.changeFontSize()
    
    def openDatabaseSettings(self):
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        #wnd = UrbansimDatabaseSettingsGUI(self, flags)
        # Commented out the previous line and added the following line
        # to test out the APR added database connection editing GUI (082908)
        wnd = DatabaseSettingsEditGui(self, flags)
        wnd.setModal(True)
        wnd.setWindowTitle('Database Server Connections')
        wnd.show()
        self.changeFontSize()
        
    def updateWindowTitle(self):
        '''update the window title to reflect the state of the project'''
        # assemble a title consisting of file name and project name
        app_name = self.application_title
        proj_name = self.toolboxBase.project_name
        file_name  = self.toolboxBase.xml_file
        dirty_flag = self.toolboxBase.projectIsDirty()

        if file_name is not None:
            file_name = file_name.split(os.sep)[-1]
        title = app_name # default to only app name
        if proj_name: # proj_name is None when no project is loaded
            if dirty_flag:
                title = '%s - (*) %s - [file: %s]' %(app_name, proj_name, file_name)
            else:
                title = '%s - %s - [file: %s]' %(app_name, proj_name, file_name)
        self.setWindowTitle(title)
    
    def openConfig(self, config=None):
        # config should be a path to an .xml config file

        # Check to see if there are changes to the current project, if a project is open
        self._saveOrDiscardChanges()

        if config: # open the configuration file
            self.toolboxBase.openXMLTree(config)

        else: # show open config dialog box
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
            config = QString(fd)
            fileNameInfo = QFileInfo(QString(fd))
            fileNameBaseName = fileNameInfo.completeBaseName()
            # Open the file and add to the Run tab...
            self.toolboxBase.openXMLTree(config)

        # update latest project config
        self.latest_project_file_name = config
        self.updateProjectHistoryNode()
        self.saveGuiConfig()

        self.resultsManagerBase.scanForRuns()    
        self.actLaunchResultBrowser.setEnabled(True)
        self.actionEdit_all_variables.setEnabled(True)
        
        self.scenariosManagerBase.removeAllElements()
        self.resultsManagerBase.removeAllElements()
        self.modelsManagerBase.removeAllElements()

        if self.all_variables is not None:
            self.all_variables.close()

        self.actionClose_Project.setEnabled(True)
        self.actionSave_Project_2.setEnabled(True)
        self.actionSave_Project_As_2.setEnabled(True)
        self.changeFontSize()

        self.updateWindowTitle()

    def saveConfig(self):
        try:
            domDocument = self.toolboxBase.doc
            opus_core_xml_configuration = self.toolboxBase.opus_core_xml_configuration
            indentSize = 2
            
            data = str(domDocument.toString(indentSize))

            opus_core_xml_configuration.update(data)
            opus_core_xml_configuration.save()
            self.toolboxBase.runManagerTree.model.markAsClean()
            self.toolboxBase.dataManagerTree.model.markAsClean()
            if self.toolboxBase.dataManagerDBSTree is not None:
                self.toolboxBase.dataManagerDBSTree.model.markAsClean()
            self.toolboxBase.modelManagerTree.model.markAsClean()
            self.toolboxBase.resultsManagerTree.model.markAsClean()
            self.toolboxBase.generalManagerTree.model.markAsClean()
        except:
            errorMessage = formatExceptionInfo(custom_message = 'Unexpected error saving config')
            QMessageBox.warning(self, 'Warning', errorMessage) 

    def saveConfigAs(self):
        try:
            # get the location for the new config file on disk
            start_dir = os.path.join(os.environ['OPUS_HOME'], 'project_configs')
            configDialog = QFileDialog()
            filter_str = QString("*.xml")
            fd = configDialog.getSaveFileName(self,QString("Save As..."),
                                              QString(start_dir), filter_str)
            # Check for cancel
            if len(fd) == 0:
                return
            fileName = QString(fd)
            # append xml extension if no extension was given
            if not fileName.endsWith('.xml') and len(fileName.split('.')) == 1:
                fileName = fileName + '.xml'
            domDocument = self.toolboxBase.doc
            opus_core_xml_configuration = self.toolboxBase.opus_core_xml_configuration
            indentSize = 2
            opus_core_xml_configuration.update(str(domDocument.toString(indentSize)))
            opus_core_xml_configuration.save_as(str(fileName))
            # mark all trees as clean
            self.toolboxBase.runManagerTree.model.markAsClean()
            self.toolboxBase.dataManagerTree.model.markAsClean()
            if self.toolboxBase.dataManagerDBSTree is not None:
                self.toolboxBase.dataManagerDBSTree.model.markAsClean()
            self.toolboxBase.modelManagerTree.model.markAsClean()
            self.toolboxBase.resultsManagerTree.model.markAsClean()
            self.toolboxBase.generalManagerTree.model.markAsClean()
            # reopen the file that was just saved to make it the active one
            self.openConfig(fileName)
        except:
            errorMessage = formatExceptionInfo(custom_message = 'Unexpected error saving config')
            QMessageBox.warning(self, 'Warning', errorMessage) 

    def _saveOrDiscardChanges(self):
        """
        Checks for changes to the currently open project (if any)
        and prompts user to save or discard changes.
        """
        if self.toolboxBase.projectIsDirty():
            doSave = QMessageBox.Discard
            question = ('Current project contains changes.\n'
                        'Do you want to save or discard those changes?')
            buttons = (QMessageBox.Discard,QMessageBox.Save)
            doSave = QMessageBox.question(self, "Warning", question, *buttons)
            if doSave == QMessageBox.Save:
                self.saveConfig()
            else:
                #if we have an existing tree we need to remove the dirty bit since we are discarding
                if self.toolboxBase.runManagerTree:
                    self.toolboxBase.runManagerTree.model.markAsClean()
                if self.toolboxBase.dataManagerTree:
                    self.toolboxBase.dataManagerTree.model.markAsClean()
                if self.toolboxBase.modelManagerTree:
                    self.toolboxBase.modelManagerTree.model.markAsClean()
                if self.toolboxBase.resultsManagerTree:
                    self.toolboxBase.resultsManagerTree.model.markAsClean()
                if self.toolboxBase.generalManagerTree:
                    self.toolboxBase.generalManagerTree.model.markAsClean()

    def closeConfig(self):
        """
        Closes the current project, if one is open.
        """

        try:
            configFile = self.toolboxBase.runManagerTree.model.configFile
        except:
            errorMessage = formatExceptionInfo(custom_message = 'Unexpected error closing config')
            QMessageBox.warning(self, 'Warning', errorMessage) 

        # Check to see if there are changes to the current project, if a project is open
        self._saveOrDiscardChanges()
        self.toolboxBase.close_controllers()
        
#        self.setWindowTitle(self.application_title)
        self.actionEdit_all_variables.setEnabled(False)
        self.actLaunchResultBrowser.setEnabled(False)

        os.environ['OPUSPROJECTNAME'] = 'misc'
        self.scenariosManagerBase.removeAllElements()
        self.resultsManagerBase.removeAllElements()
        self.modelsManagerBase.removeAllElements()

        self.actionClose_Project.setEnabled(False)
        self.actionSave_Project_2.setEnabled(False)
        self.actionSave_Project_As_2.setEnabled(False)
        
        self.toolboxBase.project_name = None
        self.updateWindowTitle()
        
    def closeEvent(self, event):
        '''called just before the window is closed.
        ask users if they want to save their changes (or cancel the closing)'''
        # Check to see if there are changes to the current project, if a project is open
        if self.toolboxBase.projectIsDirty():
            doSave = QMessageBox.Discard
            question = ('Do you want to save your changes '
                        'before quitting?')
            buttons = (QMessageBox.Cancel,
                       QMessageBox.Discard,
                       QMessageBox.Save)
            doSave = QMessageBox.question(self, "Unsaved changes", 
                                          question, 
                                          *buttons)
            if doSave == QMessageBox.Save:
                self.saveConfig()
            elif doSave == QMessageBox.Cancel:
                # dont quit
                event.ignore()
                return
        # Save application geometry on shut down
        settings = QSettings()
        settings.setValue("Geometry", QVariant(self.saveGeometry()))

    def editorOpenFileButton_released(self):
        #print "Open"
        # First find the file to open
        start_dir = ''
        opus_home = os.environ.get('OPUS_HOME')
        if opus_home:
            start_dir = opus_home
            start_dir_test = os.path.join(opus_home, 'project_configs')
            if start_dir_test:
                start_dir = start_dir_test
        configDialog = QFileDialog()
        filter_str = QString("*.py")
        fd = configDialog.getOpenFileName(self,QString("Please select a file..."),
                                          QString(start_dir), filter_str)
        # Check for cancel
        if len(fd) == 0:
            return
        fileName = QString(fd)
        fileNameInfo = QFileInfo(QString(fd))
        fileNameBaseName = fileNameInfo.completeBaseName()
        self.editorCurrentFileName = fileName

        # Clear out the old file
        self.editorStuff.clear()
        try:
            f = open(fileName,'r')
        except:
            return
        self.editorStuff.setText(f.read())
        f.close()
        self.editorStatusLabel.setText(QString("- ").append(QString(fileName)))
        self.editorDirty = False
        self.editorSaveFileButton.setDisabled(True)

    def editorSaveFileButton_released(self):
        #print "Save"
        if self.editorDirty == True:
            # Save the file TODO...
            if self.editorCurrentFileName:
                try:
                    f = open(self.editorCurrentFileName,'w')
                except:
                    return
                f.write(self.editorStuff.text())
                f.close()
                # Mark as clean
                wintitle = self.editorStatusLabel.text().replace("* ", "- ")
                self.editorStatusLabel.setText(wintitle)
                self.editorDirty = False
                self.editorSaveFileButton.setDisabled(True)

    def editorSaveAsFileButton_released(self):
        #print "Save As"
        if self.editorDirty == True:
            # Save the file TODO...
            # Mark as clean
            wintitle = self.editorStatusLabel.text().replace("* ", "- ")
            self.editorStatusLabel.setText(wintitle)
        self.editorDirty = False

    def editorStuffTextChanged(self):
        #print "text changed = " + str(self.editorDirty)
        if self.editorDirty == False:
            wintitle = self.editorStatusLabel.text().replace("- ", "* ")
            self.editorStatusLabel.setText(wintitle)
        self.editorDirty = True
        self.editorSaveFileButton.setEnabled(True)
    
    
    def changeFontSize(self):
        #menubar...
        menuFontSizeFamily = self.menubar.findChildren(QMenu)
        menuFontSizeFamily.append(self.menubar)
        menuActionFontSizeFamily = self.menubar.findChildren(QAction)
        
        #main tabs...
        regexp = QRegExp(".*tabbar$")
        toolbox = self.findChild(QWidget, "toolBox")
        tabwidget = self.findChild(QWidget, "tabWidget")
        
        mainTabsFontSizeFamily = [toolbox.findChildren(QWidget, regexp)[1],
                                  tabwidget.findChildren(QWidget, regexp)[0]]
        
        #subtabs...
        subtabFontSizeFamily = [toolbox.findChildren(QWidget, regexp)[0]]
        
        #set of widgets that shouldn't have their font changed
        omit = self.findChildren(QSpinBox)
        omit2 = []
        for omition in omit:
            omit2.extend(omition.findChildren(QWidget))
        omit.extend(omit2)
        
        widgetChildren = self.findChildren(QWidget)
        filter(lambda widge: widge not in menuActionFontSizeFamily and
                widge not in menuFontSizeFamily and
                widge not in mainTabsFontSizeFamily,
                widgetChildren)
            
        def fontSizeChange(qw, fontsize):
            qw.font().setPointSize(fontsize)
            try:
                qw.updateGeometry()
                qw.update()
            except:
                return
        
        map(lambda qw: fontSizeChange(qw,self.general_text_font_size),
            widgetChildren)
        map(lambda qw: fontSizeChange(qw,self.menu_font_size),
            menuFontSizeFamily)
        map(lambda qw: fontSizeChange(qw,self.main_tabs_font_size),
            menuActionFontSizeFamily)
        map(lambda qw: fontSizeChange(qw,self.main_tabs_font_size),
            mainTabsFontSizeFamily)
        self.updateGeometry()
        self.update()

    
    def getMenuFontSize(self):
        return self.menu_font_size
     
    def setMenuFontSize(self, pointSize):
        self.menu_font_size = pointSize 
    
    def getMainTabsFontSize(self):
        return self.main_tabs_font_size
    
    def setMainTabsFontSize(self, pointSize):
        self.main_tabs_font_size = pointSize

    def getGeneralTextFontSize(self):
        return self.general_text_font_size

    def setGeneralTextFontSize(self, pointSize):
        self.general_text_font_size = pointSize
    
    def getOpenLatestProject(self):
        return self.open_latest_project

    def setOpenLatestProject(self, open_latest_project):
        self.open_latest_project = open_latest_project
        

    def updateFontSettingsNode(self):
        #get the font settings node from xml
        font_settings_node = self.toolboxBase.gui_configuration_doc.elementsByTagName('font_settings').item(0)
        nodesToSave = {"menu_font_size":self.menu_font_size,
                       "main_tabs_font_size":self.main_tabs_font_size,
                       "general_text_font_size":self.general_text_font_size}
        #go through the children of the font settings node and set the text size correctly
        node = font_settings_node.firstChild()
        while not node.isNull():
            if node.isElement() and str(node.nodeName()) in nodesToSave:

                #we have a match for size_adjust, now we need to find the text node
                #in its children and set it to the value of font_size_adjust
                childElement = node.toElement()
                if childElement.hasChildNodes():
                    children = childElement.childNodes()
                    for x in xrange(0,children.count(),1):
                        if children.item(x).isText():
                            textNode = children.item(x).toText()
                            # Finally set the text node value
                            textNode.setData(QString(str(nodesToSave[str(node.nodeName())])))
                        
            node = node.nextSibling()
            
    def updateProjectHistoryNode(self):
        #get the project history node from xml
        proj_hist_node = self.toolboxBase.gui_configuration_doc.elementsByTagName('project_history').item(0)
        nodesToSave = {"previous_project":str(self.latest_project_file_name),
                       "":str(self.open_latest_project)}
        #go through the children of the project history node and set the value accordingly
        node = proj_hist_node.firstChild()
        while not node.isNull():
            if node.isElement() and str(node.nodeName()) in nodesToSave:
                element = node.toElement()
                hasTextNode = False
                if element.hasChildNodes():
                    child = element.firstChild()
                    while not child.isNull():
                        if child.isText():
                            hasTextNode = True
                            textNode = child.toText()
                            # Finally set the text node value
                            textNode.setData(QString(str(nodesToSave[str(node.nodeName())])))
                        child = child.nextSibling()
                if hasTextNode == False:
                    newText = self.toolboxBase.gui_configuration_doc.createTextNode(\
                                    QString(str(nodesToSave[str(node.nodeName())])))
                    element.appendChild(newText)
            node = node.nextSibling()

    def saveGuiConfig(self):
        try:
            self.toolboxBase.save_gui_configuration_file()
        except:
            errorInfo = formatExceptionInfo(custom_message = 'Unexpected error saving the gui config')
            self.errorCallback(errorInfo)  
