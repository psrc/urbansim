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

from config.opusXMLTree import OpusXMLTree

# Main class for the toolbox
class ToolboxBase(object):
  def __init__(self, parent):
    self.parent = parent

    # References to some parent main window elements
    self.tabWidget = self.parent.tabWidget
    self.toolBox = self.parent.toolBox

    # Storage for the master copy of the project XML
    self.xml_file = None
    self.doc = None
    self.configFile = None
    
    # These are the trees that are displayed for each toolbox
    self.view = None
    self.modelManagerTree = None
    self.resultsManagerTree = None
    self.runManagerTree = None
    self.dataManagerTree = None
  
  def openXMLTree(self, xml_file):
    # Check if the current model(s) is(are) dirty first...
    if self.resultsManagerTree and self.resultsManagerTree.model.dirty:
      QMessageBox.warning(self.parent,"Warning",
                          "Please save changes to current project")
    elif self.modelManagerTree and self.modelManagerTree.model.dirty:
      QMessageBox.warning(self.parent,"Warning",
                          "Please save changes to current project")
    elif self.runManagerTree and self.runManagerTree.model.dirty:
      QMessageBox.warning(self.parent,"Warning",
                          "Please save changes to current project")
    elif self.dataManagerTree and self.dataManagerTree.model.dirty:
      QMessageBox.warning(self.parent,"Warning",
                          "Please save changes to current project")
    else:
        
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

      if resultsManagerRemoveSuccess and modelManagerRemoveSuccess and \
             runManagerRemoveSuccess and dataManagerRemoveSuccess:
        # We have successfully removed the old XML trees
        # Opening a project XML
        self.xml_file = xml_file
        self.configFile = QFile(xml_file)
        if self.configFile.open(QIODevice.ReadWrite):
          self.doc = QDomDocument()
          self.doc.setContent(self.configFile)
          self.resultsManagerTree = OpusXMLTree(self,"results_manager",self.parent.gridlayout4)    
          self.modelManagerTree = OpusXMLTree(self,"model_manager",self.parent.gridlayout2)    
          self.runManagerTree = OpusXMLTree(self,"scenario_manager",self.parent.gridlayout3)    
          self.dataManagerTree = OpusXMLTree(self,"data_manager",self.parent.gridlayout1)
        else:
          print "Error reading config"
      else:
        print "There was an error removing the old config"
