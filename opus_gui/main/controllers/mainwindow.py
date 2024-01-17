# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE
from opus_gui.util.icon_library import IconLibrary

import os, sys

from lxml.etree import ElementTree, Comment
from PyQt5.QtCore import Qt, QVariant, QThread, QObject, pyqtSignal
from PyQt5.QtCore import QSettings, QRegExp
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QSpinBox, QMenu, QMainWindow, QMessageBox
from PyQt5.QtWidgets import QWidget, QTabWidget
from PyQt5.QtWidgets import QAction, QFileDialog, QToolButton
from PyQt5.QtGui import QIcon

from opus_gui.main.controllers.dialogs.message_box import MessageBox
from opus_gui.main.controllers.instance_handlers import set_opusgui_instance
from opus_gui.main.views.ui_mainwindow import Ui_MainWindow
from opus_gui.main.controllers.dialogs.opusabout import UrbansimAboutGui
from opus_gui.main.controllers.dialogs.opuspreferences import UrbansimPreferencesGui
from opus_gui.main.controllers.dialogs.databasesettings import DatabaseSettingsEditGui
from opus_gui.main.opus_project import OpusProject
from opus_gui.scenarios_manager.scenario_manager import ScenariosManager
from opus_gui.scenarios_manager.scenario_manager_functions import update_models_to_run_lists
from opus_gui.results_manager.results_manager import ResultsManager
from opus_gui.models_manager.models_manager import ModelsManager
from opus_gui.general_manager.general_manager import GeneralManager
from opus_gui.main.controllers.log_widget import LogWidget
from opus_gui.data_manager.data_manager import DataManager
from opus_gui.util.exception_formatter import formatExceptionInfo
from opus_gui.util import common_dialogs

from opus_gui.main.controllers.dialogs.load_project_template_dialog import LoadProjectTemplateDialog
from opus_gui.main.controllers.dialogs.new_project_dialog import NewProjectDynamicDialog
#from opus_gui.general_manager.controllers.variable_library import VariableLibrary
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration
from opus_core import paths

class OpusGui(QMainWindow, Ui_MainWindow):
    '''
    Main window used for housing the canvas, toolbars, and dialogs
    '''

    def __init__(self, gui_configuration = None):
        QMainWindow.__init__(self)
        self.setupUi(self)

        # Bind the application global instance for to this window
        set_opusgui_instance(self)

        self.thread().setPriority(QThread.HighestPriority)

        self.tabWidget = QTabWidget(self.splitter)
        self.splitter.setSizes([400, 500])

        # Create a log window
        self.log_tab = LogWidget(self.tabWidget)
        self.log_tab.start_stdout_capture()

        # Initialize empty project
        self.project = OpusProject()
        self.shows_hidden = False

        # Read database connection names
        db_con_file = DatabaseServerConfiguration.get_default_configuration_file_path()
        db_config_node = ElementTree(file=db_con_file).getroot()
        self.db_connection_names = [node.tag for node in db_config_node if
                                     node.tag != Comment and node.get('hidden') != "True" and node.tag != 'xml_version']
  
        # Application default configuration
        self.gui_config = gui_configuration

        # Bind actions
        self._setup_actions()

        # Manager collection -- initialized by openProject()
        self.managers = {}

#        # Delay before hiding the splash screen
#        time.sleep(1)
#        self.gui_config.splash_screen.hide()

        # Restoring application geometry from last shut down
        settings = QSettings()
        if settings.value("Geometry") is not None:
            self.restoreGeometry(settings.value("Geometry"))
        self.updateFontSize()
        self.setFocus()

        # Variable library
        self.variable_library = None

        # Load the latest project file if that flag is set in GUI configuration
        if self.gui_config.load_latest_on_start:
            try:
                self.openProject(self.gui_config.latest_project_filename or '')
            except:
                self.closeProject()
            if self.gui_config.load_latest_tab_on_start:
                try:
                    self.toolBox.setCurrentIndex(int(self.gui_config.latest_tab_index))
                except:
                    pass
        ###T: removing these until they serve a purpose
        self.menuUtilities.removeAction(self.actPythonView)
        #self.menuUtilities.removeAction(self.actionLog_View)
        self.menuUtilities.removeAction(self.actEditorView)

