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
from opus_gui.results.xml_helper_methods import elementsByAttributeValue
from opus_gui.results.xml_helper_methods import ResultsManagerXMLHelper
from opus_gui.results.forms.get_run_info import GetRunInfo


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

        #edit indicator action
        self.actEditIndicator = QAction(self.acceptIcon,
                                          "Edit indicator",
                                          self.xmlTreeObject.mainwindow)
        QObject.connect(self.actEditIndicator,
                        SIGNAL("triggered()"),
                        self.editIndicator)
        
        #create new result template...
        self.actAddNewIndicatorBatch = QAction(self.acceptIcon, 
                                          "Add new indicator batch...",
                                          self.xmlTreeObject.mainwindow)
        QObject.connect(self.actAddNewIndicatorBatch, SIGNAL("triggered()"), self.addNewIndicatorBatch)          

        self.actConfigureExistingBatchIndicatorVisualization = QAction(self.acceptIcon,
                                                                       "Configure visualization",
                                                                       self.xmlTreeObject.mainwindow)
        QObject.connect(self.actConfigureExistingBatchIndicatorVisualization, SIGNAL("triggered()"), self.configureExistingBatchIndicatorVisualization)
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

        self.actGetInfoSimulationRuns = QAction(self.acceptIcon, 
                                          "Show details",
                                          self.xmlTreeObject.mainwindow)
        QObject.connect(self.actGetInfoSimulationRuns, SIGNAL("triggered()"), self.getInfoSimulationRuns) 


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
        
        self.editIndicator(already_exists = False)

    def editIndicator(self, already_exists = True):

        if self.xmlTreeObject.model.isDirty():
            # Prompt the user to save...
            QMessageBox.warning(self.xmlTreeObject.mainwindow,
                                "Warning",
                                "Please save changes to project before generating results")               
            return 

        if already_exists:
            currentIndex = self.currentIndex
        else:
            currentIndex = None
                        
        self.xmlTreeObject.mainwindow.resultManagerStuff.editIndicator(
            selected_index = currentIndex)
        
        
    def addNewIndicatorBatch(self):
        print "addNewIndicatorBatch pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())
              
        self.xml_helper.addNewIndicatorBatch(batch_name = 'untitled_indicator_batch')
        
    def beforeAddIndicatorToBatchShown(self):
        print "AddIndicatorToBatch about to be shown"

        #batch_name = self.currentIndex.internalPointer().node().toElement().tagName()
        #existing_indicators = self.xml_helper.get_indicators_in_indicator_batch(batch_name)
        
        available_indicators = self.xml_helper.get_available_indicator_names()
        
        self.indicator_batch_menu.clear()
        for indicator_info in available_indicators:
            indicator_name = indicator_info['name']
