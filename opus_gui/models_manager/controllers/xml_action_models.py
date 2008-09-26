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

from opus_gui.models_manager.run.opusrunestimation import OpusEstimation
from opus_gui.config.managerbase.clonenode import CloneNodeGui

from opus_gui.general_manager.controllers.all_variables import AllVariablesSelectGui
from opus_gui.models_manager.controllers.create_model_from_template import CreateModelFromTemplateDialog

from opus_gui.config.xmltree.opusxmlaction import OpusXMLAction

class xmlActionController_Models(OpusXMLAction):
    
    def __init__(self, xmlTreeObject):
        OpusXMLAction.__init__(self, xmlTreeObject)
        self.xmlTreeObject = xmlTreeObject

        self.currentColumn = None
        self.currentIndex = None

        self.removeIcon = QIcon(":/Images/Images/delete.png")
        self.applicationIcon = QIcon(":/Images/Images/application_side_tree.png")
        self.calendarIcon = QIcon(":/Images/Images/calendar_view_day.png")
        self.cloneIcon = QIcon(":/Images/Images/application_double.png")
        self.makeEditableIcon = QIcon(":/Images/Images/application_edit.png")

        self.actRunEstimation = QAction(self.applicationIcon,
                                        "Run Estimation",
                                        self.xmlTreeObject.mainwindow)
        QObject.connect(self.actRunEstimation,
                        SIGNAL("triggered()"),
                        self.runEstimationAction)

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

        self.actCreateModelFromTemplate = QAction(self.cloneIcon,
                                    "Create model from template",
                                    self.xmlTreeObject.mainwindow)
        QObject.connect(self.actCreateModelFromTemplate,
                        SIGNAL("triggered()"),
                        self.createModelFromTemplate)
        
        self.actSelectVariables = QAction(self.applicationIcon,
                                          "Select Variables",
                                          self.xmlTreeObject.mainwindow)
        QObject.connect(self.actSelectVariables,
                        SIGNAL("triggered()"),
                        self.selectVariables)

    def selectVariablesCallback(self, returnList, returnString):
        print returnString
        
    def selectVariables(self):
        thisNode = self.currentIndex.internalPointer().node()
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        self.all_variables = AllVariablesSelectGui(self.mainwindow,flags,callback=self.selectVariablesCallback,
                                                   nodeToUpdate=thisNode)
        self.all_variables.setModal(True)
        self.all_variables.show()

    def checkIsDirty(self):
        if (self.xmlTreeObject.toolboxbase.resultsManagerTree and self.xmlTreeObject.toolboxbase.resultsManagerTree.model.isDirty()) or \
               (self.xmlTreeObject.toolboxbase.modelManagerTree and self.xmlTreeObject.toolboxbase.modelManagerTree.model.isDirty()) or \
               (self.xmlTreeObject.toolboxbase.runManagerTree and self.xmlTreeObject.toolboxbase.runManagerTree.model.isDirty()) or \
               (self.xmlTreeObject.toolboxbase.dataManagerTree and self.xmlTreeObject.toolboxbase.dataManagerTree.model.isDirty()) or \
               (self.xmlTreeObject.toolboxbase.dataManagerDBSTree and self.xmlTreeObject.toolboxbase.dataManagerDBSTree.model.isDirty()) or \
               (self.xmlTreeObject.toolboxbase.generalManagerTree and self.xmlTreeObject.toolboxbase.generalManagerTree.model.isDirty()):
            return True
        else:
            return False

    def runEstimationAction(self):
        thisNode = self.currentIndex.internalPointer().node()
        model_name = str(thisNode.toElement().tagName())
        self.xmlTreeObject.toolboxbase.updateOpusXMLTree()
        newEstimation = OpusEstimation(self.xmlTreeObject,
                                       self.xmlTreeObject.toolboxbase.xml_file,
                                       model_name = model_name)
        self.xmlTreeObject.mainwindow.modelsManagerBase.addEstimationElement(model = newEstimation)

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
        window.setModal(True)
        window.show()

    def createModelFromTemplate(self):
        #print "cloneNode Pressed"
        clone = self.currentIndex.internalPointer().domNode.cloneNode()
        parentIndex = self.currentIndex.model().parent(self.currentIndex)
        model = self.currentIndex.model()
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        window = CreateModelFromTemplateDialog(self,flags,clone,parentIndex,model)
        window.setModal(True)
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
#                if domElement.tagName() == QString("models_to_estimate"):
#                    self.menu.addAction(self.actRunEstimation)
                if domElement.attribute(QString("type")) == QString("model_estimation"):
                    self.menu.addAction(self.actRunEstimation)
                
                if domElement.tagName() == QString('regression_model_template'):
                    self.menu.addAction(self.actCreateModelFromTemplate)

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
                        elif domElement.hasAttribute(QString("type")) and \
                               domElement.attribute(QString("type")) == QString("variable_list"):
                            self.menu.addSeparator()
                            self.menu.addAction(self.actSelectVariables)

                        if domElement and (not domElement.isNull()) and \
                               domElement.hasAttribute(QString("type")) and \
                               ((domElement.attribute(QString("type")) == QString("dictionary")) or \
                                (domElement.attribute(QString("type")) == QString("selectable_list")) or \
                                (domElement.attribute(QString("type")) == QString("model_estimation")) or \
                                (domElement.attribute(QString("type")) == QString("list"))):
                            self.menu.addSeparator()
                            self.menu.addAction(self.actRemoveNode)
                # Check if the menu has any elements before exec is called
                if not self.menu.isEmpty():
                    self.menu.exec_(QCursor.pos())
        return

