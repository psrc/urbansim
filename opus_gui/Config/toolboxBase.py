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

from Config.opusDataModel import OpusDataModel
from Config.opusDataDelegate import OpusDataDelegate
from Run.opusRunModel import RunModelGui

# General system includes
import os, sys,string

  
# Main console class for the python console
class ToolboxBase(object):
  def __init__(self, parent):
    self.parent = parent

    self.tabWidget = self.parent.tabWidget
    self.toolBox = self.parent.toolBox
    self.datamanager_tree = self.parent.datamanager_tree
    self.modelmanager_tree = self.parent.modelmanager_tree
    self.runmanager_tree = self.parent.runmanager_tree
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

    self.datamanager_tree.resizeColumnToContents(0)
    self.modelmanager_tree.resizeColumnToContents(0)
    self.runmanager_tree.resizeColumnToContents(0)
    self.resultsmanager_tree.resizeColumnToContents(0)

    # Play with the new tree view here
    # find the directory containing the eugene xml configurations
    opus_gui_dir = __import__('opus_gui').__path__[0]
    f = os.path.join(opus_gui_dir, 'projects', 'eugene', 'baseline.xml')
    self.configFile = QFile(f)
    if self.configFile.open(QIODevice.ReadWrite):
      self.doc = QDomDocument()
      self.doc.setContent(self.configFile)
      # Close the file and re-open with truncation
      self.configFile.close()
      self.configFile.open(QIODevice.ReadWrite | QIODevice.Truncate)
      indentSize = 2
      out = QTextStream(self.configFile)
      self.doc.save(out, indentSize)
      self.model = OpusDataModel(self.doc, self.parent, self.configFile)
      self.view = QTreeView(self.parent)
      self.delegate = OpusDataDelegate(self.parent)
      #self.view.setItemDelegate(self.delegate)
      self.view.setModel(self.model)
      self.view.setExpanded(self.model.index(0,0,QModelIndex()),True)
      #NEED TO FIX THIS
      self.parent.gridlayout5.addWidget(self.view)
      self.view.setColumnWidth(0,250)
      # Hook up to the mousePressEvent and pressed
      #QObject.connect(self.view, SIGNAL("pressed(const QModelIndex &)"), self.processPressed)
      self.view.setContextMenuPolicy(Qt.CustomContextMenu)
      QObject.connect(self.view, SIGNAL("customContextMenuRequested(const QPoint &)"), self.processCustomMenu)
      self.acceptIcon = QIcon(":/Images/Images/accept.png")
      self.applicationIcon = QIcon(":/Images/Images/application_side_tree.png")
      self.bulletIcon = QIcon(":/Images/Images/bullet_black.png")
      self.calendarIcon = QIcon(":/Images/Images/calendar_view_day.png")
      self.act1 = QAction(self.acceptIcon, "Run a Model", self.parent)
      QObject.connect(self.act1, SIGNAL("triggered()"), self.action1)
      self.act2 = QAction(self.applicationIcon, "Action2", self.parent)
      QObject.connect(self.act2, SIGNAL("triggered()"), self.action2)
      self.act3 = QAction(self.bulletIcon, "Action3", self.parent)
      QObject.connect(self.act3, SIGNAL("triggered()"), self.action3)
      self.act4 = QAction(self.calendarIcon, "Action4", self.parent)
      QObject.connect(self.act4, SIGNAL("triggered()"), self.action4)
    else:
      print "Error reading config"
    
  def action1(self):
    print "action1 context pressed with column = %s and item = %s" % \
          (self.currentColumn,
           self.currentIndex.internalPointer().node().toElement().attribute(QString("name")))
    flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | \
            Qt.WindowMaximizeButtonHint 
    wnd = RunModelGui(self.parent,flags)
    wnd.show()

  def action2(self):
    print "action2 context pressed with column = %s and item = %s" % \
          (self.currentColumn, self.currentIndex.internalPointer().node().toElement().attribute(QString("name")))

  def action3(self):
    print "action3 context pressed with column = %s and item = %s" % \
          (self.currentColumn, self.currentIndex.internalPointer().node().toElement().attribute(QString("name")))

  def action4(self):
    print "action4 context pressed with column = %s and item = %s" % \
          (self.currentColumn, self.currentIndex.internalPointer().node().toElement().attribute(QString("name")))

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
      self.menu = QMenu(self.parent)
      self.menu.addAction(self.act1)
      self.menu.addAction(self.act2)
      self.menu.addSeparator()
      self.menu.addAction(self.act3)
      self.menu.addAction(self.act4)
      self.menu.exec_(QCursor.pos())
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
