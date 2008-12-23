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
from PyQt4.QtCore import QString, SIGNAL
from PyQt4.QtGui import QIcon, QMenu, QCursor

from opus_gui.models_manager.run.run_estimation import OpusEstimation
from opus_gui.abstract_manager.controllers.xml_configuration.clonenode import \
    CloneNodeGui, RenameNodeGui

from opus_gui.general_manager.controllers.all_variables import AllVariablesSelectGui

# Dialogs for instantiating model templates
from opus_gui.models_manager.controllers.dialogs.regression_model_from_template import RegressionModelFromTemplateDialog
from opus_gui.models_manager.controllers.dialogs.simple_model_from_template import SimpleModelFromTemplateDialog
from opus_gui.models_manager.controllers.dialogs.allocation_from_template import AllocationModelFromTemplateDialog
from opus_gui.models_manager.controllers.dialogs.choice_from_template import ChoiceModelFromTemplateDialog
from opus_gui.models_manager.controllers.dialogs.agent_location_choice_from_model import AgentLocationChoiceModelFromTemplateDialog

from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlController
from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlView
from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlItemDelegate

from opus_gui.models_manager.models.xml_model_models import XmlModel_Models

class XmlController_Models(XmlController):

    def __init__(self, toolboxbase, parentWidget):
        XmlController.__init__(self, toolboxbase = toolboxbase, xml_type = 'model_manager', \
                                   parentWidget = parentWidget)

        self.removeIcon = QIcon(":/Images/Images/delete.png")
        self.applicationIcon = QIcon(":/Images/Images/application_side_tree.png")
        self.calendarIcon = QIcon(":/Images/Images/calendar_view_day.png")
        self.cloneIcon = QIcon(":/Images/Images/application_double.png")
        self.makeEditableIcon = QIcon(":/Images/Images/application_edit.png")

        self.actRemoveNode = self.createAction(self.removeIcon, \
            "Remove node from current project", self.removeNode)
        self.actMakeEditable = self.createAction(self.makeEditableIcon, \
            "Add to current project", self.makeEditableAction)
        self.actCloneNode = self.createAction(self.cloneIcon, \
            "Duplicate Node", self.cloneNode)

        cb = lambda x=None:RenameNodeGui(self, self.currentElement()).show()
        self.actRenameNode = self.createAction(self.makeEditableIcon, \
            "Rename Node", cb)
        self.actCreateModelFromTemplate = self.createAction(self.cloneIcon, \
            "Create model from template", self.createModelFromTemplate)
        self.actSelectVariables = self.createAction(self.applicationIcon, \
            "Select Variables", self.selectVariables)
        # create an estimation run for the selected model
        self.actRunEstimation = self.createAction(self.applicationIcon, \
            "Run Estimation", self.runEstimation)
        # inform the users that they need to right click the sub model groups
        self.actHowToRunEstGroups = self.createAction(self.applicationIcon,
            "Right click the individual submodel groups to estimate them",
            lambda: ())
        # run a submodel group
        self.actRunEstimationGroup = self.createAction(self.applicationIcon,
            "Run Estimation Group", self.runEstimationGroup)


        # create actions for the model from template dialogs
        self.create_from_template_actions = []
        for l in ('Agent Location Choice Model',
                  'Allocation Model',
                  'Choice Model',
                  'Regression Model',
                  'Simple Model'):
            callback = \
                lambda x=l.lower():self.createModelFromTemplate(x)
            self.create_from_template_actions.\
                append(self.createAction(self.cloneIcon, l, callback))


    def setupModelViewDelegate(self):
        '''switch out the model'''
        self.model = XmlModel_Models(self, self.toolboxbase.doc, self.mainwindow,
              self.toolboxbase.configFile, self.xmlType, True)
        self.view = XmlView(self.mainwindow)
        self.delegate = XmlItemDelegate(self.view)


    def currentItem(self):
        return self.view.currentIndex()

    def currentElement(self):
        return self.currentItem().internalPointer().node().toElement()

    def selectVariablesCallback(self, returnList, returnString):
        print returnString

    def selectVariables(self):
        AllVariablesSelectGui(self.mainwindow,
                              callback=self.selectVariablesCallback,
                              nodeToUpdate=self.currentElement()).show()

    def runEstimation(self):
        '''
        Create an estimation run dialog for for running all the submodels.
        '''
        current_element = self.currentElement()
        model_name = str(current_element.tagName())
        self.toolboxbase.updateOpusXMLTree()
        newEstimation = OpusEstimation(self,
                                       self.toolboxbase.xml_file,
                                       model_name = model_name)
        self.mainwindow.modelsManagerBase.addEstimationElement(newEstimation)


    def runEstimationGroup(self):
        '''
            Create an estimation run dialog for this model for running a
            all submodels within a submodel group.
        '''
        # figure out the model name.
        # Expected place is <model name>/specfication/<current element>
        current_element = self.currentElement()
        model_element = current_element.parentNode().parentNode().toElement()

        model_name = str(model_element.tagName())
        group_name = str(current_element.tagName())

        self.toolboxbase.updateOpusXMLTree()
        newEstimation = OpusEstimation(self,
                                       self.toolboxbase.xml_file,
                                       model_name = model_name,
                                       model_group = group_name)
        self.mainwindow.modelsManagerBase.addEstimationElement(newEstimation)

    def removeNode(self):
        self.model.removeRow(self.currentItem().internalPointer().row(),
                                            self.model.parent(self.currentItem()))
        self.model.emit(SIGNAL("layoutChanged()"))
        # re-validate the models to run lists
        self.toolboxbase.runManagerTree.validate_models_to_run_list()


    def cloneNode(self):
        #print "cloneNode Pressed"
        clone = self.currentElement().cloneNode()
        parentIndex = self.model.parent(self.currentItem())
        window = CloneNodeGui(self, clone, parentIndex, self.model)
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
            raise ValueError('Did not find a template for %s. '
                             'Expected to find template named %s' \
                        %(model_name, template_expected_name))

        # clone the dom node and fetch the information of
        # where we are in the tree
        clone = template_node.cloneNode()

        # select dialog based on model name
        model_name = QString(model_name).toLower()
        dialog = None

        # all dialog have the same arguments, so we just specify them once
        dialog_args = (self.mainwindow, clone, self.model)

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
            raise NotImplementedError('dialog for template %s '
                                      'not yet implemented' %model_name)

        # show the dialog
        dialog.show()


    def makeEditableAction(self):
        self.model.makeEditable(self.currentElement())
        self.model.emit(SIGNAL("layoutChanged()"))


    def processCustomMenu(self, position):
        # grab the item and make sure its valid
        index = self.view.indexAt(position)
        if not index.isValid() or index.column() != 0:
            return

        item = self.view.indexAt(position) # get object at mouse coord
        if not item.isValid():
            return

        # make the item the current item in the model
        self.view.setCurrentIndex(index)

        domElement = item.internalPointer().node().toElement()
        if domElement.isNull():
            return # invalid item

        element_type = domElement.attribute('type').toLower()

        # create menu to populate
        menu = QMenu(self.mainwindow)

        # populate menu with model manager specific menu choices
        if element_type == 'model_system':
            submenu = QMenu(menu) # to populate with templates
            submenu.setTitle('Create model from template')
            for act in self.create_from_template_actions:
                submenu.addAction(act)
            menu.addMenu(submenu)

        if element_type == 'model':
            # If the users right clicks a model, give them the option to
            # estimate it only if the model has a (non empty) specification
            # subnode. If the model holds subgroups -- inform the user how to
            # estimate them.
            spec_node = self.xml.get('specification', domElement)
            submodels = None
            if spec_node:
                submodels = self.xml.children(spec_node)
            if spec_node and submodels:
                # check if its groups by type checking the first node
                # note: this is not a reliable method if models can have mixed
                # submodels and submodel groups.
                if submodels[0].attribute('type').toLower() == 'submodel':
                    menu.addAction(self.actRunEstimation)
                else:
                    menu.addAction(self.actHowToRunEstGroups)


        # TODO 4.2.1 change to node_type == submodel_group
        # for now, assume that a 'dictionary' located under 'specification' is
        # of type submodel group.
        if element_type == 'dictionary':
            parent_element = domElement.parentNode().toElement()
            if parent_element.tagName() == 'specification':
                menu.addAction(self.actRunEstimationGroup)

        menu.addSeparator()

        if domElement.hasAttribute(QString("inherited")):
            # inherited items have to be copied into this project before
            # we allow manipulating
            menu.addAction(self.actMakeEditable)
        else:
            if element_type in ['model', 'submodel']:
                menu.addAction(self.actRenameNode)

            if domElement.attribute("copyable").toLower() == "true" or \
            element_type in ['model', 'submodel']:
                menu.addAction(self.actCloneNode)

            if element_type == "variable_list":
                menu.addAction(self.actSelectVariables)

            # select which nodes that are removable
            if element_type in ['model', 'submodel', 'submodel_equation']:
                menu.addAction(self.actRemoveNode)

        # Check if the menu has any elements before exec is called
        if not menu.isEmpty():
            menu.exec_(QCursor.pos())

