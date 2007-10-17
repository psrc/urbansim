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

# QGIS bindings for mapping functions
from qgis.core import *
from qgis.gui import *

# Custom Tools

# UI specific includes
from opusMain_ui import Ui_MainWindow
from Util.pythonGui import OpusPythonShell
from Config.opusDataModel import OpusDataModel
# General system includes
import sys

  
# Main window used for houseing the canvas, toolbars, and dialogs
class OpusGui(QMainWindow, Ui_MainWindow):

  def __init__(self):
    QMainWindow.__init__(self)
    
    # required by Qt4 to initialize the UI
    self.setupUi(self)
    
    # We need to initialize the window sizes
    self.splitter.setSizes([350,500])
    
    # create map canvas
    self.canvas = QgsMapCanvas(self.widgetMap)
    self.canvas.setCanvasColor(Qt.yellow)
    self.canvas.enableAntiAliasing(True)
    self.canvas.useQImageToRender(False)
    self.canvas.show()
    self.canvas.parentWin = self
    debugString = QString("Finished Loading Canvas...")
    self.statusbar.showMessage(debugString)
    
    # lay our widgets out in the main window
    self.layout = QVBoxLayout(self.widgetMap)
    self.layout.addWidget(self.canvas)

    # Link in the map tools
    QObject.connect(self.mpActionZoomIn, SIGNAL("triggered()"), self.zoomIn)
    QObject.connect(self.mpActionZoomOut, SIGNAL("triggered()"), self.zoomOut)
    QObject.connect(self.mpActionPan, SIGNAL("triggered()"), self.pan)

    # Map tools
    self.toolPan = QgsMapToolPan(self.canvas)
    self.toolPan.setAction(self.mpActionPan)
    self.toolZoomIn = QgsMapToolZoom(self.canvas, False)
    self.toolZoomIn.setAction(self.mpActionZoomIn)
    self.toolZoomOut = QgsMapToolZoom(self.canvas, True)
    self.toolZoomOut.setAction(self.mpActionZoomOut)
    
    ##### Lets test out a simple map
    self.layers = []
    f = "Data/st99_d00.shp"
    f_string = QString(f)
    info = QFileInfo(QString(f))
    
    # create layer
    layer = QgsVectorLayer(QString(f), info.completeBaseName(), "ogr")
    
    if not layer.isValid():
      # Deal with the error
      debugString = QString("Error Loading Layer...")
      self.statusbar.showMessage(debugString)
      return
    QgsMapLayerRegistry.instance().addMapLayer(layer)
    
    # set extent to the extent of our layer
    self.canvas.setExtent(layer.extent())
    
    # Set the transparency for the layer
    #layer.setTransparency(190)
    
    # set the map canvas layer set
    cl = QgsMapCanvasLayer(layer)
    self.layers.insert(0,cl)
    self.canvas.setLayerSet(self.layers)
    
    self.pythonGui = OpusPythonShell(self.pythonWidget,self.pythonLineEdit,self.__dict__)
    self.pythonLayout = QGridLayout(self.pythonWidget)
    self.pythonLayout.setMargin(9)
    self.pythonLayout.setSpacing(6)
    self.pythonLayout.setObjectName("pythonLayout")
    self.pythonLayout.addWidget(self.pythonGui)
    
    debugString = QString("Startup Done...")
    #self.statusbar.showMessage(debugString)

    # Build a list of the default list of tabs
    self.tabWidgetList = {}
    for tabIndex in range(self.tabWidget.count()):
      self.tabWidgetList[str(self.tabWidget.tabText(tabIndex))] = \
      self.tabWidget.widget(tabIndex)
    # Init to the first in toolbox by default
    self.toolBoxChanged(0)
    
    QObject.connect(self.toolBox, SIGNAL("currentChanged(int)"),
                    self.toolBoxChanged)

    self.datamanager_tree.resizeColumnToContents(0)
    self.modelmanager_tree.resizeColumnToContents(0)
    self.runmanager_tree.resizeColumnToContents(0)
    self.resultsmanager_tree.resizeColumnToContents(0)

    # Play with the new tree view here
    self.configFile = QFile("./config.xml")
    if self.configFile.open(QIODevice.ReadWrite):
      self.doc = QDomDocument()
      self.doc.setContent(self.configFile)
      # Close the file and re-open with truncation
      self.configFile.close()
      self.configFile.open(QIODevice.ReadWrite | QIODevice.Truncate)
      indentSize = 2
      out = QTextStream(self.configFile)
      self.doc.save(out, indentSize)
      self.model = OpusDataModel(self.doc, self)
      self.view = QTreeView(self)
      self.view.setModel(self.model)
      self.gridlayout5.addWidget(self.view)
      self.view.setColumnWidth(0,250)
      # Hook up to the mousePressEvent and pressed
      QObject.connect(self.view, SIGNAL("pressed(const QModelIndex &)"), self.processPressed)
      self.view.setContextMenuPolicy(Qt.CustomContextMenu)
      QObject.connect(self.view, SIGNAL("customContextMenuRequested(const QPoint &)"), self.processCustomMenu)
    else:
      print "Error reading config"
    

  def processCustomMenu(self, position):
    print "Right mouse click custom menu requested"
    if self.view.indexAt(position).isValid():
      if self.view.indexAt(position).internalPointer().node().nodeValue() != "":
        print "right mouse requested was for ", self.view.indexAt(position).internalPointer().node().nodeValue()
      elif self.view.indexAt(position).internalPointer().node().toElement().tagName() != "":
        print "right mouse requested was for ", self.view.indexAt(position).internalPointer().node().toElement().tagName()
    return
  
  def processPressed(self, index):
    print "Pressed Event Captured"
    if index.isValid():
      if index.internalPointer().node().nodeValue() != "":
        print "left mouse requested was for ", index.internalPointer().node().nodeValue()
      elif index.internalPointer().node().toElement().tagName() != "":
        print "left mouse requested was for ", index.internalPointer().node().toElement().tagName()
    return

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
    
  # Signal handeler for zoom in button
  def zoomIn(self):
    self.canvas.setMapTool(self.toolZoomIn)

  # Signal handeler for zoom out button
  def zoomOut(self):
    self.canvas.setMapTool(self.toolZoomOut)

  # Signal handeler for pan button
  def pan(self):
    self.canvas.setMapTool(self.toolPan)
