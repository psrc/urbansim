# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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
from PyQt4.QtCore import QString, Qt, QObject, SIGNAL
from PyQt4.QtGui import QIcon, QAction, QMenu, QCursor

from opus_gui.config.managerbase.clonenode import CloneNodeGui
from opus_gui.results_manager.xml_helper_methods import elementsByAttributeValue
from opus_gui.results_manager.xml_helper_methods import ResultsManagerXMLHelper,get_child_values
from opus_gui.results_manager.controllers.get_run_info import GetRunInfo

class xmlActionController_Results(object):
    def __init__(self, opusXMLAction):
        self.opusXMLAction = opusXMLAction
        self.mainwindow = opusXMLAction.mainwindow
        self.xmlTreeObject = opusXMLAction.xmlTreeObject
        self.toolboxBase = self.xmlTreeObject.mainwindow.toolboxBase
        self.xml_helper = ResultsManagerXMLHelper(toolboxBase = self.toolboxBase)

        self.currentColumn = None
        self.currentIndex = None

        self.acceptIcon = QIcon(":/Images/Images/accept.png")
        self.removeIcon = QIcon(":/Images/Images/delete.png")
        self.calendarIcon = QIcon(":/Images/Images/calendar_view_day.png")
        self.applicationIcon = QIcon(":/Images/Images/application_side_tree.png")
        self.cloneIcon = QIcon(":/Images/Images/application_double.png")
        self.makeEditableIcon = QIcon(":/Images/Images/application_edit.png")

        
        self.actAddNewIndicatorBatch = QAction(self.acceptIcon, 
                                          "Add new indicator batch...",
                                          self.xmlTreeObject.mainwindow)
        QObject.connect(self.actAddNewIndicatorBatch, SIGNAL("triggered()"), self.addNewIndicatorBatch)          

        self.actAddVisualizationToBatch = QAction(self.acceptIcon,
                                               'Add new indicator visualization...',
                                               self.xmlTreeObject.mainwindow
                                               )
        QObject.connect(self.actAddVisualizationToBatch, SIGNAL("triggered()"), self.configureNewBatchIndicatorVisualization)    

        
        #delete run from disk
        self.actDeleteRun = QAction(self.removeIcon, 
                                          "Remove run and delete from harddrive...",
                                          self.xmlTreeObject.mainwindow)
        QObject.connect(self.actDeleteRun, SIGNAL("triggered()"), self.deleteRun)          

        self.actImportRun = QAction(self.acceptIcon, 
                                          "Import run from disk",
                                          self.xmlTreeObject.mainwindow)
        QObject.connect(self.actImportRun, SIGNAL("triggered()"), self.importRun) 
    

        self.actConfigureExistingBatchIndicatorVisualization = QAction(self.acceptIcon,
                                                                       "Configure visualization",
                                                                       self.xmlTreeObject.mainwindow)
        QObject.connect(self.actConfigureExistingBatchIndicatorVisualization, SIGNAL("triggered()"), self.configureExistingBatchIndicatorVisualization)


        self.actGetInfoSimulationRuns = QAction(self.acceptIcon, 
                                          "Show details",
                                          self.xmlTreeObject.mainwindow)
        QObject.connect(self.actGetInfoSimulationRuns, SIGNAL("triggered()"), self.getInfoSimulationRuns) 


