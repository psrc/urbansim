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

from opus_gui.models_manager.run.run_estimation import OpusEstimation
from opus_gui.abstract_manager.controllers.xml_configuration.clonenode import CloneNodeGui

from opus_gui.general_manager.controllers.all_variables import AllVariablesSelectGui

# Dialogs for instantiating model templates
from opus_gui.models_manager.controllers.dialogs.regression_model_from_template import RegressionModelFromTemplateDialog
from opus_gui.models_manager.controllers.dialogs.simple_model_from_template import SimpleModelFromTemplateDialog
from opus_gui.models_manager.controllers.dialogs.allocation_from_template import AllocationModelFromTemplateDialog
from opus_gui.models_manager.controllers.dialogs.choice_from_template import ChoiceModelFromTemplateDialog
from opus_gui.models_manager.controllers.dialogs.agent_location_choice_from_model import AgentLocationChoiceModelFromTemplateDialog

from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlController
from opus_gui.models_manager.models.xml_model_models import XmlModel_Models

class XmlController_Models(XmlController):
    
    def __init__(self, toolboxbase, parentWidget, addTree = True, listen_to_menu = True): 
        XmlController.__init__(self, toolboxbase = toolboxbase, xml_type = 'model_manager', \
                                   parentWidget = parentWidget, addTree = addTree, \
                                   listen_to_menu = listen_to_menu)
        
        self.model = XmlModel_Models(self, self.toolboxbase.doc, \
                                     self.mainwindow, \
                                     self.toolboxbase.configFile, \
                                     self.xmlType, True)
        
        # re add the tree
        self.addTree(False)
        
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
        #TODO: Maybe 'Make copy from inherited' or something would be better 
        # than 'Add' which suggest that it doesn't exist?
        self.actMakeEditable = QAction(self.makeEditableIcon,
                                       "Add to current project",
                                       self.mainwindow)
        QObject.connect(self.actMakeEditable,
                        SIGNAL("triggered()"),
                        self.makeEditableAction)

        self.actCloneNode = QAction(self.cloneIcon,
                                    "Duplicate Node",
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
        
        # create actions for the model from template dialogs
        self.createFromModelTemplateActions = []
        for l in ('Agent Location Choice Model', \
                  'Allocation Model', \
                  'Choice Model', \
                  'Regression Model', \
                  'Simple Model'):
            self.createFromModelTemplateActions.append(self.newCreateFromTemplateAction(l))

    def newCreateFromTemplateAction(self, label):
        '''create an action with a text of label and bind it to self.createNewModelFromTemplate with
        an argument of the lower case label'''
        action = QAction(self.cloneIcon, label, self.mainwindow)
        callback = lambda x=QString(label).toLower(): self.createModelFromTemplate(x)
        QObject.connect(action, SIGNAL("triggered()"), callback)
        return action
   
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
        active_element = self.currentIndex.internalPointer().node().toElement()
        model_name = str(active_element.tagName())
        self.toolboxbase.updateOpusXMLTree()
        newEstimation = OpusEstimation(self,
                                       self.toolboxbase.xml_file,
                                       model_name = model_name)
        self.mainwindow.modelsManagerBase.addEstimationElement(estimation = newEstimation)

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
        window = CloneNodeGui(self, clone, parentIndex, model)
        window.show()

    def createModelFromTemplate(self, model_name):
        '''select element to clone and present the correct dialog for it'''
        # the method selects wich element node to clone by mapping the
        #  model_name to a node element in the tree
        template_expected_name = QString(model_name).replace(' ', '_').append('_template')
        
        # look for the template node under the model_system child node
        model_system_node = self.model.xmlRoot.firstChildElement('model_system')
        template_node = model_system_node.firstChildElement(template_expected_name)
        
        if template_node.isNull():
            raise ValueError('Did not find a template for %s. Expected to find template named %s' \
                        %(model_name, template_expected_name))

        # clone the dom node and fetch the information of where we are in the tree
        clone = template_node.cloneNode()
        model = self.currentIndex.model()
        parentIndex = self.currentIndex
        
        # select dialog based on model name
        model_name = QString(model_name).toLower()
        dialog = None
        
        # all dialog have the same args, so we just specify them once
        dialog_args = (self.mainwindow, clone, parentIndex, model)
        
        if model_name == 'simple model':
            dialog = SimpleModelFromTemplateDialog(*dialog_args)
        elif model_name == 'choice model':
            dialog = ChoiceModelFromTemplateDialog(*dialog_args)
        elif model_name == 'regression model':
            dialog = RegressionModelFromTemplateDialog(*dialog_args)
        elif model_name == 'allocation model':
            dialog = AllocationModelFromTemplateDialog(*dialog_args)                                            
        elif model_name == 'agent location choice model':
            dialog = AgentLocationChoiceModelFromTemplateDialog(*dialog_args)
        
        if not dialog:
            raise NotImplementedError('dialog for template %s not yet implemented' %model_name)
        
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
            item = self.currentIndex.internalPointer()
            domNode = item.node()
            if domNode.isNull():
                return
            
            # Handle ElementNodes
            if domNode.isElement():
                domElement = domNode.toElement()
                if domElement.isNull():
                    return
                
                element_type = domElement.attribute('type')
                
                # create menu to populate
                menu = QMenu(self.mainwindow)

                if element_type == 'model_system':
                    submenu = QMenu(menu) # to populate with templates
                    submenu.setTitle('Create model from template')
                    for act in self.createFromModelTemplateActions:
                        submenu.addAction(act)
                    menu.addMenu(submenu)
                    
                if element_type in ['model', 'submodel', 'model_system']:
                    menu.addAction(self.actRunEstimation)
                
                if menu:
                    menu.addSeparator()
                    # Last minute chance to add items that all menues should have
                    if domElement.hasAttribute(QString("inherited")):
                        # Tack on a make editable if the node is inherited
                        menu.addSeparator()
                        menu.addAction(self.actMakeEditable)
                    else:
                        if domElement.hasAttribute(QString("copyable")) and \
                               domElement.attribute(QString("copyable")) == QString("True"):
                            menu.addSeparator()
                            menu.addAction(self.actCloneNode)
                        elif domElement.hasAttribute(QString("type")) and \
                               domElement.attribute(QString("type")) == QString("variable_list"):
                            menu.addSeparator()
                            menu.addAction(self.actSelectVariables)

                        if domElement and (not domElement.isNull()) and \
                               domElement.hasAttribute(QString("type")) and \
                               ((domElement.attribute(QString("type")) == QString("dictionary")) or \
                                (domElement.attribute(QString("type")) == QString("selectable_list")) or \
                                (domElement.attribute(QString("type")) == QString("model_estimation")) or \
                                (domElement.attribute(QString("type")) == QString("list"))):
                            menu.addSeparator()
                            menu.addAction(self.actRemoveNode)
                # Check if the menu has any elements before exec is called
                if not menu.isEmpty():
                    menu.exec_(QCursor.pos())
        return

