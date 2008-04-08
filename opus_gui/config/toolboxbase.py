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
from PyQt4.QtXml import *

from opus_gui.config.xmltree.opusxmltree import OpusXMLTree
from opus_gui.config.filetree.opusfiletree import OpusFileTree
from opus_core.configurations.xml_configuration import XMLConfiguration

import os,tempfile

# Main class for the toolbox
class ToolboxBase(object):
    def __init__(self, parent):
        self.parent = parent
        self.mainwindow = parent

        # References to some parent main window elements
        self.tabWidget = self.parent.tabWidget
        self.toolBox = self.parent.toolBox

        # Storage for the master copy of the project XML
        self.xml_file = None
        self.doc = None
        self.configFile = None
        self.configFileTemp = None

        # These are the trees that are displayed for each toolbox
        self.view = None
        self.modelManagerTree = None
        self.resultsManagerTree = None
        self.runManagerTree = None
        self.dataManagerTree = None
        self.dataManagerFileTree = None
        self.dataManagerDBSTree = None

        self.gui_configuration_file = os.path.join(os.environ['OPUS_HOME'], 'gui_config.xml')
        if not os.path.exists(self.gui_configuration_file):
            self.emit_default_gui_configuration_file(file_name = self.gui_configuration_file)

        self.gui_configuration_doc = QDomDocument()
        self.gui_configuration_doc.setContent(QFile(self.gui_configuration_file))

    def openXMLTree(self, xml_file):
        saveBeforeOpen = QMessageBox.Discard
        # Check if the current model(s) is(are) dirty first...
        save_string = QString("Current project contains changes... \n"
                              "Should we save or discard those changes before opening?")

        for manager in [self.resultsManagerTree, self.modelManagerTree, self.runManagerTree, self.dataManagerTree]:
            if manager and manager.model.dirty:
                saveBeforeOpen = QMessageBox.question(self.parent,"Warning",
                                                      save_string,
                                                      QMessageBox.Discard,QMessageBox.Save)
                break

        if saveBeforeOpen == QMessageBox.Save:
            self.parent.saveConfig()
        else:
            #if we have an existing tree we need to remove the dirty bit since we are discarding
            if self.runManagerTree:
                self.runManagerTree.model.dirty = False
            if self.dataManagerTree:
                self.dataManagerTree.model.dirty = False
            if self.dataManagerFileTree:
                self.dataManagerFileTree.model.dirty = False
            if self.modelManagerTree:
                self.modelManagerTree.model.dirty = False
            if self.resultsManagerTree:
                self.resultsManagerTree.model.dirty = False

        # Try to remove all the old trees...
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
        dataManagerDBSRemoveSuccess = True
        if self.dataManagerDBSTree != None:
            dataManagerDBSRemoveSuccess = self.dataManagerDBSTree.removeTree()

        if resultsManagerRemoveSuccess and modelManagerRemoveSuccess and \
               runManagerRemoveSuccess and dataManagerRemoveSuccess and \
               dataManagerFileRemoveSuccess and dataManagerDBSRemoveSuccess:
            # We have successfully removed the old XML trees

            # (OLD) Opening a project XML
            #self.xml_file = xml_file
            #self.configFile = QFile(xml_file)
            #if self.configFile.open(QIODevice.ReadWrite):

            # (NEW) Open the XML by first passing to the xml_configuration and letting
            # opus core return the nested XML based on inheritence
            self.xml_file = xml_file
            self.configFile = QFile(xml_file)
            fileNameInfo = QFileInfo(self.xml_file)
            fileName = fileNameInfo.fileName().trimmed()
            fileNamePath = fileNameInfo.absolutePath().trimmed()
            self.opusXMLTree = XMLConfiguration(str(fileName),str(fileNamePath))
            [tempFile,tempFilePath] = tempfile.mkstemp()
            #print tempFile,tempFilePath
            self.opusXMLTree.full_tree.write(tempFilePath)
            self.configFileTemp = QFile(tempFilePath)
            if self.configFile and self.configFileTemp:
                self.configFileTemp.open(QIODevice.ReadWrite)
                self.doc = QDomDocument()
                self.doc.setContent(self.configFileTemp)
                self.opusDataPathOrig = os.getenv("OPUS_DATA_PATH")
                #Then append the cache_directory_root from the modelmanager section of the XML
                cache_dir_root_path = ""
                cache_dir_root_list = self.doc.elementsByTagName(QString("cache_directory_root"))
                if cache_dir_root_list.length() > 0:
                    # We have a dir then we append it
                    cache_dir_root = cache_dir_root_list.item(0)
                    if cache_dir_root.hasChildNodes():
                        children = cache_dir_root.childNodes()
                        for x in xrange(0,children.count(),1):
                            if children.item(x).isText():
                                cache_dir_root_path = "/" + children.item(x).nodeValue()
                self.opusDataPath = self.opusDataPathOrig + cache_dir_root_path
                #print self.opusDataPath
                self.opusDataPath = os.path.normpath(str(self.opusDataPath))
                self.resultsManagerTree = OpusXMLTree(self,"results_manager",
                                                      self.parent.resultsmanager_page.layout())
                self.modelManagerTree = OpusXMLTree(self,"model_manager",
                                                    self.parent.modelmanager_page.layout())
                self.runManagerTree = OpusXMLTree(self,"scenario_manager",
                                                  self.parent.runmanager_page.layout())
                self.dataManagerTree = OpusXMLTree(self,"data_manager",
                                                   self.parent.datamanager_xmlconfig.layout())
                self.dataManagerFileTree = OpusFileTree(self,self.opusDataPath,
                                                        self.parent.datamanager_dirview.layout())
                self.dataManagerDBSTree = OpusXMLTree(self, "project_wide_configurations",
                                                      self.parent.datamanager_dbsconnections.layout())
            else:
                print "Error reading the %s configuration file" % (xml_file)
        else:
            print "There was an error removing the old config"

    def closeXMLTree(self):
        # Try to remove all the old trees...
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
        dataManagerDBSRemoveSuccess = True
        if self.dataManagerDBSTree != None:
            dataManagerDBSRemoveSuccess = self.dataManagerDBSTree.removeTree()

    def emit_default_gui_configuration_file(self, file_name):
        from opus_core.misc import directory_path_from_opus_path

        default_gui_config_path = os.path.join(directory_path_from_opus_path('opus_gui.projects'),
                                               'default_gui_configuration.xml')
        default_gui_config = open(default_gui_config_path)
        new_file = open(file_name, 'w')
        new_file.write(''.join(default_gui_config.readlines()))
        new_file.close()
        default_gui_config.close()