#            if indicator_name in existing_indicators:
#                continue
            indicator = QString(indicator_name)
            act_indicator = QAction(self.acceptIcon, 
                                    indicator_name,
                                    self.indicator_batch_menu)
            callback = lambda indicator=indicator: self.addIndicatorToBatch(indicator)
            QObject.connect(act_indicator, SIGNAL("triggered()"), callback) 
            self.indicator_batch_menu.addAction(act_indicator)
            
    def addIndicatorToBatch(self, indicator):
        print "adding indicator to batch..."
        print "addIndicatorToBatch pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())
        batch_name = self.currentIndex.internalPointer().node().toElement().tagName()
        self.xml_helper.addIndicatorToBatch(batch_name = batch_name, 
                                            indicator_name = indicator)
        
    def configureNewBatchIndicatorVisualization(self, viz):
        if self.xmlTreeObject.model.isDirty():
            # Prompt the user to save...
            QMessageBox.warning(self.xmlTreeObject.mainwindow,
                                "Warning",
                                "Please save changes to project")               
            return 

        batch_name = self.currentIndex.internalPointer().node().toElement().tagName()
        self.xmlTreeObject.mainwindow.resultManagerStuff.configureNewIndicatorBatchVisualization(
            visualization_type = viz,
            batch_name = batch_name)

    def configureExistingBatchIndicatorVisualization(self):
        if self.xmlTreeObject.model.isDirty():
            # Prompt the user to save...
            QMessageBox.warning(self.xmlTreeObject.mainwindow,
                                "Warning",
                                "Please save changes to project")               
            return 

        self.xmlTreeObject.mainwindow.resultManagerStuff.configureExistingIndicatorBatchVisualization(
            selected_index = self.currentIndex)      
          
    def beforeRunIndicatorBatchShown(self):
        print "AddIndicatorToBatch about to be shown"
        
        domDocument = self.xmlTreeObject.mainwindow.toolboxStuff.doc
        node_list = elementsByAttributeValue(domDocument = domDocument, 
                                              attribute = 'type', 
                                              value = 'source_data')
        
        self.run_indicator_batch_menu.clear()
        for element, node in node_list:
            simulation_run = QString(element.nodeName())
            act_simulation_run = QAction(self.acceptIcon, 
                                    element.nodeName(),
                                    self.run_indicator_batch_menu)
            callback = lambda simulation_run=simulation_run: self.indicatorBatchRun(simulation_run)
            QObject.connect(act_simulation_run, SIGNAL("triggered()"), callback) 
            self.run_indicator_batch_menu.addAction(act_simulation_run)
                
    def indicatorBatchRun(self, simulation_run):
        print "indicatorBatchRun pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())
        if not self.xmlTreeObject.model.isDirty():
            self.xmlTreeObject.mainwindow.resultManagerStuff.addRunIndicatorBatchForm(
                batch_name = self.currentIndex.internalPointer().node().toElement().tagName(),
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

    def getInfoSimulationRuns(self):
        window = GetRunInfo(self,self.currentIndex)
        window.show()
        
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
                selected_type = domElement.attribute(QString("type"))
                
                self.menu = QMenu(self.xmlTreeObject.mainwindow)
                if selected_type == QString("indicator_library") and \
                       domElement.attribute(QString("append_to")) == QString("True"):
                    self.menu.addAction(self.actAddNewIndicator)
                elif selected_type == QString("source_data"):
                    self.menu.addAction(self.actGenerateResults)
                    self.menu.addAction(self.actGetInfoSimulationRuns)
                elif domElement.tagName() == QString("Indicator_batches"):
                    self.menu.addAction(self.actAddNewIndicatorBatch)
                elif selected_type == QString("indicator"):
#                    self.menu.addAction(self.actViewDocumentation)
                    self.menu.addAction(self.actEditIndicator)
                    self.menu.addAction(self.actGenerateResults)
                elif selected_type == QString("indicator_result"):
                    visualization_menu = QMenu(self.xmlTreeObject.mainwindow)
                    visualization_menu.setTitle(QString("View result as..."))
                    #visualization_menu.addAction(self.actViewResultAsTablePerYear)
                    visualization_menu.addAction(self.actViewResultAsTablePerAttribute)                    
                    visualization_menu.addAction(self.actViewResultAsMatplotlibMap)
                    #visualization_menu.addAction(self.actViewResultAsArcgisMap)
                    visualization_menu.addAction(self.actViewResultAsMatplotlibChart)
                    visualization_menu.addAction(self.actViewResultAsAdvanced)
                    self.menu.addMenu(visualization_menu)
                    
                elif selected_type == QString("indicator_batch"):
                    self._build_indicator_batch_menu()
                
                elif selected_type == QString('batch_visualization'):
                    self.menu.addAction(self.actConfigureExistingBatchIndicatorVisualization)
                    
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

    def _build_indicator_batch_menu(self):
        #needs to be called when indicator_batch right clicked on...
        self.indicator_batch_menu = QMenu(self.xmlTreeObject.mainwindow)
        self.indicator_batch_menu.setTitle(QString("Add new indicator visualization..."))

        available_visualizations = self.xml_helper.get_visualization_options()
        
        for viz in available_visualizations.keys():
            viz = QString(viz)
            act_viz = QAction(self.acceptIcon, 
                                    viz,
                                    self.indicator_batch_menu)
            callback = lambda viz=viz: self.configureNewBatchIndicatorVisualization(viz)
            QObject.connect(act_viz, SIGNAL("triggered()"), callback) 
            self.indicator_batch_menu.addAction(act_viz)
    
        self.menu.addMenu(self.indicator_batch_menu)

        
        self.run_indicator_batch_menu = QMenu(self.xmlTreeObject.mainwindow)
        self.run_indicator_batch_menu.setTitle(QString('Run indicator batch on...'))
        QObject.connect(self.run_indicator_batch_menu, SIGNAL('aboutToShow()'), self.beforeRunIndicatorBatchShown)
        
        self.menu.addMenu(self.run_indicator_batch_menu)
