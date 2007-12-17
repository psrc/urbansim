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
from run.opusRunModel import OpusModel
from run.opusRunScript import *

# General system includes
import os, sys,string

  
class XMLTree(object):
  def __init__(self, parent,path,xmlType,parentWidget):
    self.parent = parent.parent
    self.parentTool = parent
    self.path = path
    self.xmlType = xmlType
    self.parentWidget = parentWidget
    self.groupBox = QGroupBox(self.parent)
    self.groupBoxLayout = QVBoxLayout(self.groupBox)
    # Play with the new tree view here
    self.xml_file = path
    self.configFile = QFile(self.xml_file)
    if self.configFile.open(QIODevice.ReadWrite):
      self.doc = QDomDocument()
      self.doc.setContent(self.configFile)
      self.model = OpusDataModel(self.doc, self.parent, self.configFile, self.xmlType, True)
      self.view = QTreeView(self.parent)
      self.delegate = OpusDataDelegate(self.view)
      self.view.setItemDelegate(self.delegate)
      self.view.setModel(self.model)
      self.view.setExpanded(self.model.index(0,0,QModelIndex()),True)
      self.view.setAnimated(True)
      #NEED TO FIX THIS
      self.view.setColumnWidth(0,200)
      self.view.setColumnWidth(1,50)
      self.view.setMinimumHeight(200)
      #self.parentTool.runManagerVBoxLayout.addWidget(self.view)

      self.groupBoxLayout.addWidget(self.view)
      self.groupBox.setTitle(QFileInfo(self.xml_file).filePath())
      #self.parent.gridlayout3.addWidget(self.groupBox)
      self.parentWidget.addWidget(self.groupBox)

      # Hook up to the mousePressEvent and pressed
      self.view.setContextMenuPolicy(Qt.CustomContextMenu)
      QObject.connect(self.view, SIGNAL("customContextMenuRequested(const QPoint &)"), self.processCustomMenu)
      self.removeIcon = QIcon(":/Images/Images/delete.png")
      self.acceptIcon = QIcon(":/Images/Images/accept.png")
      self.applicationIcon = QIcon(":/Images/Images/application_side_tree.png")
      self.bulletIcon = QIcon(":/Images/Images/bullet_black.png")
      self.calendarIcon = QIcon(":/Images/Images/calendar_view_day.png")
      self.actRunModel = QAction(self.acceptIcon, "Run This Model", self.parent)
      QObject.connect(self.actRunModel, SIGNAL("triggered()"), self.runModel)
      self.actRemoveTree = QAction(self.removeIcon, "Remove this tree from the GUI", self.parent)
      QObject.connect(self.actRemoveTree, SIGNAL("triggered()"), self.removeTree)
      self.act2 = QAction(self.applicationIcon, "Action2", self.parent)
      QObject.connect(self.act2, SIGNAL("triggered()"), self.action2)
      self.act3 = QAction(self.bulletIcon, "Action3", self.parent)
      QObject.connect(self.act3, SIGNAL("triggered()"), self.action3)
      self.act4 = QAction(self.calendarIcon, "Action4", self.parent)
      QObject.connect(self.act4, SIGNAL("triggered()"), self.action4)
      self.actOpenXMLFile = QAction(self.calendarIcon, "Open XML File", self.parent)
      QObject.connect(self.actOpenXMLFile, SIGNAL("triggered()"), self.openXMLFile)
      self.actExecScriptFile = QAction(self.calendarIcon, "Exec Script", self.parent)
      QObject.connect(self.actExecScriptFile, SIGNAL("triggered()"), self.execScriptFile)
    else:
      print "Error reading config"

  def runModel(self):
    print "action1 context pressed with column = %s and item = %s" % \
          (self.currentColumn,
           self.currentIndex.internalPointer().node().toElement().attribute(QString("name")))
    # Add the model to the run Q and fire up the GUI
    newModel = OpusModel(self,self.xml_file)
    self.parent.runManagerStuff.addNewModelRun(newModel)
    #self.parent.runManagerStuff.gui.show()

  def removeTree(self):
    print "remove tree pressed with column = %s and item = %s" % \
          (self.currentColumn,
           self.currentIndex.internalPointer().node().toElement().attribute(QString("name")))
    #print "Trying to remove %s group box" % (self.groupBox.title())
    self.groupBox.hide()
    self.parent.parentWidget.removeWidget(self.groupBox)

  def action2(self):
    print "action2 context pressed with column = %s and item = %s" % \
          (self.currentColumn, self.currentIndex.internalPointer().node().toElement().attribute(QString("name")))

  def action3(self):
    print "action3 context pressed with column = %s and item = %s" % \
          (self.currentColumn, self.currentIndex.internalPointer().node().toElement().attribute(QString("name")))

  def action4(self):
    print "action4 context pressed with column = %s and item = %s" % \
          (self.currentColumn, self.currentIndex.internalPointer().node().toElement().attribute(QString("name")))

  def execScriptFile(self):
    print "Exec Script Pressed"
    # First find the script path...
    scriptPath = ""
    if self.currentIndex.internalPointer().parent().node().hasChildNodes():
      children = self.currentIndex.internalPointer().parent().node().childNodes()
      for x in xrange(0,children.count(),1):
        if children.item(x).isElement():
            domElement = children.item(x).toElement()
            if not domElement.isNull():
              if domElement.attribute(QString("name")) == QString("script_path"):
                if domElement.hasChildNodes():
                  children2 = domElement.childNodes()
                  for x2 in xrange(0,children2.count(),1):
                    if children2.item(x2).isText():
                      scriptPath = children2.item(x2).nodeValue()
    if scriptPath != "":
      baseInfo = QFileInfo(self.xml_file)
      baseDir = baseInfo.absolutePath()
      newFile = QString(baseDir).append("/").append(QString(scriptPath))
      sys.path.append(newFile)
      
    filePath = ""
    if self.currentIndex.internalPointer().node().hasChildNodes():
      children = self.currentIndex.internalPointer().node().childNodes()
      for x in xrange(0,children.count(),1):
        if children.item(x).isText():
          filePath = children.item(x).nodeValue()
    #fileInfo = QFileInfo(filePath)
    #baseInfo = QFileInfo(self.xml_file)
    #baseDir = baseInfo.absolutePath()
    #newFile = QFileInfo(QString(baseDir).append("/").append(QString(fileInfo.filePath())))
    print "New File", filePath
    x = OpusScript(self.parent,filePath)
    y = RunScriptThread(self.parent,x)
    y.run()
    
  def openXMLFile(self):
    print "Open File context pressed with column = %s and item = %s" % \
          (self.currentColumn, self.currentIndex.internalPointer().node().toElement().attribute(QString("name")))
    filePath = ""
    if self.currentIndex.internalPointer().node().hasChildNodes():
      children = self.currentIndex.internalPointer().node().childNodes()
      for x in xrange(0,children.count(),1):
        if children.item(x).isText():
          filePath = children.item(x).nodeValue()
    fileInfo = QFileInfo(filePath)
    baseInfo = QFileInfo(self.xml_file)
    baseDir = baseInfo.absolutePath()
    newFile = QFileInfo(QString(baseDir).append("/").append(QString(fileInfo.filePath())))
    #print "Test - ", newFile.absoluteFilePath()
    self.parentTool.openXMLTree(newFile.absoluteFilePath())

  def processCustomMenu(self, position):
    if self.view.indexAt(position).isValid() and self.view.indexAt(position).column() == 0:
      #print "Right mouse click custom menu requested, column %s" % \
      #      (self.view.indexAt(position).column())
      if self.view.indexAt(position).internalPointer().node().nodeValue() != "":
        1+1
        #print "right mouse requested was for ", \
        #      self.view.indexAt(position).internalPointer().node().nodeValue()
      elif self.view.indexAt(position).internalPointer().node().toElement().tagName() != "":
        1+1
        #print "right mouse requested was for ", \
        #      self.view.indexAt(position).internalPointer().node().toElement().tagName()
      titleString = "Context Column %s" % (self.view.indexAt(position).column())
      self.currentColumn = self.view.indexAt(position).column()
      self.currentIndex = self.view.indexAt(position)
      item = self.currentIndex.internalPointer()
      domNode = item.node()
      if domNode.isNull():
        return QVariant()
      # Handle ElementNodes
      if domNode.isElement():
        domElement = domNode.toElement()
        if domElement.isNull():
          return QVariant()
        if domElement.tagName() == QString("scenario_manager"):
          self.menu = QMenu(self.parent)
          if domElement.attribute(QString("executable")) == QString("True"):
            self.menu.addAction(self.actRunModel)
            self.menu.addSeparator()
          self.menu.addAction(self.actRemoveTree)
          self.menu.exec_(QCursor.pos())
        elif domElement.attribute(QString("type")) == QString("file"):
          self.menu = QMenu(self.parent)
          self.menu.addAction(self.actOpenXMLFile)
          self.menu.exec_(QCursor.pos())
        elif domElement.attribute(QString("type")) == QString("script_file"):
          self.menu = QMenu(self.parent)
          self.menu.addAction(self.actExecScriptFile)
          self.menu.exec_(QCursor.pos())
        else:
          self.menu = QMenu(self.parent)
          self.menu.addAction(self.act2)
          self.menu.addSeparator()
          self.menu.addAction(self.act3)
          self.menu.addAction(self.act4)
          self.menu.exec_(QCursor.pos())
    return

# Main console class for the python console
class ToolboxBase(object):
  def __init__(self, parent):
    self.parent = parent

    self.tabWidget = self.parent.tabWidget
    self.toolBox = self.parent.toolBox
    #self.datamanager_tree = self.parent.datamanager_tree
    self.modelmanager_tree = self.parent.modelmanager_tree
    self.resultsmanager_tree = self.parent.resultsmanager_tree
    
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
    self.resultsmanager_tree.resizeColumnToContents(0)

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
