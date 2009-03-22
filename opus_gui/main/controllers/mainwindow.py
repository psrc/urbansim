# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import time, os

from xml.etree.cElementTree import ElementTree
from PyQt4.QtCore import Qt, QVariant, QThread, QString, QObject, SIGNAL
from PyQt4.QtCore import QSettings, QRegExp
from PyQt4.QtGui import QSpinBox, QMenu, QMainWindow, QMessageBox
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QAction, QFileDialog, QToolButton, QIcon


from opus_gui.main.controllers.instance_handlers import set_opusgui_instance
from opus_gui.main.views.ui_mainwindow import Ui_MainWindow
from opus_gui.main.controllers.dialogs.opusabout import UrbansimAboutGui
from opus_gui.main.controllers.dialogs.opuspreferences import UrbansimPreferencesGui
from opus_gui.main.controllers.dialogs.databasesettings import DatabaseSettingsEditGui
from opus_gui.main.controllers.opus_gui_configuration import OpusGuiConfiguration
from opus_gui.main.controllers.opus_project import OpusProject
from opus_gui.scenarios_manager.scenario_manager import ScenariosManager
from opus_gui.scenarios_manager.scenario_manager_functions import update_models_to_run_lists
from opus_gui.results_manager.results_manager import ResultsManager
from opus_gui.models_manager.models_manager import ModelsManager
from opus_gui.general_manager.general_manager import GeneralManager
from opus_gui.data_manager.data_manager import DataManager
from opus_gui.util.exception_formatter import formatExceptionInfo
from opus_gui.general_manager.controllers.all_variables import AllVariablesEditGui

