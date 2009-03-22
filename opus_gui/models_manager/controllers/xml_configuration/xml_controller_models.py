# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE
from opus_gui.main.controllers.instance_handlers import get_mainwindow_instance
from opus_gui.scenarios_manager.scenario_manager import update_models_to_run_lists

import copy

from PyQt4.QtGui import QMenu, QCursor

from opus_gui.models_manager.run.run_estimation import OpusEstimation

# TODO: remove this import when refactoring AllVariablesDialogs

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

    def __init__(self, manager):
        ''' See XmlController for documentation '''
        XmlController.__init__(self, manager)

        # Create popup menu actions
        i = self.model.cloneIcon
        t = "Create model from template"
        cb = self.createModelFromTemplate
        self.actCreateModelFromTemplate = self.createAction(i, t, cb)

        i = self.model.applicationIcon
        t = "Select Variables"
        cb = self.selectVariables
        self.actSelectVariables = self.createAction(i, t, cb)

        i = self.model.applicationIcon
        t = "Run Estimation"
        cb = self.runEstimationForSelected
        self.actRunEstimation = self.createAction(i, t, cb)

        i = self.model.applicationIcon
        t = "Right click the individual groups (specification/<group>) to estimate"
        cb = lambda: ()
        self.actHowToRunEstGroups = self.createAction(i, t, cb)

        i = self.model.applicationIcon
        t = "Run Estimation Group"
        cb = self.runEstimationGroupForSelected
        self.actRunEstimationGroup = self.createAction(i, t, cb)

        # Batch action creation for template dialogs
        self.acts_create_from_template = []
        template_names = ('Agent Location Choice Model', 'Allocation Model',
                  'Choice Model', 'Regression Model', 'Simple Model')

        for template_name in template_names:
            i = self.model.cloneIcon
            t = template_name
            cb = lambda x=template_name.lower():self.createModelFromTemplate(x)
            self.acts_create_from_template.append(self.createAction(i, t, cb))

    def setupModelViewDelegate(self):
        ''' See XmlController for documentation '''
        # switch out the model for a custom one
        self.model = XmlModel_Models(self.xml_root, self.manager.project)
        self.view = XmlView(self.manager.base_widget)
        self.delegate = XmlItemDelegate(self.view)

    def selectVariables(self):
        ''' Opens the variable selector GUI for the selected node '''
        assert self.hasSelectedItem()
        node = self.selectedItem().node
#            def __init__(self, opus_gui, nodeToUpdate=None, callback=None):
        window = AllVariablesSelectGui(get_mainwindow_instance(),
                                       node,
                                       None)
        window.show()

    def runEstimationForSelected(self):
        '''
        Create an Estimation Run Dialog for for running all the submodels.
        '''
        assert self.hasSelectedItem()
        model_name = self.selectedItem().node.tag
        xml_config = self.manager.project.xml_config
        newEstimation = OpusEstimation(xml_config, model_name)
        self.manager.addEstimationElement(newEstimation)

    def runEstimationGroupForSelected(self):
        '''
            Create an estimation run dialog for this model for running a
            all submodels within a submodel group.
        '''
        assert self.hasSelectedItem()
        # figure out the model name.
        # Expected place is <model_item>/specfication/<group_item>
        group_index = self.selectedIndex()
        model_index = self.model.parent(self.model.parent(group_index))
        xml_config = self.manager.project.xml_config

        group_node = group_index.internalPointer().node
        model_node = model_index.internalPointer().node

        newEstimation = OpusEstimation(xml_config,
                                       model_node.tag,
                                       group_node.tag)
        self.manager.addEstimationElement(newEstimation)

    def createModelFromTemplate(self, model_name):
        ''' select element to clone and present the correct dialog for it '''
        # the method selects which element node to clone by mapping the
        # model_name to a node element in the tree

        expected_template_name = model_name.replace(' ', '_') + '_template'

        # look for the template node under the model_system child node
        model_system = self.model.root_node().find('model_system')
        template_node = model_system.find(expected_template_name)

        if template_node is None:
            raise ValueError('Did not find a template for %s. '
                             'Expected to find template named %s' \
                        %(model_name, expected_template_name))

        clone = copy.deepcopy(template_node)

        # select dialog based on model name
        model_name = model_name.lower()
        dialog = None

        # all dialog have the same arguments, so we just specify them once
        dialog_args = (clone, self.manager.project,
                       self.create_model_from_template_callback,
                       self.view)

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

    def create_model_from_template_callback(self, new_model_node):
        self.model.insertRow(0, self.selectedIndex(), new_model_node)
        update_models_to_run_lists()

    def processCustomMenu(self, point):
        ''' See XmlConfig.processCustomMenu for documentation '''
        index = self.selectItemAt(point)
        if not index:
            return

        node = self.selectedItem().node
        menu = QMenu(self.view)

        if node.get('type') == 'model_system':
            submenu = QMenu(menu) # to populate with templates
            submenu.setTitle('Create model from template')
            for act in self.acts_create_from_template:
                submenu.addAction(act)
            menu.addMenu(submenu)

        if node.get('type') == 'model':
            # If the users right clicks a model, give them the option to
            # estimate it only if the model has a (non empty) specification
            # subnode. If the model holds subgroups -- inform the user how to
            # estimate them.
            spec_node = node.find('specification')

            submodels = None
            if spec_node:
                submodels = spec_node[:]
            if spec_node and submodels:
                # check if its groups by type checking the first node
                # note: this is not a reliable method if models can have mixed
                # submodels and submodel groups.
                if submodels[0].get('type') == 'submodel':
                    menu.addAction(self.actRunEstimation)
                else:
                    menu.addAction(self.actHowToRunEstGroups)


        # TODO 4.2.1 change to node_type == submodel_group
        # for now, assume that a 'dictionary' located under 'specification' is
        # of type submodel group.
        if node.get('type') == 'dictionary':
            parent_index = self.model.parent(self.selectedIndex())
            parent_node = parent_index.internalPointer().node
            if parent_node.tag == 'specification':
                menu.addAction(self.actRunEstimationGroup)

        if node.get('type') == "variable_list" and not node.get('inherited'):
            menu.addAction(self.actSelectVariables)

        self.addDefaultMenuItems(node, menu)

        if not menu.isEmpty():
            menu.exec_(QCursor.pos())
