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
from PyQt4.QtCore import QString, QFileInfo, QFile, QIODevice
from PyQt4.QtGui import QMessageBox
from PyQt4.QtXml import QDomDocument

from opus_gui.data_manager.controllers.files.action_data_opus_data import fileActionController_Data_opus_data
from opus_core.configurations.xml_configuration import XMLConfiguration

from opus_gui.general_manager.controllers.xml.action_general import xmlActionController_General
from opus_gui.results_manager.controllers.xml.action_results import xmlActionController_Results
from opus_gui.models_manager.controllers.xml.action_models import xmlActionController_Models
from opus_gui.scenarios_manager.controllers.xml.action_scenarios import xmlActionController_Scenarios
from opus_gui.data_manager.controllers.xml.action_data_tools import xmlActionController_Data_tools

import os,tempfile

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
        self.opusXMLTree = None
        
        # These are the trees that are displayed for each toolbox
        self.view = None
        self.modelManagerTree = None
        self.resultsManagerTree = None
        self.runManagerTree = None
        self.dataManagerTree = None
        self.dataManagerFileTree = None
        self.generalManagerTree = None

        gui_directory = os.path.join(os.environ['OPUS_HOME'], 'settings')
        if not os.path.exists(gui_directory):
            os.mkdir(gui_directory)
        self.gui_configuration_file = os.path.join(gui_directory, 'gui_config.xml')
        if not os.path.exists(self.gui_configuration_file):
            self.emit_default_gui_configuration_file(file_name = self.gui_configuration_file)

        self.gui_configuration_doc = QDomDocument()
        self.gui_configuration_doc.setContent(QFile(self.gui_configuration_file))

    def updateOpusXMLTree(self):
        if self.opusXMLTree and self.doc:
            # print "updateOpusXMLTree"
            indentSize = 2
            self.opusXMLTree.update(str(self.doc.toString(indentSize)))
    
    def openXMLTree(self, xml_file):
        saveBeforeOpen = QMessageBox.Discard
        # Check if the current model(s) is(are) dirty first...
        save_string = QString("Current project contains changes... \n"
                              "Should we save or discard those changes before opening?")

        for manager in [self.resultsManagerTree, self.modelManagerTree, self.runManagerTree, self.dataManagerTree]:
            if manager and manager.model.isDirty():
                saveBeforeOpen = QMessageBox.question(self.mainwindow,"Warning",
                                                      save_string,
                                                      QMessageBox.Discard,QMessageBox.Save)
                break

        if saveBeforeOpen == QMessageBox.Save:
            self.mainwindow.saveConfig()
        else:
            #if we have an existing tree we need to remove the dirty bit since we are discarding
            if self.runManagerTree:
                self.runManagerTree.model.markAsClean()
            if self.dataManagerTree:
                self.dataManagerTree.model.markAsClean()
            if self.modelManagerTree:
                self.modelManagerTree.model.markAsClean()
            if self.resultsManagerTree:
                self.resultsManagerTree.model.markAsClean()
            if self.generalManagerTree:
                self.generalManagerTree.model.markAsClean()

        # Try to remove all the old trees...
        generalManagerRemoveSuccess = True
        if self.generalManagerTree != None:
            generalManagerRemoveSuccess = self.generalManagerTree.removeTree()
        resultsManagerRemoveSuccess = True
        if self.resultsManagerTree != None:
            resultsManagerRemoveSuccess = self.resultsManagerTree.removeTree()
        modelManagerRemoveSuccess = True
        if self.modelManagerTree != None:
            modelManagerRemoveSuccess = self.modelManagerTree.removeTree()
        runManagerRemoveSuccess = True
        if self.runManagerTree != None:
            runManagerRemoveSuccess = self.runManagerTree.removeTree()
        dataManagerRemoveSuccess = True
        if self.dataManagerTree != None:
            dataManagerRemoveSuccess = self.dataManagerTree.removeTree()
        dataManagerFileRemoveSuccess = True
        if self.dataManagerFileTree != None:
            dataManagerFileRemoveSuccess = self.dataManagerFileTree.removeTree()

        if resultsManagerRemoveSuccess and modelManagerRemoveSuccess and \
               runManagerRemoveSuccess and dataManagerRemoveSuccess and \
               dataManagerFileRemoveSuccess and \
               generalManagerRemoveSuccess:
            # We have successfully removed the old XML trees

            # Open the XML by first passing to the xml_configuration and letting
            # opus core return the nested XML based on inheritence
            self.xml_file = xml_file
            self.configFile = QFile(xml_file)
            fileNameInfo = QFileInfo(self.xml_file)
            fileName = fileNameInfo.fileName().trimmed()
            fileNamePath = fileNameInfo.absolutePath().trimmed()
            self.opusXMLTree = XMLConfiguration(str(fileName),str(fileNamePath))
            [tempFile,tempFilePath] = tempfile.mkstemp()
            #print tempFile,tempFilePath
            # full_tree is the "whole" tree, inherited nodes and all
            # tree is just the actual file the GUI was asked to open
            self.opusXMLTree.full_tree.write(tempFilePath)
            self.configFileTemp = QFile(tempFilePath)
            if self.configFile and self.configFileTemp:
                self.configFileTemp.open(QIODevice.ReadWrite)
                self.doc = QDomDocument()
                self.doc.setContent(self.configFileTemp)
                self.project_name = self.opusXMLTree.full_tree.getroot().findtext('./general/project_name')
                
                self.opusDataPath = os.path.join(self.opusXMLTree.get_opus_data_path(), self.project_name)
                os.environ['OPUSPROJECTNAME'] = self.project_name
                
                self.generalManagerTree = xmlActionController_General(toolboxbase = self, parentWidget = self.mainwindow.generalmanager_page.layout())
                self.modelManagerTree = xmlActionController_Models(toolboxbase = self, parentWidget = self.mainwindow.modelmanager_page.layout())
                self.runManagerTree = xmlActionController_Scenarios(toolboxbase = self, parentWidget = self.mainwindow.runmanager_page.layout())
                self.dataManagerTree = xmlActionController_Data_tools(toolboxbase = self, parentWidget = self.mainwindow.datamanager_xmlconfig.layout())
                self.resultsManagerTree = xmlActionController_Results(toolboxbase = self, parentWidget = self.mainwindow.resultsmanager_page.layout())
                
                self.dataManagerFileTree = fileActionController_Data_opus_data(self,'data_manager.opus_data',self.opusDataPath,
                                                        self.mainwindow.datamanager_dirview.layout())
                
            else:
                print "Error reading the %s configuration file" % (xml_file)
        else:
            print "There was an error removing the old config"


    def closeXMLTree(self):
        # Try to remove all the old trees...
        if self.generalManagerTree != None:
            generalManagerRemoveSuccess = self.generalManagerTree.removeTree()
        if self.resultsManagerTree != None:
            resultsManagerRemoveSuccess = self.resultsManagerTree.removeTree()
        if self.modelManagerTree != None:
            modelManagerRemoveSuccess = self.modelManagerTree.removeTree()
        if self.runManagerTree != None:
            runManagerRemoveSuccess = self.runManagerTree.removeTree()
        if self.dataManagerTree != None:
            dataManagerRemoveSuccess = self.dataManagerTree.removeTree()
        if self.dataManagerFileTree != None:
            dataManagerFileRemoveSuccess = self.dataManagerFileTree.removeTree()


    def emit_default_gui_configuration_file(self, file_name):
        from opus_core.misc import directory_path_from_opus_path

        default_gui_config_path = os.path.join(directory_path_from_opus_path('opus_gui.main.projects'),
                                               'default_gui_configuration.xml')
        default_gui_config = open(default_gui_config_path)
        new_file = open(file_name, 'w')
        new_file.write(''.join(default_gui_config.readlines()))
        new_file.close()
        default_gui_config.close()
        
        
    def reemit_reinit_default_gui_configuration_file(self):
        self.emit_default_gui_configuration_file(file_name = self.gui_configuration_file)
        self.gui_configuration_doc = QDomDocument()
        self.gui_configuration_doc.setContent(QFile(self.gui_configuration_file))


    def save_gui_configuration_file(self):
        #updates and saves the gui configuration file
        from xml.etree.cElementTree import ElementTree, tostring
        import StringIO
        
        str_io = StringIO.StringIO(self.gui_configuration_doc.toString(2))
        etree = ElementTree(file=str_io)
        etree.write(self.gui_configuration_file)
        str_io.close()
        