class OpusGui(QMainWindow, Ui_MainWindow):
    '''
    Main window used for housing the canvas, toolbars, and dialogs
    '''

    class Output:
        '''
        Output override for the app to catch stdout and stderr and
        placing it in the log tab
        '''
        def __init__( self, writefunc ):
            self.writefunc = writefunc
        def write( self, line ):
            if line != "\n":
                self.writefunc(line)

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        # Bind the application global instance for to this window
        set_opusgui_instance(self)

        # this is to remove the three tabs that are in the UI file
        for i in range(2, -1, -1):
            self.tabWidget.removeTab(i)

        self.thread().setPriority(QThread.HighestPriority)

        # This is the output for stdout
        self.output = OpusGui.Output(self.writeOutput)

        self.splitter.setSizes([400, 500])

        # Initialize empty project
        self.project = OpusProject()

        # Read database connection names
        settings_directory = os.path.join(os.environ['OPUS_HOME'], 'settings')
        db_con_file = os.path.join(settings_directory,
                                   'database_server_configurations.xml')
        db_config_node = ElementTree(file=db_con_file).getroot()
        self.db_connection_names = [node.tag for node in db_config_node if
                                    node.get('hidden') != "True"
                                    # hack?
                                    and node.tag != 'xml_version']

        # Application default configuration
        self.gui_config = OpusGuiConfiguration()
        self.gui_config.load()

        # Show splash screen
        self.gui_config.splash_screen.show()

        # Bind actions
        self._setupActions()

        # Manager collection -- initialized by openProject()
        self.managers = {}

        # Delay before hiding the splash screen
        time.sleep(1)
        self.gui_config.splash_screen.hide()

        # Restoring application geometry from last shut down
        settings = QSettings()
        self.restoreGeometry(settings.value("Geometry").toByteArray())
        self.updateFontSize()
        self.setFocus()

        # Variable library
        self.all_variables = None

        # Load the latest project file if that flag is set in GUI configuration
        if self.gui_config.load_latest_on_start:
            self.openProject(self.gui_config.latest_project_filename or '')

        ###T: removing these until they serve a purpose
        self.menuUtilities.removeAction(self.actPythonView)
        #self.menuUtilities.removeAction(self.actionLog_View)
        self.menuUtilities.removeAction(self.actEditorView)

        self.updateWindowTitle()

    def _setupActions(self):
        ''' Bind actions to callbacks and setup keyboard shortcuts '''

        # Keyboard shortcuts
        self.actOpenProject.setShortcut('Ctrl+O')
        self.actSaveProject.setShortcut('Ctrl+S')
        self.actSaveProjectAs.setShortcut('Ctrl+Shift+S')
        self.actCloseProject.setShortcut('Ctrl+W')
        self.actVariableLibrary.setShortcut('Ctrl+V')
        self.actLaunchResultBrowser.setShortcut('Ctrl+R')
        self.actDatabaseSettings.setShortcut('Ctrl+D')
        self.actPreferences.setShortcut('Ctrl+P')

        # Connect trigger slots using a little quickie function
        def connect(action, callback):
            QObject.connect(action, SIGNAL("triggered()"), callback)
        connect(self.actOpenProject, self.openProject)
        connect(self.actSaveProject, self.saveProject)
        connect(self.actSaveProjectAs, self.saveProjectAs)
        connect(self.actCloseProject, self.closeProject)
        connect(self.actExit, self.close)
        connect(self.actAbout, self.openAbout)
        connect(self.actPreferences, self.openPreferences)
        connect(self.actDatabaseSettings, self.openDatabaseSettings)
        connect(self.actVariableLibrary, self.editAllVariables)
        connect(self.actLogView, self.openLogTab)
        connect(self.actLaunchResultBrowser, self.openResultBrowser)

        # Create a 'Close tab' widget
        action = QAction(self)
        action.setIcon(QIcon(':/Images/Images/cross.png'))
        connect(action, self.closeCurrentTab)
        widget = QToolButton(self)
        widget.setDefaultAction(action)
        widget.setWhatsThis('Close tab')
        widget.setToolTip('Close tab')
        self.tabWidget.setCornerWidget(widget)

        # GIS -- disabled for time being
        # connect(self.actionMap_View, self.openMapTab)

        # Disable some options by default
        self.actVariableLibrary.setEnabled(False)
        self.actLaunchResultBrowser.setEnabled(False)

    def writeOutput(self, result):
        ''' Write non empty results to logView '''
        if result == "":
            return
        self.logViewTextBrowser.append(result)

    def editAllVariables(self):
        ''' Open the variable library GUI '''
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        self.all_variables = AllVariablesEditGui(self, flags)

        self.all_variables.setModal(True)
        self.all_variables.show()

    def closeCurrentTab(self):
        ''' Close the currently showing tab '''
        widget = self.tabWidget.currentWidget()

        # Check which manager the tab belongs to and ask it to close the tab
        # TODO maybe implement a generic tab element that knows which parent
        # it belongs to?
        for manager in self.managers.values():
            if widget in manager.tab_widgets:
                manager.close_tab(widget)
                break
        else:
            # Finished loop w/o finding the parent of the tab so close manually
            self.tabWidget.removeTab(self.tabWidget.currentIndex())

    def openMapTab(self):
        ''' Open up a tab containing a map view '''
        if self.tabWidget.indexOf(self.tab_mapView) == -1:
            self.tab_mapView.show()
            self.updateFontSize()
            map_icon = QIcon(":/Images/Images/map.png")
            self.tabWidget.insertTab(0, self.tab_mapView, map_icon, "Map View")
            self.tabWidget.setCurrentWidget(self.tab_mapView)

    def openResultBrowser(self):
        ''' Open a Results browser '''
        self.managers['results_manager'].add_result_browser()

    def openLogTab(self):
        ''' Open a log viewer '''
        if self.tabWidget.indexOf(self.tab_logView) == -1:
            self.tab_logView.show()
            self.updateFontSize()
            self.tabWidget.insertTab(0,self.tab_logView,
                                     QIcon(":/Images/Images/table.png"),"Log View")
            self.tabWidget.setCurrentWidget(self.tab_logView)

    def openAbout(self):
        ''' Show a dialog box with information about OpusGui '''
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        wnd = UrbansimAboutGui(self,flags)
        wnd.setModal(True)
        wnd.show()
        self.updateFontSize()

    def openPreferences(self):
        ''' Open the preferences window '''
        wnd = UrbansimPreferencesGui(self)
        wnd.setModal(True)
        wnd.show()
        self.updateFontSize()

    def openDatabaseSettings(self):
        ''' Open the database settings window '''
        #wnd = UrbansimDatabaseSettingsGUI(self, flags)
        # Commented out the previous line and added the following line
        # to test out the APR added database connection editing GUI (082908)
        wnd = DatabaseSettingsEditGui(self)
        wnd.setModal(True)
        wnd.setWindowTitle('Database Server Connections')
        wnd.show()
        self.updateFontSize()

    def updateWindowTitle(self):
        '''update the window title to reflect the state of the project'''
        # assemble a title consisting of application title (at),
        # project file name (pfn) and project name (pn)
        at = self.gui_config.application_title
        pn = self.project.name
        pfn = (self.project.filename or '').split(os.sep)[-1]

        if self.project.is_open():
            if self.project.dirty:
                title = '%s - (*) %s - [file: %s]' % (at, pn, pfn)
            else:
                title = '%s - %s - [file: %s]' % (at, pn, pfn)
        else:
            title = at or '' # Show just application title

        self.setWindowTitle(QString(title))

    def openProject(self, project_filename = None):
        '''
        Open and initialize a project.
        If the project_filename parameter is None, the user is asked for a file
        @param project_filename (String): absolute path to project file to load
        '''
        # Ask to save any changes before openeing a new project
        if self.okToCloseProject() == False: return

        # Close the currently opened project
        self.closeProject()

        # Ask for filename if one was not provided
        if project_filename is None:
            start_dir = ''
            project_configs = os.path.join((os.environ.get('OPUS_HOME') or '.'),
                                           'project_configs')
            if os.path.exists(project_configs):
                start_dir = project_configs

            filter_str = QString("*.xml")
            msg = "Select project file to load"
            project_filename = QFileDialog().getOpenFileName(self, msg,
                                                     start_dir, filter_str)
            if not project_filename:
                return # Cancel

        loaded_ok, msg = self.project.open(project_filename)
        if not loaded_ok:
            QMessageBox.warning(self, 'Failed to load project', msg)
            return

        # update latest project config
        self.gui_config.latest_project_filename = self.project.filename
        self.gui_config.save()

        # Initialize managers for the different tabs

        self.managers['general'] = \
        GeneralManager(self.generalmanager_page, self.tabWidget, self.project)

        self.managers['model_manager'] = \
        ModelsManager(self.modelmanager_page, self.tabWidget, self.project)

        self.managers['scenario_manager'] = \
        ScenariosManager(self.runmanager_page, self.tabWidget, self.project)

        self.managers['results_manager'] = \
        ResultsManager(self.resultsmanager_page, self.tabWidget, self.project)

        # DataManager is a little special since it has two "base_widgets"
        self.managers['data_manager'] = \
        DataManager(self.datamanager_xmlconfig, # XmlController
                    self.datamanager_dirview, # FileController
                    self.tabWidget, self.project)

        self.managers['results_manager'].scanForRuns()

        # Enable actions on opened project
        self.actLaunchResultBrowser.setEnabled(True)
        self.actVariableLibrary.setEnabled(True)

        self.actCloseProject.setEnabled(True)
        self.actSaveProject.setEnabled(True)
        self.actSaveProjectAs.setEnabled(True)
        self.updateFontSize()

        self.updateWindowTitle()
        update_models_to_run_lists()

    def saveProject(self, filename = None):
        '''
        Save the configuration file to disk.
        @param filename (String): filename to save to
        @return: True if save was successful, False otherwise
        '''
        ok_flag, msg = self.project.save(filename)
        if not ok_flag:
            QMessageBox.critical(self, 'Could not save project', msg)
            return False
        return True

    def saveProjectAs(self):
        ''' Save the project configuration under a different name '''
        try:
            # get the location for the new config file on disk
            start_dir = os.path.join(os.environ['OPUS_HOME'], 'project_configs')
            configDialog = QFileDialog()
            filter_str = QString("*.xml")
            fd = configDialog.getSaveFileName(self,QString("Save As..."),
                                              QString(start_dir), filter_str)
            # Check for cancel
            if not fd:
                return

            filename = QString(fd)
            # append xml extension if no extension was given
            if not filename.endsWith('.xml') and len(filename.split('.')) == 1:
                filename = filename + '.xml'

            if not self.saveProject(filename):
                return

            # hack: open the project right after save to properly change the
            # 'active project' related parameters
            self.openProject(filename)

        except:
            errorMessage = formatExceptionInfo(custom_message = \
                                               'Unexpected error saving config')
            QMessageBox.warning(self, 'Warning', errorMessage)

    def okToCloseProject(self):
        '''
        Called before an operation that causes this project to close.
        If the project contains changes; ask if the user wants to save them,
        discard them or cancel the operation.
        @return: True if the user wishes to proceed with the closing operation.
        '''
        if not self.project.dirty: return True

        question = ('Current project contains changes.\n'
                    'Do you want to save or discard those changes?')
        buttons = (QMessageBox.Discard, QMessageBox.Save, QMessageBox.Cancel)
        doSave = QMessageBox.question(self, "Warning", question, *buttons)
        if doSave == QMessageBox.Save:
            ok_flag, msg = self.project.save() # cancels on failed save
            if not ok_flag:
                QMessageBox.critical(self, "Could not save project", str(msg))
                return False
            return True
        elif doSave == QMessageBox.Discard:
            self.project.dirt = False
            return True
        else:
            return False

    def closeProject(self):
        ''' Closes the current project. '''
        if not self.okToCloseProject(): return

        for manager in self.managers.values():
            manager.close()

        self.project.close()

        self.actVariableLibrary.setEnabled(False)
        self.actLaunchResultBrowser.setEnabled(False)

        self.actCloseProject.setEnabled(False)
        self.actSaveProject.setEnabled(False)
        self.actSaveProjectAs.setEnabled(False)

    def closeEvent(self, event):
        '''
        Callback for close window event.
        Give the user a change to save any project changes or continue working.
        '''
        if not self.okToCloseProject():
            event.ignore()
            return

        # Save application geometry and gui configuration on shut down
        self.gui_config.save()
        settings = QSettings()
        settings.setValue("Geometry", QVariant(self.saveGeometry()))

    def updateFontSize(self):
        ''' Update various widgets with the font size from GUI settings '''
        # TODO -- this could use some clean up
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

        map(lambda qw: fontSizeChange(qw,self.gui_config.fonts['general']),
            widgetChildren)
        map(lambda qw: fontSizeChange(qw,self.gui_config.fonts['menu']),
            menuFontSizeFamily)
        map(lambda qw: fontSizeChange(qw,self.gui_config.fonts['tabs']),
            menuActionFontSizeFamily)
        map(lambda qw: fontSizeChange(qw,self.gui_config.fonts['tabs']),
            mainTabsFontSizeFamily)
        self.updateGeometry()
        self.update()
