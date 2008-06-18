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

from opus_gui.config.managerbase.cloneinherited import CloneInheritedGui
from opus_gui.config.managerbase.clonenode import CloneNodeGui
from opus_gui.results.xml_helper_methods import elementsByAttributeValue, get_child_values
from opus_gui.results.xml_helper_methods import ResultsManagerXMLHelper


class OpusXMLAction_Results(object):
    def __init__(self, opusXMLAction):
        self.opusXMLAction = opusXMLAction
        self.mainwindow = opusXMLAction.mainwindow
        self.xmlTreeObject = opusXMLAction.xmlTreeObject
        self.toolboxStuff = self.xmlTreeObject.mainwindow.toolboxStuff
        self.xml_helper = ResultsManagerXMLHelper(toolboxStuff = self.toolboxStuff)

        self.currentColumn = None
        self.currentIndex = None

        self.acceptIcon = QIcon(":/Images/Images/accept.png")
        self.removeIcon = QIcon(":/Images/Images/delete.png")
        self.calendarIcon = QIcon(":/Images/Images/calendar_view_day.png")
        self.applicationIcon = QIcon(":/Images/Images/application_side_tree.png")
        self.cloneIcon = QIcon(":/Images/Images/application_double.png")
        self.makeEditableIcon = QIcon(":/Images/Images/application_edit.png")

        #create new indicator action (only for my_indicators)
        self.actAddNewIndicator = QAction(self.acceptIcon, 
                                          "Add new indicator",
                                          self.xmlTreeObject.mainwindow)
        QObject.connect(self.actAddNewIndicator, SIGNAL("triggered()"), self.addNewIndicator)

        #create new result template...
        self.actAddNewIndicatorGroup = QAction(self.acceptIcon, 
                                          "Add new indicator group...",
                                          self.xmlTreeObject.mainwindow)
        QObject.connect(self.actAddNewIndicatorGroup, SIGNAL("triggered()"), self.addNewIndicatorGroup)          

        #generate results will enter a dialogue to pair indicators with 
        #result templates and datasets and then run them to produce results
        self.actGenerateResults = QAction(self.acceptIcon, 
                                          "Generate results with...",
                                          self.xmlTreeObject.mainwindow)
        QObject.connect(self.actGenerateResults, SIGNAL("triggered()"), self.generateResults)

        #examine results via some visualization...
        self.actViewResultAsMatplotlibMap = QAction(self.acceptIcon, 
                                          "Map (Matplotlib)",
                                          self.xmlTreeObject.mainwindow)
        QObject.connect(self.actViewResultAsMatplotlibMap, SIGNAL("triggered()"), self.viewResultsMatplotlibMap)                
        #self.actViewResultAsArcgisMap = QAction(self.acceptIcon, 
        #                                  "Map (ArcGis)",
        #                                  self.xmlTreeObject.mainwindow)
        #QObject.connect(self.actViewResultAsArcgisMap, SIGNAL("triggered()"), self.viewResultsArcGisMap)                

        self.actViewResultAsMatplotlibChart = QAction(self.acceptIcon, 
                                          "Chart (Matplotlib)",
                                          self.xmlTreeObject.mainwindow)
        QObject.connect(self.actViewResultAsMatplotlibChart, SIGNAL("triggered()"), self.viewResultsMatplotlibChart) 
#        self.actViewResultAsTablePerYear = QAction(self.acceptIcon, 
#                                          "Table (one per year over selected indicators)",
#                                          self.xmlTreeObject.mainwindow)
        #QObject.connect(self.actViewResultAsTablePerYear, SIGNAL("triggered()"), self.viewResultsTablePerYear) 
        self.actViewResultAsTablePerAttribute = QAction(self.acceptIcon, 
                                          "Table",
                                          self.xmlTreeObject.mainwindow)
        QObject.connect(self.actViewResultAsTablePerAttribute, SIGNAL("triggered()"), self.viewResultsTablePerAttribute) 

        #launch advanced view results window...
        self.actViewResultAsAdvanced = QAction(self.acceptIcon, 
                                          "Advanced visualization...",
                                          self.xmlTreeObject.mainwindow)
        QObject.connect(self.actViewResultAsAdvanced, SIGNAL("triggered()"), self.viewResultsAdvanced) 


