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
from opus_gui.abstract_manager.controllers.xml.clonenode import CloneNodeGui

from opus_gui.general_manager.controllers.all_variables import AllVariablesSelectGui

from opus_gui.models_manager.controllers.dialogs.regression_model_from_template import RegressionModelFromTemplateDialog
from opus_gui.models_manager.controllers.dialogs.simple_model_from_template import SimpleModelFromTemplateDialog

from opus_gui.abstract_manager.controllers.xml.opus_xml_controller import OpusXMLController

class xmlActionController_Models(OpusXMLController):
    
    def __init__(self, toolboxbase, parentWidget, addTree = True, listen_to_menu = True): 
        OpusXMLController.__init__(self, toolboxbase = toolboxbase, xml_type = 'model_manager', \
                                   parentWidget = parentWidget, addTree = addTree, \
                                   listen_to_menu = listen_to_menu) 

        self.currentColumn = None
        self.currentIndex = None

        self.removeIcon = QIcon(":/Images/Images/delete.png")
        self.applicationIcon = QIcon(":/Images/Images/application_side_tree.png")
        self.calendarIcon = QIcon(":/Images/Images/calendar_view_day.png")
        self.cloneIcon = QIcon(":/Images/Images/application_double.png")
        self.makeEditableIcon = QIcon(":/Images/Images/application_edit.png")

        self.actRunEstimation = QAction(self.applicationIcon,
                                        "Run Estimation",
                                        self.mainwindow)
        QObject.connect(self.actRunEstimation,
                        SIGNAL("triggered()"),
                        self.runEstimationAction)

        self.actRemoveNode = QAction(self.removeIcon,
                                     "Remove node from current project",
                                     self.mainwindow)
        QObject.connect(self.actRemoveNode,
                        SIGNAL("triggered()"),
                        self.removeNode)

        self.actMakeEditable = QAction(self.makeEditableIcon,
                                       "Add to current project",
                                       self.mainwindow)
        QObject.connect(self.actMakeEditable,
                        SIGNAL("triggered()"),
                        self.makeEditableAction)

        self.actCloneNode = QAction(self.cloneIcon,
                                    "Copy Node",
                                    self.mainwindow)
        QObject.connect(self.actCloneNode,
                        SIGNAL("triggered()"),
                        self.cloneNode)

        self.actCreateModelFromTemplate = QAction(self.cloneIcon,
                                    "Create model from template",
                                    self.mainwindow)
        QObject.connect(self.actCreateModelFromTemplate,
                        SIGNAL("triggered()"),
                        self.createModelFromTemplate)
        
        self.actSelectVariables = QAction(self.applicationIcon,
                                          "Select Variables",
                                          self.mainwindow)
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
        if (self.toolboxbase.resultsManagerTree and self.toolboxbase.resultsManagerTree.model.isDirty()) or \
               (self.toolboxbase.modelManagerTree and self.toolboxbase.modelManagerTree.model.isDirty()) or \
               (self.toolboxbase.runManagerTree and self.toolboxbase.runManagerTree.model.isDirty()) or \
               (self.toolboxbase.dataManagerTree and self.toolboxbase.dataManagerTree.model.isDirty()) or \
               (self.toolboxbase.dataManagerDBSTree and self.toolboxbase.dataManagerDBSTree.model.isDirty()) or \
               (self.toolboxbase.generalManagerTree and self.toolboxbase.generalManagerTree.model.isDirty()):
            return True
        else:
            return False

    def runEstimationAction(self):
        thisNode = self.currentIndex.internalPointer().node()
        model_name = str(thisNode.toElement().tagName())
        self.toolboxbase.updateOpusXMLTree()
        newEstimation = OpusEstimation(self,
                                       self.toolboxbase.xml_file,
                                       model_name = model_name)
        self.mainwindow.modelsManagerBase.addEstimationElement(model = newEstimation)

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
        #TODO: move view specific things into dialog for cleaner separation of view/ctrl
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        window = CloneNodeGui(self,flags,clone,parentIndex,model)
        window.setModal(True)
        window.show()

    def createModelFromTemplate(self):
        # clone the dom node and fetch the information of where we are in the tree
        clone = self.currentIndex.internalPointer().domNode.cloneNode()
        model = self.currentIndex.model()
        parentIndex = model.parent(self.currentIndex)
        
        # select dialog based on template name
        tag_name = clone.toElement().tagName()
        dialog = None
        # all dialog have the same args, so we just specify them once
        dialog_args = (self.mainwindow, clone, parentIndex, model)
        
        if tag_name == 'simple_model_template':
            dialog = SimpleModelFromTemplateDialog(*dialog_args)
        elif tag_name == 'choice_model_template':
            pass
        elif tag_name == 'regression_model_template':
            dialog = RegressionModelFromTemplateDialog(*dialog_args)
        elif tag_name == 'allocation_model_template':
            pass
        elif tag_name == 'agent_location_choice_model_template':
            pass
        
        if not dialog:
            raise NotImplementedError('dialog for template %s not yet implemented' %tag_name)
        
        # show the dialog
        dialog.setModal(True)
        dialog.show()
        
    def makeEditableAction(self):
        thisNode = self.currentIndex.internalPointer().node()
        self.currentIndex.model().makeEditable(thisNode)
        # Finally we refresh the tree to indicate that there has been a change
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def processCustomMenu(self, position):
        if self.view.indexAt(position).isValid() and \
               self.view.indexAt(position).column() == 0:
            self.currentColumn = self.view.indexAt(position).column()
            self.currentIndex = self.view.indexAt(position)
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

                self.menu = QMenu(self.mainwindow)
#                if domElement.tagName() == QString("models_to_estimate"):
#                    self.menu.addAction(self.actRunEstimation)
                if domElement.attribute(QString("type")) == QString("model_estimation"):
                    self.menu.addAction(self.actRunEstimation)
                
                #TODO: Some sort of metadata check for templates rather than naming schemes
                if domElement.tagName().endsWith('_model_template'):
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

