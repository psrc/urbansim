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

import os,tempfile
from xml.etree.cElementTree import ElementTree
import StringIO

# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import QFileInfo, QFile, QIODevice
from PyQt4.QtGui import QMessageBox
from PyQt4.QtXml import QDomDocument

from opus_gui.data_manager.controllers.files.file_controller_opus_data import FileController_OpusData
from opus_core.configurations.xml_configuration import XMLConfiguration

from opus_gui.general_manager.controllers.xml_configuration.xml_controller_general import XmlController_General
from opus_gui.results_manager.controllers.xml_configuration.xml_controller_results import XmlController_Results
from opus_gui.models_manager.controllers.xml_configuration.xml_controller_models import XmlController_Models
from opus_gui.scenarios_manager.controllers.xml_configuration.xml_controller_scenarios import XmlController_Scenarios
from opus_gui.data_manager.controllers.xml_configuration.xml_controller_data_tools import XmlController_DataTools
from opus_core.opus_exceptions.xml_version_exception import XMLVersionException
from opus_core.misc import directory_path_from_opus_path

# Main class for the toolbox
class ToolboxBase(object):
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow

        # References to some parent main window elements
        self.tabWidget = self.mainwindow.tabWidget
        self.toolBox = self.mainwindow.toolBox

        # Storage for the master copy of the project XML
        self.xml_file = None
        self.doc = None
        self.configFile = None
        self.configFileTemp = None
        self.opus_core_xml_configuration = None
        self.view = None

        # These are the trees that are displayed for each toolbox
        self.generalManagerTree = None
        self.modelManagerTree = None
        self.resultsManagerTree = None
        self.runManagerTree = None
        self.dataManagerTree = None
        self.dataManagerFileTree = None

        # TODO never used -- obsolete or returning feature?
        self.dataManagerDBSTree = None

        gui_directory = os.path.join(os.environ['OPUS_HOME'], 'settings')
        if not os.path.exists(gui_directory):
            os.mkdir(gui_directory)
        
        self.gui_configuration_file = os.path.join(gui_directory, 'gui_config.xml')
        if not os.path.exists(self.gui_configuration_file):
            self.emit_default_gui_configuration_file(self.gui_configuration_file)

        self.project_name = None

        self.gui_configuration_doc = QDomDocument()
        self.gui_configuration_doc.setContent(QFile(self.gui_configuration_file))


    def updateOpusXMLTree(self):
        '''
        Update the XMLConfiguration object for the currently opened project with
        the XML content in QtXml.
        '''
        if self.opus_core_xml_configuration and self.doc:
            indentSize = 2
            self.opus_core_xml_configuration.update(str(self.doc.toString(indentSize)))


    def openXMLTree(self, xml_file):
        '''
        Load a project from a XML file.
        @param xml_file: filename (str) of XML file to load
        @return: True if the load was successful, False otherwise.
        '''

        # make sure all trees are clean and close them
        if not self.close_controllers():
            msg = ('There was an error removing the old config. '
                'Details:\nCould not remove all manager trees.\n'
                'Try to restart OpusGui and open the project again')
            QMessageBox.critical(self.mainwindow, 'Error loading file', msg)
            return False

        # Open the XML by first passing to the xml_configuration and letting
        # opus core return the nested XML based on inheritence
        self.xml_file = xml_file
        self.configFile = QFile(xml_file)
        fileNameInfo = QFileInfo(self.xml_file)
        fileName = fileNameInfo.fileName().trimmed()
        fileNamePath = fileNameInfo.absolutePath().trimmed()
        try:
            self.opus_core_xml_configuration = XMLConfiguration(str(fileName),str(fileNamePath))
        except Exception, ex:
            msg = 'Failed to load XML:\n'
            QMessageBox.critical(self.mainwindow, 'Failed to load XML',
                                 msg + str(ex))
            return False

        _, tempFilePath = tempfile.mkstemp()
        #print tempFile,tempFilePath
        # full_tree is the "whole" tree, inherited nodes and all
        # tree is just the actual file the GUI was asked to open
        self.configFileTemp = QFile(tempFilePath)
        self.opus_core_xml_configuration.full_tree.write(tempFilePath)
        if not self.configFile or not self.configFileTemp:
            msg = "Error reading the %s configuration file" % (xml_file)
            QMessageBox.critical(self.mainwindow, 'Error loading file', msg)
            return False

        self.configFileTemp.open(QIODevice.ReadWrite)
        self.doc = QDomDocument()
        self.doc.setContent(self.configFileTemp)
        self.project_name = self.opus_core_xml_configuration.full_tree.getroot().findtext('./general/project_name')

        self.opusDataPath = os.path.join(self.opus_core_xml_configuration.get_opus_data_path(), self.project_name)
        os.environ['OPUSPROJECTNAME'] = self.project_name

        self.generalManagerTree = \
            XmlController_General(self, self.mainwindow.generalmanager_page)
        self.modelManagerTree = \
            XmlController_Models(self, self.mainwindow.modelmanager_page)
        self.runManagerTree = \
            XmlController_Scenarios(self, self.mainwindow.runmanager_page)
        self.dataManagerTree = \
            XmlController_DataTools(self, self.mainwindow.datamanager_xmlconfig)
        self.resultsManagerTree = \
            XmlController_Results(self, self.mainwindow.resultsmanager_page)

        self.dataManagerFileTree = \
            FileController_OpusData(self, 'data_manager.opus_data',
                                    self.opusDataPath,
                                    self.mainwindow.datamanager_dirview.layout())

        # project loaded, show any XML version messages
        if self.opus_core_xml_configuration.version_warning_message:
            msg = ('Warning! Inconsistent version numbers found in XML files '
                   'when loading project.\n\nDetails:\n\n')
            msg = msg + self.opus_core_xml_configuration.version_warning_message
            QMessageBox.warning(self.mainwindow, 'Inconsistent xml versions', msg)
        return True


    def projectIsDirty(self):
        '''
        Get dirty status for the project.
        @return: True if any of the managers is dirty, False otherwise
        '''
        managers = [self.resultsManagerTree,
            self.modelManagerTree,
            self.runManagerTree,
            self.dataManagerTree,
            self.generalManagerTree]
        for manager in managers:
            if manager and manager.model.isDirty():
                return True
        return False


    def markProjectAsClean(self):
        ''' Marks all of the manager trees as clean '''
        managers = [self.resultsManagerTree,
            self.modelManagerTree,
            self.runManagerTree,
            self.dataManagerTree,
            self.generalManagerTree]
        for manager in managers:
            if manager:
                manager.model.markAsClean()


    def close_controllers(self):
        '''
        Close all manager trees.
        @return: True if all trees was successfully closed, False otherwise.
        '''
        managers = [self.resultsManagerTree, self.modelManagerTree,
                  self.runManagerTree, self.dataManagerTree,
                  self.generalManagerTree, self.dataManagerFileTree]

        for manager in managers:
            if manager and manager.removeTree() == False:
                return False
        return True


    def emit_default_gui_configuration_file(self, file_name):
        ''' 
        Copy the default configuration file from opus_gui/main.
        @param: file_name (String) full path of where to copy the configuration
        '''
        default_gui_config_path = os.path.join(directory_path_from_opus_path('opus_gui.main'),
                                               'default_gui_configuration.xml')
        default_gui_config = open(default_gui_config_path)
        new_file = open(file_name, 'w')
        new_file.write(''.join(default_gui_config.readlines()))
        new_file.close()
        default_gui_config.close()


    def reemit_reinit_default_gui_configuration_file(self):
        '''
        Emit the default configuration file and initialize the QDomDocument for
        configurations from the newly emitted file.
        '''
        self.emit_default_gui_configuration_file(self.gui_configuration_file)
        self.gui_configuration_doc = QDomDocument()
        self.gui_configuration_doc.setContent(QFile(self.gui_configuration_file))


    def save_gui_configuration_file(self):
        ''' Update and save the GUI configuration file '''
        str_io = StringIO.StringIO(self.gui_configuration_doc.toString(2))
        etree = ElementTree(file=str_io)
        etree.write(self.gui_configuration_file)
        str_io.close()