#        self.actViewDocumentation = QAction(self.applicationIcon, "View documentation", self.xmlTreeObject.mainwindow)
#        QObject.connect(self.actViewDocumentation, SIGNAL("triggered()"), self.viewDocumentation)

        self.actRemoveNode = QAction(self.removeIcon,
                                     "Remove Node",
                                     self.xmlTreeObject.mainwindow)
        QObject.connect(self.actRemoveNode,
                        SIGNAL("triggered()"),
                        self.removeNode)

        self.actMakeEditable = QAction(self.makeEditableIcon,
                                       "Make Editable",
                                       self.xmlTreeObject.mainwindow)
        QObject.connect(self.actMakeEditable,
                        SIGNAL("triggered()"),
                        self.makeEditableAction)

        self.actCloneNode = QAction(self.cloneIcon,
                                    "Copy Node",
                                    self.xmlTreeObject.mainwindow)
        QObject.connect(self.actCloneNode,
                        SIGNAL("triggered()"),
                        self.cloneNode)


    def addNewIndicator(self):
        print "addNewIndicator pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())

        self.xml_helper.addNewIndicator(indicator_name = 'untitled indicator', 
                                        package_name = '?', 
                                        expression = '?')

    def addNewIndicatorGroup(self):
        print "addNewIndicatorGroup pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())
              
        self.xml_helper.addNewIndicatorGroup(group_name = 'untitled indicator group')
        
    def beforeAddIndicatorToGroupShown(self):
        print "AddIndicatorToGroup about to be shown"

        #group_name = self.currentIndex.internalPointer().node().toElement().tagName()
        #existing_indicators = self.xml_helper.get_indicators_in_indicator_group(group_name)
        
        available_indicators = self.xml_helper.get_available_indicator_names()
        
        self.indicator_group_menu.clear()
        for indicator_info in available_indicators:
            indicator_name = indicator_info['name']
#            if indicator_name in existing_indicators:
#                continue
            indicator = QString(indicator_name)
            act_indicator = QAction(self.acceptIcon, 
                                    indicator_name,
                                    self.indicator_group_menu)
            callback = lambda indicator=indicator: self.addIndicatorToGroup(indicator)
            QObject.connect(act_indicator, SIGNAL("triggered()"), callback) 
            self.indicator_group_menu.addAction(act_indicator)
            
    def addIndicatorToGroup(self, indicator):
        print "adding indicator to group..."
        print "addIndicatorToGroup pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())
        group_name = self.currentIndex.internalPointer().node().toElement().tagName()
        self.xml_helper.addIndicatorToGroup(group_name = group_name, 
                                            indicator_name = indicator)
        
    def beforeRunIndicatorGroupShown(self):
        print "AddIndicatorToGroup about to be shown"
        
        domDocument = self.xmlTreeObject.mainwindow.toolboxStuff.doc
        node_list = elementsByAttributeValue(domDocument = domDocument, 
                                              attribute = 'type', 
                                              value = 'source_data')
        
        self.run_indicator_group_menu.clear()
        for element, node in node_list:
            simulation_run = QString(element.nodeName())
            act_simulation_run = QAction(self.acceptIcon, 
                                    element.nodeName(),
                                    self.run_indicator_group_menu)
            callback = lambda simulation_run=simulation_run: self.indicatorGroupRun(simulation_run)
            QObject.connect(act_simulation_run, SIGNAL("triggered()"), callback) 
            self.run_indicator_group_menu.addAction(act_simulation_run)
                
    def indicatorGroupRun(self, simulation_run):
        print "indicatorGroupRun pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())
        if not self.xmlTreeObject.model.isDirty():
            self.xmlTreeObject.mainwindow.resultManagerStuff.addRunIndicatorGroupForm(
                selected_item = self.currentIndex.internalPointer().node().toElement().tagName(),
                simulation_run = simulation_run)
        else:
            # Prompt the user to save...
            QMessageBox.warning(self.xmlTreeObject.mainwindow,
                                "Warning",
                                "Please save changes to project before generating results")
                      
    def generateResults(self):
        print "generateResults pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())
        if not self.xmlTreeObject.model.isDirty():
            self.xmlTreeObject.mainwindow.resultManagerStuff.addGenerateIndicatorForm(
                selected_item = self.currentIndex.internalPointer().node().toElement().tagName())
        else:
            # Prompt the user to save...
            QMessageBox.warning(self.xmlTreeObject.mainwindow,
                                "Warning",
                                "Please save changes to project before generating results")

    def _viewIndicatorVisualization(self, indicator_type):
        indicator_name = self.currentIndex.internalPointer().node().toElement().tagName()        
        self.xmlTreeObject.mainwindow.resultManagerStuff.addIndicatorForm(
                                                          indicator_type = indicator_type,
                                                          indicator_names = [indicator_name])


    def viewResultsMatplotlibMap(self):
        self._viewIndicatorVisualization(indicator_type = 'matplotlib_map')

    def viewResultsArcGisMap(self):
        self._viewIndicatorVisualization(indicator_type = 'arcgis_map')
         
    def viewResultsMatplotlibChart(self):
        self._viewIndicatorVisualization(indicator_type = 'matplotlib_chart')

    def viewResultsTablePerAttribute(self):
        self._viewIndicatorVisualization(indicator_type = 'table_per_attribute')

    def viewResultsTablePerYear(self):
        self._viewIndicatorVisualization(indicator_type = 'table_per_year')

    def viewDocumentation(self):
        pass

    def viewResultsAdvanced(self):
        print "viewResultsAdvanced pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())                  
        if not self.xmlTreeObject.model.isDirty():
            self.xmlTreeObject.mainwindow.resultManagerStuff.addAdvancedVisualizationForm()
        else:
            # Prompt the user to save...
            QMessageBox.warning(self.xmlTreeObject.mainwindow,
                                "Warning",
                                "Please save changes to project before generating results")

    def removeNode(self):
        #print "Remove Node Pressed"
        self.currentIndex.model().removeRow(self.currentIndex.internalPointer().row(),
                                            self.currentIndex.model().parent(self.currentIndex))
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def cloneNode(self):
        #print "cloneNode Pressed"
        clone = self.currentIndex.internalPointer().domNode.cloneNode()
        parentIndex = self.currentIndex.model().parent(self.currentIndex)
        model = self.currentIndex.model()
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        window = CloneNodeGui(self,flags,clone,parentIndex,model)
        window.show()

    def makeEditableAction(self):
        thisNode = self.currentIndex.internalPointer().node()
        self.currentIndex.model().makeEditable(thisNode)
        # Finally we refresh the tree to indicate that there has been a change
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def processCustomMenu(self, position):
        if self.xmlTreeObject.view.indexAt(position).isValid() and \
               self.xmlTreeObject.view.indexAt(position).column() == 0:
            self.currentColumn = self.xmlTreeObject.view.indexAt(position).column()
            self.currentIndex = self.xmlTreeObject.view.indexAt(position)
            parentElement = None
            parentIndex = self.currentIndex.model().parent(self.currentIndex)
            if parentIndex and parentIndex.isValid():
                parentNode = parentIndex.internalPointer().node()
                parentElement = parentNode.toElement()
            item = self.currentIndex.internalPointer()
            domNode = item.node()
            if domNode.isNull():
                return
            # Handle ElementNodes
            if domNode.isElement():
                domElement = domNode.toElement()
                if domElement.isNull():
                    return
                
                self.menu = QMenu(self.xmlTreeObject.mainwindow)
                if domElement.attribute(QString("type")) == QString("indicator_library") and \
                       domElement.attribute(QString("append_to")) == QString("True"):
                    self.menu.addAction(self.actAddNewIndicator)
                elif domElement.attribute(QString("type")) == QString("source_data"):
                    self.menu.addAction(self.actGenerateResults)
                elif domElement.tagName() == QString("Indicator_groups"):
                    self.menu.addAction(self.actAddNewIndicatorGroup)
                elif domElement.attribute(QString("type")) == QString("indicator"):
