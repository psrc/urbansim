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


class OpusXMLAction_Results(object):
    def __init__(self, parent):
        self.parent = parent
        self.xmlTreeObject = parent.xmlTreeObject
        
        self.currentColumn = None
        self.currentIndex = None
        
        self.acceptIcon = QIcon(":/Images/Images/accept.png")
        self.removeIcon = QIcon(":/Images/Images/delete.png")
        self.calendarIcon = QIcon(":/Images/Images/calendar_view_day.png")
        self.applicationIcon = QIcon(":/Images/Images/application_side_tree.png")

        #create new indicator action (only for my_indicators)
        self.actAddNewIndicator = QAction(self.acceptIcon, 
                                          "Add new indicator",
                                          self.xmlTreeObject.parent)
        QObject.connect(self.actAddNewIndicator, SIGNAL("triggered()"), self.addNewIndicator)

        #create new result template...
        self.actAddNewResultTemplate = QAction(self.acceptIcon, 
                                          "Add new data source...",
                                          self.xmlTreeObject.parent)
        QObject.connect(self.actAddNewResultTemplate, SIGNAL("triggered()"), self.addNewResultTemplate)          
        
        #generate results will enter a dialogue to pair indicators with 
        #result templates and datasets and then run them to produce results
        self.actGenerateResults = QAction(self.acceptIcon, 
                                          "Generate results with...",
                                          self.xmlTreeObject.parent)
        QObject.connect(self.actGenerateResults, SIGNAL("triggered()"), self.generateResults)

        #examine results via some visualization...
        self.actViewResultAsMatplotlibMap = QAction(self.acceptIcon, 
                                          "Map (Matplotlib)",
                                          self.xmlTreeObject.parent)
        QObject.connect(self.actViewResultAsMatplotlibMap, SIGNAL("triggered()"), self.viewResultsMatplotlibMap)                
