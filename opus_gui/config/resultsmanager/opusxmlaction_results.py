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

class OpusXMLAction_Results(object):
    def __init__(self, parent):
        self.parent = parent
        self.mainwindow = parent.mainwindow
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
        self.actAddNewIndicatorGroup = QAction(self.acceptIcon, 
                                          "Add new indicator group...",
                                          self.xmlTreeObject.parent)
        QObject.connect(self.actAddNewIndicatorGroup, SIGNAL("triggered()"), self.addNewIndicatorGroup)          

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
        #self.actViewResultAsArcgisMap = QAction(self.acceptIcon, 
        #                                  "Map (ArcGis)",
        #                                  self.xmlTreeObject.parent)
        #QObject.connect(self.actViewResultAsArcgisMap, SIGNAL("triggered()"), self.viewResultsArcGisMap)                

        self.actViewResultAsMatplotlibChart = QAction(self.acceptIcon, 
                                          "Chart (Matplotlib)",
                                          self.xmlTreeObject.parent)
        QObject.connect(self.actViewResultAsMatplotlibChart, SIGNAL("triggered()"), self.viewResultsMatplotlibChart) 
#        self.actViewResultAsTablePerYear = QAction(self.acceptIcon, 
#                                          "Table (one per year over selected indicators)",
#                                          self.xmlTreeObject.parent)
        #QObject.connect(self.actViewResultAsTablePerYear, SIGNAL("triggered()"), self.viewResultsTablePerYear) 
        self.actViewResultAsTablePerAttribute = QAction(self.acceptIcon, 
                                          "Table",
                                          self.xmlTreeObject.parent)
        QObject.connect(self.actViewResultAsTablePerAttribute, SIGNAL("triggered()"), self.viewResultsTablePerAttribute) 

        #launch advanced view results window...
        self.actViewResultAsAdvanced = QAction(self.acceptIcon, 
                                          "Advanced visualization...",
                                          self.xmlTreeObject.parent)
        QObject.connect(self.actViewResultAsAdvanced, SIGNAL("triggered()"), self.viewResultsAdvanced) 


        self.actViewDocumentation = QAction(self.applicationIcon, "View documentation", self.xmlTreeObject.parent)
        QObject.connect(self.actViewDocumentation, SIGNAL("triggered()"), self.viewDocumentation)

        self.actRemoveNode = QAction(self.removeIcon,
                                     "Remove Node",
                                     self.xmlTreeObject.parent)
        QObject.connect(self.actRemoveNode,
                        SIGNAL("triggered()"),
                        self.removeNode)

        self.actMakeEditable = QAction(self.applicationIcon,
                                       "Make Editable",
                                       self.xmlTreeObject.parent)
        QObject.connect(self.actMakeEditable,
                        SIGNAL("triggered()"),
                        self.makeEditableAction)

        self.actCloneNode = QAction(self.calendarIcon,
                                    "Copy Node",
                                    self.xmlTreeObject.parent)
        QObject.connect(self.actCloneNode,
                        SIGNAL("triggered()"),
                        self.cloneNode)


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

        self.currentIndex.model().markAsDirty()
        model.emit(SIGNAL("layoutChanged()"))


    def addNewIndicatorGroup(self):
        print "addNewIndicatorGroup pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())
              
        model = self.currentIndex.model()
        document = model.domDocument
        name = 'untitled indicator group'

        newNode = model.create_node(document = document, 
                                    name = name, 
                                    type = 'indicator_group', 
                                    value = '')

        model.insertRow(0,
                self.currentIndex,
                newNode)

        self.currentIndex.model().markAsDirty()
        model.emit(SIGNAL("layoutChanged()"))

            
    def generateResults(self):
        print "generateResults pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())
        if not self.xmlTreeObject.model.dirty:
            self.xmlTreeObject.parent.resultManagerStuff.addGenerateIndicatorForm(
                selected_item = self.currentIndex.internalPointer().node().toElement().tagName())
        else:
            # Prompt the user to save...
            QMessageBox.warning(self.xmlTreeObject.parent,
                                "Warning",
                                "Please save changes to project before generating results")

    def viewResultsMatplotlibMap(self):
        clicked_node = self.currentIndex.internalPointer().node().toElement()          
        self.xmlTreeObject.parent.resultManagerStuff.addIndicatorFormFromNode(
                                                          indicator_type = 'matplotlib_map',
                                                          clicked_node = clicked_node)

    def viewResultsArcGisMap(self):
        clicked_node = self.currentIndex.internalPointer().node().toElement()          
        self.xmlTreeObject.parent.resultManagerStuff.addIndicatorFormFromNode(
                                                          indicator_type = 'arcgis_map',
                                                          clicked_node = clicked_node)           
    def viewResultsMatplotlibChart(self):
        clicked_node = self.currentIndex.internalPointer().node().toElement()           
        self.xmlTreeObject.parent.resultManagerStuff.addIndicatorFormFromNode(
                                                          indicator_type = 'matplotlib_chart',
                                                          clicked_node = clicked_node)

    def viewResultsTablePerAttribute(self):
        clicked_node = self.currentIndex.internalPointer().node().toElement()           
        self.xmlTreeObject.parent.resultManagerStuff.addIndicatorFormFromNode(
                                                          indicator_type = 'table_per_attribute',
                                                          clicked_node = clicked_node)

    def viewResultsTablePerYear(self):
        clicked_node = self.currentIndex.internalPointer().node().toElement()           
        self.xmlTreeObject.parent.resultManagerStuff.addIndicatorFormFromNode(
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

    def removeNode(self):
        #print "Remove Node Pressed"
        self.currentIndex.model().removeRow(self.currentIndex.internalPointer().row(),
                                            self.currentIndex.model().parent(self.currentIndex))
        self.currentIndex.model().markAsDirty()
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def cloneNode(self):
        #print "cloneNode Pressed"
        clone = self.currentIndex.internalPointer().domNode.cloneNode()
        parent = self.currentIndex.model().parent(self.currentIndex)
        model = self.currentIndex.model()
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        window = CloneNodeGui(self,flags,clone,parent,model)
        window.show()

    def makeEditableAction(self):
        thisNode = self.currentIndex.internalPointer().node()
        # Strip the inherited attribute down the tree
        self.currentIndex.model().stripAttributeDown('inherited',thisNode)
        # Now up the tree, only hitting parent nodes and not sibblings
        self.currentIndex.model().stripAttributeUp('inherited',thisNode)
        self.currentIndex.model().markAsDirty()
        # Finally we refresh the tree to indicate that there has been a change
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    #################### Old methods not currently used ###################
    def cloneNodeAction(self):
        print "Clone Node pressed..."
        clone = self.currentIndex.internalPointer().domNode.cloneNode()
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        window = CloneInheritedGui(self,flags,self.xmlTreeObject.model,clone)
        window.show()

    ##################################################3####################

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
                
                self.menu = QMenu(self.xmlTreeObject.parent)
                if domElement.attribute(QString("type")) == QString("indicator_library") and \
                       domElement.attribute(QString("append_to")) == QString("True"):
                    self.menu.addAction(self.actAddNewIndicator)
                elif domElement.attribute(QString("type")) == QString("source_data"):
                    self.menu.addAction(self.actGenerateResults)
                elif domElement.tagName() == QString("Indicator_groups"):
                    self.menu.addAction(self.actAddNewIndicatorGroup)
                elif domElement.attribute(QString("type")) == QString("indicator"):
                    self.menu.addAction(self.actViewDocumentation)
                    self.menu.addAction(self.actGenerateResults)
                elif domElement.attribute(QString("type")) == QString("indicator_result"):
                    visualization_menu = QMenu(self.xmlTreeObject.parent)
                    visualization_menu.setTitle(QString("View result as..."))
                    #visualization_menu.addAction(self.actViewResultAsTablePerYear)
                    visualization_menu.addAction(self.actViewResultAsTablePerAttribute)                    
                    visualization_menu.addAction(self.actViewResultAsMatplotlibMap)
                    #visualization_menu.addAction(self.actViewResultAsArcgisMap)
                    visualization_menu.addAction(self.actViewResultAsMatplotlibChart)
                    visualization_menu.addAction(self.actViewResultAsAdvanced)
                    self.menu.addMenu(visualization_menu)

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