#                    self.menu.addAction(self.actViewDocumentation)
                    self.menu.addAction(self.actGenerateResults)
                elif domElement.attribute(QString("type")) == QString("indicator_result"):
                    visualization_menu = QMenu(self.xmlTreeObject.mainwindow)
                    visualization_menu.setTitle(QString("View result as..."))
                    #visualization_menu.addAction(self.actViewResultAsTablePerYear)
                    visualization_menu.addAction(self.actViewResultAsTablePerAttribute)                    
                    visualization_menu.addAction(self.actViewResultAsMatplotlibMap)
                    #visualization_menu.addAction(self.actViewResultAsArcgisMap)
                    visualization_menu.addAction(self.actViewResultAsMatplotlibChart)
                    visualization_menu.addAction(self.actViewResultAsAdvanced)
                    self.menu.addMenu(visualization_menu)
                    
                elif domElement.attribute(QString("type")) == QString("indicator_group"):
                    self._build_indicator_group_menu()
                    
                    
                if self.menu:
                    # Last minute chance to add items that all menues should have
                    if domElement.hasAttribute(QString("inherited")):
                        # Tack on a make editable if the node is inherited
                        self.menu.addSeparator()
                        self.menu.addAction(self.actMakeEditable)
                    else:
                        if domElement.hasAttribute(QString("copyable")) and \
                               domElement.attribute(QString("copyable")) == QString("True"):
                            self.menu.addSeparator()
                            self.menu.addAction(self.actCloneNode)
                        if parentElement and (not parentElement.isNull()) and \
                               parentElement.hasAttribute(QString("type")) and \
                               ((parentElement.attribute(QString("type")) == QString("dictionary")) or \
                                (parentElement.attribute(QString("type")) == QString("selectable_list")) or \
                                (parentElement.attribute(QString("type")) == QString("list"))):
                            self.menu.addSeparator()
                            self.menu.addAction(self.actRemoveNode)
                # Check if the menu has any elements before exec is called
                if not self.menu.isEmpty():
                    self.menu.exec_(QCursor.pos())
        return

    def _build_indicator_group_menu(self):
        #needs to be called when indicator_group right clicked on...
        self.indicator_group_menu = QMenu(self.xmlTreeObject.mainwindow)
        self.indicator_group_menu.setTitle(QString("Add indicator to group..."))
        QObject.connect(self.indicator_group_menu, SIGNAL('aboutToShow()'), self.beforeAddIndicatorToGroupShown)
        self.menu.addMenu(self.indicator_group_menu)

        
        self.run_indicator_group_menu = QMenu(self.xmlTreeObject.mainwindow)
        self.run_indicator_group_menu.setTitle(QString('Run indicator group on...'))
        QObject.connect(self.run_indicator_group_menu, SIGNAL('aboutToShow()'), self.beforeRunIndicatorGroupShown)
        
        self.menu.addMenu(self.run_indicator_group_menu)