#        self.actViewDocumentation = QAction(self.applicationIcon, "View documentation", self.xmlTreeObject.mainwindow)
#        QObject.connect(self.actViewDocumentation, SIGNAL("triggered()"), self.viewDocumentation)

        self.actRemoveNode = QAction(self.removeIcon,
                                     "Remove node from current project",
                                     self.xmlTreeObject.mainwindow)
        QObject.connect(self.actRemoveNode,
                        SIGNAL("triggered()"),
                        self.removeNode)

        self.actMakeEditable = QAction(self.makeEditableIcon,
                                       "Add to current project",
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


    def addNewIndicatorBatch(self):
              
        self.xml_helper.addNewIndicatorBatch(batch_name = 'untitled_indicator_batch')
        
#    def beforeAddIndicatorToBatchShown(self):
#        #batch_name = self.currentIndex.internalPointer().node().toElement().tagName()
#        #existing_indicators = self.xml_helper.get_indicators_in_indicator_batch(batch_name)
#        
#        available_indicators = self.xml_helper.get_available_indicator_names()
#        
#        self.indicator_batch_menu.clear()
#        for indicator_info in available_indicators:
#            indicator_name = indicator_info['name']
##            if indicator_name in existing_indicators:
##                continue
#            indicator = QString(indicator_name)
#            act_indicator = QAction(self.acceptIcon, 
#                                    indicator_name,
#                                    self.indicator_batch_menu)
#            callback = lambda indicator=indicator: self.addIndicatorToBatch(indicator)
#            QObject.connect(act_indicator, SIGNAL("triggered()"), callback) 
#            self.indicator_batch_menu.addAction(act_indicator)
#            
#    def addIndicatorToBatch(self, indicator):
#        batch_name = self.currentIndex.internalPointer().node().toElement().tagName()
#        self.xml_helper.addIndicatorToBatch(batch_name = batch_name, 
#                                            indicator_name = indicator)
        
    def configureNewBatchIndicatorVisualization(self, viz = None):
        batch_name = self.currentIndex.internalPointer().node().toElement().tagName()
        self.xmlTreeObject.mainwindow.resultManagerStuff.configureNewIndicatorBatchVisualization(
            #visualization_type = viz,
            batch_name = batch_name)

    def configureExistingBatchIndicatorVisualization(self):

        self.xmlTreeObject.mainwindow.resultManagerStuff.configureExistingIndicatorBatchVisualization(
            selected_index = self.currentIndex)   
        
    def deleteRun(self):

        node = self.currentIndex.internalPointer().node()
        vals = get_child_values(parent = node, child_names = ['cache_directory', 'run_id'])
        cache_directory = str(vals['cache_directory'])
        if cache_directory.find('base_year') == -1:
            run_id = vals.get('run_id', None)
            if run_id is not None:
                run_id = int(run_id)
                self.xmlTreeObject.mainwindow.resultManagerStuff.deleteRun(
                    run_id = int(run_id), cache_directory = cache_directory)    
            
            self.removeNode()   
            
    def importRun(self):
        self.xmlTreeObject.mainwindow.resultManagerStuff.importRun()  
          
    def beforeRunIndicatorBatchShown(self):
        domDocument = self.xmlTreeObject.mainwindow.toolboxBase.doc
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
        self.xmlTreeObject.mainwindow.resultManagerStuff.addRunIndicatorBatchForm(
            batch_name = self.currentIndex.internalPointer().node().toElement().tagName(),
            simulation_run = simulation_run)
                      

    def getInfoSimulationRuns(self):
        window = GetRunInfo(self,self.currentIndex)
        window.show()

    def viewDocumentation(self):
        pass


    def removeNode(self):
        self.currentIndex.model().removeRow(self.currentIndex.internalPointer().row(),
                                            self.currentIndex.model().parent(self.currentIndex))
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def cloneNode(self):
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
#                if selected_type == QString("indicator_library") and \
#                       domElement.attribute(QString("append_to")) == QString("True"):
#                    self.menu.addAction(self.actAddNewIndicator)
                if selected_type == QString("source_data"):
#                    self.menu.addAction(self.actGenerateResults)
                    self.menu.addAction(self.actGetInfoSimulationRuns)
                    self.menu.addAction(self.actDeleteRun)
                elif domElement.tagName() == QString("Indicator_batches"):
                    self.menu.addAction(self.actAddNewIndicatorBatch)
                    
                elif domElement.tagName() == QString("Simulation_runs"):
                    self.menu.addAction(self.actImportRun)
                    
                elif selected_type == QString("indicator_batch"):
#                    self._build_indicator_batch_menu()
                    self.menu.addAction(self.actAddVisualizationToBatch)
                    self.run_indicator_batch_menu = QMenu(self.xmlTreeObject.mainwindow)
                    self.run_indicator_batch_menu.setTitle(QString('Run indicator batch on...'))
                    QObject.connect(self.run_indicator_batch_menu, SIGNAL('aboutToShow()'), self.beforeRunIndicatorBatchShown)
                    self.menu.addMenu(self.run_indicator_batch_menu)
                                    
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

                        types_with_remove = ["dictionary", "selectable_list", "list", "source_data", "batch_visualization", "indicator_batch", "indicator", "indicator_result"]

                        if domElement and (not domElement.isNull()) and \
                               domElement.hasAttribute(QString("type")) and \
                               (str(domElement.attribute(QString("type"))) in types_with_remove):

                            self.menu.addSeparator()
                            self.menu.addAction(self.actRemoveNode)
                # Check if the menu has any elements before exec is called
                if not self.menu.isEmpty():
                    self.menu.exec_(QCursor.pos())
        return

#    def _build_indicator_batch_menu(self):
#        #needs to be called when indicator_batch right clicked on...
##        self.indicator_batch_menu = QMenu(self.xmlTreeObject.mainwindow)
##        self.indicator_batch_menu.setTitle(QString("Add new indicator visualization..."))
#        
#
#
#        available_visualizations = self.xml_helper.get_visualization_options()
#        
#        for viz in available_visualizations.keys():
#            viz = QString(viz)
#            act_viz = QAction(self.acceptIcon, 
#                                    viz,
#                                    self.indicator_batch_menu)
#            callback = lambda viz=viz: self.configureNewBatchIndicatorVisualization(viz)
#            QObject.connect(act_viz, SIGNAL("triggered()"), callback) 
#            self.indicator_batch_menu.addAction(act_viz)
#    
#        self.menu.addMenu(self.indicator_batch_menu)
#
#        
#        self.run_indicator_batch_menu = QMenu(self.xmlTreeObject.mainwindow)
#        self.run_indicator_batch_menu.setTitle(QString('Run indicator batch on...'))
#        QObject.connect(self.run_indicator_batch_menu, SIGNAL('aboutToShow()'), self.beforeRunIndicatorBatchShown)
#        
#        self.menu.addMenu(self.run_indicator_batch_menu)