#        self.actViewResultAsArcgisMap = QAction(self.acceptIcon, 
#                                          "Map (ArcGis)",
#                                          self.xmlTreeObject.parent)
#        QObject.connect(self.actViewResultAsArcgisMap, SIGNAL("triggered()"), self.viewResultsArcGisMap)                

        self.actViewResultAsMatplotlibChart = QAction(self.acceptIcon, 
                                          "Chart (Matplotlib)",
                                          self.xmlTreeObject.parent)
        QObject.connect(self.actViewResultAsMatplotlibChart, SIGNAL("triggered()"), self.viewResultsMatplotlibChart) 
        self.actViewResultAsTablePerYear = QAction(self.acceptIcon, 
                                          "Table (one per year over selected indicators)",
                                          self.xmlTreeObject.parent)
        QObject.connect(self.actViewResultAsTablePerYear, SIGNAL("triggered()"), self.viewResultsTablePerYear) 
        self.actViewResultAsTablePerAttribute = QAction(self.acceptIcon, 
                                          "Table (one per selected indicator)",
                                          self.xmlTreeObject.parent)
        QObject.connect(self.actViewResultAsTablePerAttribute, SIGNAL("triggered()"), self.viewResultsTablePerAttribute) 
        
        #launch advanced view results window...
        self.actViewResultAsAdvanced = QAction(self.acceptIcon, 
                                          "[Advanced configuration]",
                                          self.xmlTreeObject.parent)
        QObject.connect(self.actViewResultAsAdvanced, SIGNAL("triggered()"), self.viewResultsAdvanced) 
        
                
        self.actViewDocumentation = QAction(self.applicationIcon, "View documentation", self.xmlTreeObject.parent)
        QObject.connect(self.actViewDocumentation, SIGNAL("triggered()"), self.viewDocumentation)
        
    def addNewIndicator(self):
        print "addNewIndicator pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())

        model = self.currentIndex.model()
        document = model.domDocument
        name = 'untitled indicator'
        default_value = '?'
        
        newNode = model.create_node(document = document, 
                                    name = name, 
                                    type = 'indicator', 
                                    value = '')
        
        package_node = model.create_node(document = document, 
                                    name = 'package', 
                                    type = 'string', 
                                    value = default_value)
        
        expression_node = model.create_node(document = document, 
                                    name = 'expression', 
                                    type = 'string', 
                                    value = default_value)
        
        model.insertRow(0,
                self.currentIndex,
                newNode)
        
        parent = model.index(0,0,QModelIndex()).parent()
        
        child_index = model.findElementIndexByName(name, parent)[0]
        if child_index.isValid():
            for node in [expression_node, package_node]:
                model.insertRow(0,
                                child_index,
                                node)
        else:
            print "No valid node was found..."
        
        model.emit(SIGNAL("layoutChanged()"))
        
    
    def addNewResultTemplate(self):
        print "addNewResultTemplate pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())
              
    def generateResults(self):
        print "generateResults pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())
        if not self.xmlTreeObject.model.dirty:
            self.xmlTreeObject.parent.resultManagerStuff.addGenerateIndicatorForm()
        else:
            # Prompt the user to save...
            QMessageBox.warning(self.xmlTreeObject.parent,
                                "Warning",
                                "Please save changes to project before generating results")
    
    def viewResultsMatplotlibMap(self):
        clicked_node = self.currentIndex.internalPointer().node().toElement()          
        self.xmlTreeObject.parent.resultManagerStuff.addIndicatorForm(
                                                          indicator_type = 'matplotlib_map',
                                                          clicked_node = clicked_node)

    def viewResultsArcGisMap(self):
        clicked_node = self.currentIndex.internalPointer().node().toElement()          
        self.xmlTreeObject.parent.resultManagerStuff.addIndicatorForm(
                                                          indicator_type = 'arcgis_map',
                                                          clicked_node = clicked_node)           
    def viewResultsMatplotlibChart(self):
        clicked_node = self.currentIndex.internalPointer().node().toElement()           
        self.xmlTreeObject.parent.resultManagerStuff.addIndicatorForm(
                                                          indicator_type = 'matplotlib_chart',
                                                          clicked_node = clicked_node)
      
    def viewResultsTablePerAttribute(self):
        clicked_node = self.currentIndex.internalPointer().node().toElement()           
        self.xmlTreeObject.parent.resultManagerStuff.addIndicatorForm(
                                                          indicator_type = 'table_per_attribute',
                                                          clicked_node = clicked_node)
        
    def viewResultsTablePerYear(self):
        clicked_node = self.currentIndex.internalPointer().node().toElement()           
        self.xmlTreeObject.parent.resultManagerStuff.addIndicatorForm(
                                                          indicator_type = 'table_per_year',
                                                          clicked_node = clicked_node)

    def viewDocumentation(self):
        pass
        
    def viewResultsAdvanced(self):
        print "viewResultsAdvanced pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())                  
        if not self.xmlTreeObject.model.dirty:
            self.xmlTreeObject.parent.resultManagerStuff.addAdvancedVisualizationForm()
        else:
            # Prompt the user to save...
            QMessageBox.warning(self.xmlTreeObject.parent,
                                "Warning",
                                "Please save changes to project before generating results")
                        
    def processCustomMenu(self, position):
        if self.xmlTreeObject.view.indexAt(position).isValid() and \
               self.xmlTreeObject.view.indexAt(position).column() == 0:
            self.currentColumn = self.xmlTreeObject.view.indexAt(position).column()
            self.currentIndex = self.xmlTreeObject.view.indexAt(position)
            item = self.currentIndex.internalPointer()
            domNode = item.node()
            if domNode.isNull():
                return
            # Handle ElementNodes
            if domNode.isElement():
                domElement = domNode.toElement()
                if domElement.isNull():
                    return
                if domElement.attribute(QString("type")) == QString("indicator_library") and \
                   domElement.attribute(QString("append_to")) == QString("True"):
                    self.menu = QMenu(self.xmlTreeObject.parent)
                    self.menu.addAction(self.actAddNewIndicator)
                    self.menu.exec_(QCursor.pos())
                    
                elif domElement.attribute(QString("type")) == QString("source_data"):
                    self.menu = QMenu(self.xmlTreeObject.parent)
                    self.menu.addAction(self.actGenerateResults)
                    self.menu.exec_(QCursor.pos())

                elif domElement.attribute(QString("type")) == QString("all_source_data"):
                    self.menu = QMenu(self.xmlTreeObject.parent)
                    self.menu.addAction(self.actAddNewResultTemplate)
                    self.menu.exec_(QCursor.pos())
                                                 
                elif domElement.attribute(QString("type")) == QString("indicator"):
                    self.menu = QMenu(self.xmlTreeObject.parent)
                    self.menu.addAction(self.actViewDocumentation)
                    self.menu.addAction(self.actGenerateResults)
                    self.menu.exec_(QCursor.pos())
                    
                elif domElement.attribute(QString("type")) == QString("indicator_result"):
                    self.menu = QMenu(self.xmlTreeObject.parent)
                    visualization_menu = QMenu(self.xmlTreeObject.parent)
                    visualization_menu.setTitle(QString("View result as..."))

                    visualization_menu.addAction(self.actViewResultAsTablePerYear)
                    visualization_menu.addAction(self.actViewResultAsTablePerAttribute)                    
                    visualization_menu.addAction(self.actViewResultAsMatplotlibMap)
#                    visualization_menu.addAction(self.actViewResultAsArcgisMap)
                    visualization_menu.addAction(self.actViewResultAsMatplotlibChart)
                    visualization_menu.addAction(self.actViewResultAsAdvanced)
                    
                    self.menu.addMenu(visualization_menu)
                    self.menu.exec_(QCursor.pos())

        return


