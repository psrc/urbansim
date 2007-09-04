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

# QGIS bindings for mapping functions
from qgis.core import *
from qgis.gui import *

# Custom Tools

# UI specific includes
from opusMain_ui import Ui_MainWindow

# General system includes
import sys

  
# Main window used for houseing the canvas, toolbars, and dialogs
class OpusGui(QMainWindow, Ui_MainWindow):

  def __init__(self):
    QMainWindow.__init__(self)

    # required by Qt4 to initialize the UI
    self.setupUi(self)

    # We need to initialize the window sizes
    self.splitter.setSizes([150,700])

    debugString = QString("Startup Done...")
    self.statusbar.showMessage(debugString)

    # Build a list of the default list of tabs
    self.tabWidgetList = {}
    for tabIndex in range(self.tabWidget.count()):
      self.tabWidgetList[str(self.tabWidget.widget(tabIndex).objectName())] = \
      self.tabWidget.widget(tabIndex)
    # Init to the first in toolbox by default
    self.toolBoxChanged(0)
    
    QObject.connect(self.toolBox, SIGNAL("currentChanged(int)"),
                    self.toolBoxChanged)
  
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
      self.updateTabs(("tab_detailView","tab_mapView"))
    elif (item.objectName() == "modelmanager_page"):
      # Model Manager
      self.updateTabs(("tab_detailView","tab_mapView","tab_modelFlow"))
    elif (item.objectName() == "runmanager_page"):
      # Run Manager
      self.updateTabs(("tab_detailView","tab_mapView","tab_runStatus"))
    elif (item.objectName() == "resultsmanager_page"):
      # Result Manager
      self.updateTabs(("tab_detailView","tab_mapView","tab_trendView"))

    debugString = QString("toolBoxChanged signal captured - Name = " + item.objectName())
    self.statusbar.showMessage(debugString)
    