#        self.connect(self, pyqtSignal('variables_updated'), self.update_saved_state)
#        self.variables_updated.connect(self.update_saved_state) # HS: TODO: after variable library is fixed
        self.update_saved_state()

    def _setup_actions(self):
        ''' Bind actions to callbacks and setup keyboard shortcuts '''

        # Keyboard shortcuts
        self.actOpenProject.setShortcut('Ctrl+O')
        self.actSaveProject.setShortcut('Ctrl+S')
        self.actShowHidden.setShortcut('Ctrl+H')
        self.actSaveProjectAs.setShortcut('Ctrl+Shift+S')
        self.actReloadProject.setShortcut('Ctrl+Shift+R')
        self.actCloseProject.setShortcut('Ctrl+W')
        self.actExit.setShortcut('Ctrl+Q')
        self.actVariableLibrary.setShortcut('Ctrl+V')
        self.actLaunchResultBrowser.setShortcut('Ctrl+R')
        self.actDatabaseSettings.setShortcut('Ctrl+D')
        self.actPreferences.setShortcut('Ctrl+P')

        # Connect trigger slots using a little quickie function
        def connect(action, callback):
            action.triggered.connect(callback)
        connect(self.actNewProject, self.newProject)
        connect(self.actOpenProject, self.openProject)
        connect(self.actSaveProject, self.saveProject)
        connect(self.actShowHidden, self.showHidden)
        connect(self.actSaveProjectAs, self.saveProjectAs)
        connect(self.actReloadProject, self.reloadProject)
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
        # flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        if self.project is None or not self.project.is_open():
            return
        if self.variable_library is not None:
            self.variable_library.initialize()
        else:
            self.variable_library = VariableLibrary(self.project, self)
        self.variable_library.exec_()

    def closeCurrentTab(self):
        ''' Close the currently showing tab '''
        widget = self.tabWidget.currentWidget()

        # Check which manager the tab belongs to and ask it to close the tab
        # TODO maybe implement a generic tab element that knows which parent
        # it belongs to?
        for manager in list(self.managers.values()):
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
        if self.tabWidget.indexOf(self.log_tab) == -1:
            self.tabWidget.insertTab(0, self.log_tab, IconLibrary.icon('table'), 'Log Window')
        self.log_tab.do_refresh()
        self.tabWidget.setCurrentWidget(self.log_tab)

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

    def showHidden(self):
        self.shows_hidden = not self.shows_hidden
        for manager in list(self.managers.values()):
            manager.xml_controller.rebuild()

    def update_saved_state(self, force_dirty = False):
        '''update the window title to reflect the state of the project
        @param force_dirty makes the project dirty before setting the save state'''
        # assemble a title consisting of application title (at),
        # project file name (pfn) and project name (pn)
        at = self.gui_config.application_title
        pn = self.project.name
        pfn = (self.project.filename or '').split(os.sep)[-1]

        if self.project.is_open():
            if force_dirty:
                self.project.dirty = True
            if self.project.dirty:
                title = '%s - (*) %s - [file: %s]' % (at, pn, pfn)
            else:
                title = '%s - %s - [file: %s]' % (at, pn, pfn)
            self.actSaveProject.setEnabled(self.project.dirty)
        else:
            title = 'OPUS' if not at else at # Show just application title
            self.actSaveProject.setEnabled(False)

        self.setWindowTitle((title))

    def openProject(self, project_filename = None, text = None):
        '''
        Open and initialize a project.
        If the project_filename parameter is None, the user is asked for a file
        @param project_filename (String): absolute path to project file to load
        '''
        # Ask to save any changes before openeing a new project
        if self.okToCloseProject(text) == False: return

        # Close the currently opened project
        self.closeProject()

        # Ask for filename if one was not provided
        if project_filename is None or project_filename is False:
            start_dir = ''
            project_configs = paths.OPUS_PROJECT_CONFIGS_PATH
            if os.path.exists(project_configs):
                start_dir = project_configs

            filter_str = ("*.xml")
            msg = "Select project file to load"
            project_filename = QFileDialog().getOpenFileName(self, msg,
                                                     start_dir, filter_str)
            if not project_filename:
                return # Cancel

        if len(project_filename) > 1:
            project_filename = project_filename[0]
            
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
        self.actShowHidden.setEnabled(True)
        self.actReloadProject.setEnabled(True)
        self.updateFontSize()

        self.update_saved_state()
        update_models_to_run_lists()
        
        
    def newProject(self):
        ''' User selected "New Project" menu option '''
        # Ask to save any changes before openeing a new project
        if self.okToCloseProject() == False: return

        # Close the currently opened project
        self.closeProject()
        
        # let the user select a project to base the new project on
        load_dialog = LoadProjectTemplateDialog(self)
        if load_dialog.exec_() != load_dialog.Accepted:
            return
        
        template_project = load_dialog.template_project
        
        # let the user fill in any project specific changes
        new_project_dialog = NewProjectDynamicDialog(template_project, parent_widget = self) 
        if new_project_dialog.exec_() != new_project_dialog.Accepted:
            return
        
        # open the newly created project
        self.openProject(new_project_dialog.new_project_filename)
            

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
            start_dir = paths.OPUS_PROJECT_CONFIGS_PATH
            configDialog = QFileDialog()
            filter_str = ("*.xml")
            fd = configDialog.getSaveFileName(self,("Save As..."),
                                              (start_dir), filter_str)
            # Check for cancel
            if not fd:
                return

            filename = (fd)
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

    def reloadProject(self, text='reloading the project'):
        self.openProject(self.project.filename, text=text)
    
    def okToCloseProject(self, text=None):
        '''
        Called before an operation that causes this project to close.
        If the project contains changes; ask if the user wants to save them,
        discard them or cancel the operation.
        @return: True if the user wishes to proceed with the closing operation.
        '''
        if not self.project.dirty: return True
        if text is None: text = 'closing the project'
        question = 'Do you want to save your changes before %s?' % text
        user_answer = common_dialogs.save_before_close(question)
        if user_answer == common_dialogs.YES:
            ok_flag, msg = self.project.save() # cancels on failed save
            if not ok_flag:
                MessageBox.error(self, "Could not save project", str(msg))
                return False
            return True
        elif user_answer == common_dialogs.NO:
            self.project.dirty = False
            return True
        else:
            return False

    def closeProject(self):
        ''' Closes the current project. '''
        if not self.okToCloseProject(): return

        for manager in list(self.managers.values()):
            manager.close()

        self.project.close()

        self.actVariableLibrary.setEnabled(False)
        self.actLaunchResultBrowser.setEnabled(False)

        self.actCloseProject.setEnabled(False)
        self.actSaveProject.setEnabled(False)
        self.actShowHidden.setEnabled(False)
        self.actSaveProjectAs.setEnabled(False)
        self.actReloadProject.setEnabled(False)

    def closeEvent(self, event):
        '''
        Callback for close window event.
        Give the user a change to save any project changes or continue working.
        '''
        if not self.okToCloseProject():
            event.ignore()
            return

        # Save application geometry and gui configuration on shut down
        self.gui_config.latest_tab_index = str(self.toolBox.currentIndex())
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
        toolbox = self.toolBox
        tabwidget = self.tabWidget

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
        [widge for widge in widgetChildren if widge not in menuActionFontSizeFamily and
                widge not in menuFontSizeFamily and
                widge not in mainTabsFontSizeFamily]

        def fontSizeChange(qw, fontsize):
            qw.font().setPointSize(fontsize)
            try:
                qw.updateGeometry()
                qw.update()
            except:
                return

        list(map(lambda qw: fontSizeChange(qw,self.gui_config.fonts['general']),
            widgetChildren))
        list(map(lambda qw: fontSizeChange(qw,self.gui_config.fonts['menu']),
            menuFontSizeFamily))
        list(map(lambda qw: fontSizeChange(qw,self.gui_config.fonts['tabs']),
            menuActionFontSizeFamily))
        list(map(lambda qw: fontSizeChange(qw,self.gui_config.fonts['tabs']),
            mainTabsFontSizeFamily))
        self.updateGeometry()
        self.update()
