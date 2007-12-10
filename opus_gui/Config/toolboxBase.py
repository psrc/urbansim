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

from Config.opusDataItem import OpusDataItem
from Config.opusDataModel import OpusDataModel
from Config.opusDataDelegate import OpusDataDelegate
#from Run.opusRunGui import RunModelGui
from Run.opusRunModel import OpusModel
from Run.opusRunScript import *

# General system includes
import os, sys,string


from inprocess.travis.opus_gui.Config.XMLTree import XMLTree
from inprocess.travis.opus_gui.Config.ResultsXMLTree import ResultsXMLTree      
      
# Main console class for the python console
class ToolboxBase(object):
  def __init__(self, parent):
    self.parent = parent

    self.tabWidget = self.parent.tabWidget
    self.toolBox = self.parent.toolBox
    #self.datamanager_tree = self.parent.datamanager_tree
    self.modelmanager_tree = self.parent.modelmanager_tree
    #self.resultsmanager_tree = self.parent.resultsmanager_tree
    
    # Build a list of the default list of tabs
    self.tabWidgetList = {}
    for tabIndex in range(self.tabWidget.count()):
      self.tabWidgetList[str(self.tabWidget.tabText(tabIndex))] = \
      self.tabWidget.widget(tabIndex)
    # Init to the first in toolbox by default
    self.toolBoxChanged(0)
    
    QObject.connect(self.toolBox, SIGNAL("currentChanged(int)"),
                    self.toolBoxChanged)

    #self.datamanager_tree.resizeColumnToContents(0)
    self.modelmanager_tree.resizeColumnToContents(0)
    #self.resultsmanager_tree.resizeColumnToContents(0)

    self.view = None
    self.runManagerTrees = []
    self.dataManagerTrees = []
    #self.runManagerTreeContainer = QScrollArea(self.parent)
    #self.runManagerVBoxLayout = QVBoxLayout(self.runManagerTreeContainer)
    #self.runManagerVBoxLayout.setObjectName("runManagerVBoxLayout")
    #self.parent.gridlayout3.addWidget(self.runManagerTreeContainer)

  def openXMLDirTree(self, xml_dir):
    pass
  
  def openXMLTree(self, xml_file):
    self.runManagerTrees.append(XMLTree(self,xml_file,"scenario_manager",self.parent.gridlayout3))    
    self.dataManagerTrees.append(XMLTree(self,xml_file,"data_manager",self.parent.gridlayout1))    
    
    self.parent.resultsmanager_tree = ResultsXMLTree(self, xml_file, "results_manager", self.parent.gridlayout4)
    self.resultsmanager_tree = self.parent.resultsmanager_tree
    
  def updateTabs(self, listOfTabs):
    # Here we can update to show current tabs
    for index in range(self.tabWidget.count()):
      self.tabWidget.removeTab(0)      
    for tab in listOfTabs:
      if tab in self.tabWidgetList:
        self.tabWidget.addTab(self.tabWidgetList.get(tab),tab)
    
  def toolBoxChanged(self, index):
    # Here we can add and remove tabs from the right side gui as the toolbox
    # items are changed
    # Switch on the toolbox item
    item = self.toolBox.widget(index)
    if (item.objectName() == "datamanager_page"):
      # Data Manager
      self.updateTabs(("Editor","Map View","Python Console","Log View"))
      #self.updateTabs(("tab_editorView","tab_mapView","tab_pythonView","tab_logView"))
    elif (item.objectName() == "modelmanager_page"):
      # Model Manager
      self.updateTabs(("Editor","Map View","Python Console","Log View"))
      #self.updateTabs(("tab_editorView","tab_mapView","tab_pythonView","tab_logView"))
    elif (item.objectName() == "runmanager_page"):
      # Run Manager
      self.updateTabs(("Editor","Map View","Python Console","Log View"))
      #self.updateTabs(("tab_editorView","tab_mapView","tab_pythonView","tab_logView"))
    elif (item.objectName() == "resultsmanager_page"):
      # Result Manager
      self.updateTabs(("Map View","Python Console","Log View"))
      #self.updateTabs(("tab_mapView","tab_pythonView","tab_logView"))

    #debugString = QString("toolBoxChanged signal captured - Name = " + item.objectName())
    #self.statusbar.showMessage(debugString)
