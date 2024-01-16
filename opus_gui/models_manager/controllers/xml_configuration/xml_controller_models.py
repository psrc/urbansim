# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from lxml import etree

from PyQt5.QtWidgets import QMenu
from PyQt5.QtGui import QCursor, QFont
from PyQt5.QtCore import pyqtSignal

from opus_core.logger import logger
from opus_gui.models_manager.run.run_estimation import OpusEstimation

from opus_gui.models_manager.controllers.submodel_editor import SubModelEditor
from opus_gui.models_manager.controllers.dialogs.dynamic_template_dialog import DynamicTemplateDialog

from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlController
from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlView
from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlItemDelegate

from opus_gui.models_manager.models.xml_model_models import XmlModel_Models
from opus_gui.scenarios_manager.scenario_manager import update_models_to_run_lists

class XmlController_Models(XmlController):

    def __init__(self, manager):
        ''' See XmlController for documentation '''
        XmlController.__init__(self, manager)

        # Create popup menu actions
        p = ('add', "Create model from template", self._show_dialog_for_template_node)
        self.action_create_model_from_template = self.create_action(*p)
        p = ('estimation', "Run Estimation", self.run_estimation_for_selected)
        self.action_run_estimation = self.create_action(*p)
        p = ('', "Right click the individual groups (specification/<group>) to estimate", lambda: ())
        self.action_show_how_to_estimate_groups = self.create_action(*p)
        p = ('estimation', "Run Estimation Group", self.run_estimation_for_selected_group)
        self.action_run_estimation_group = self.create_action(*p)
        p = ('submodel', "Edit Submodel", self._open_submodel_editor_for_selected)
        self.action_edit_submodel = self.create_action(*p)

        # Create a list of available template nodes
        self.create_from_template_actions = []
        template_nodes = self.project.findall('model_manager/templates/model_template')
        templates = dict((node.get('name'), node) for node in template_nodes)

        for template_name, template_node in list(templates.items()):
            callback = lambda x = template_node: self._show_dialog_for_template_node(x)
            action = self.create_action('clone', template_name, callback)
            self.create_from_template_actions.append(action)

        self.editor = None

    def add_model_view_delegate(self):
        ''' See XmlController for documentation '''
        # switch out the model for a custom one
        self.model = XmlModel_Models(self.xml_root, self.manager.project)
        self.view = XmlView(self.manager.base_widget)
        self.delegate = XmlItemDelegate(self.view)

    def run_estimation_for_selected(self):
        '''
        Create an Estimation Run Dialog for for running all the submodels.
        '''
        assert self.has_selected_item()
        model_name = self.selected_item().node.get('name')
        xml_config = self.manager.project.xml_config
        estimation_element = OpusEstimation(xml_config, model_name)
        self.manager.add_estimation_element(estimation_element)

    def run_estimation_for_selected_group(self):
        '''
        Create an estimation run dialog for this model for running a
        all submodels within a submodel group.
        '''
        assert self.has_selected_item()
        # Structure looks like: <model_item>/specfication/<group_item>
        # so model_index is parent of parent of the group index
        group_node = self.selected_item().node
        model_node = group_node.getparent().getparent()
        xml_config = self.manager.project.xml_config

        estimation_element = OpusEstimation(xml_config, model_node.get('name'), group_node.get('name'))
        self.manager.add_estimation_element(estimation_element)

    def _show_dialog_for_template_node(self, template_node):
        ''' generate a dialog for the selected template '''
        dialog = DynamicTemplateDialog(template_node, self.project, self.view)
        if dialog.exec_() == dialog.Accepted:
            models_node = self.project.find('model_manager/models')
            self.model.insert_node(dialog.model_node, models_node)

    def create_model_from_template_callback(self, new_model_node):
        # do the actual inserting of the opus model into the project
        self.model.insertRow(0, self.selected_index(), new_model_node)
        update_models_to_run_lists()

    def _open_submodel_editor_for_selected(self):
#        assert self.has_selected_item()
#        submodel_node = self.selected_item().node
#        submodel_parent = submodel_node.getparent()
#        if self.editor is None:
#            self.editor = SubModelEditorOld(self.project)
#        editor = self.editor
#        editor.init_for_submodel_node(submodel_node)
#        if editor.exec_() == editor.Accepted:
#            self._update_submodel(submodel_node, editor.submodel_node)

        assert self.has_selected_item()
        submodel_node = self.selected_item().node
        if self.editor is None:
            self.editor = SubModelEditor(self.project)
        editor = self.editor
        editor.init_for_submodel_node(submodel_node)
        if editor.exec_() == editor.Accepted:
            self._update_submodel(submodel_node, editor.submodel_node)

    def _update_submodel(self, current_node, edited_node):
        ''' Updating a submodel node (current_node) based on an edited version of it (edited_node)'''
        # the effect of renaming a shadowing node is that a new (local) copy is created and
        # the inherited node is reinserted. If the user did not rename the node we overwrite
        # the old submodel with the new values.
        name_change = current_node.get('name') != edited_node.get('name')
        if self.project.is_shadowing(current_node) and name_change:
            parent_node = current_node.getparent()
            row = parent_node.index(current_node)
            new_submodel_node = self.project.insert_node(edited_node, parent_node, row)
            if new_submodel_node is None:
                msg = ('Tried to insert a new submodel (%s) but failed. '
                       'The recent submodel changes have been lost.' %current_node.get('name'))
                logger.log_warning(msg)
            self.project.delete_node(current_node)
        else:
            for key in edited_node.attrib:
                current_node.attrib[key] = edited_node.attrib[key]
            for child in current_node:
                current_node.remove(child)
            for child in edited_node:
                current_node.append(child)
        self.project.dirty = True
        
    def add_custom_menu_items_for_node(self, node, menu):
        if node.tag == 'models':
            submenu = QMenu(menu) # to populate with templates
            submenu.setTitle('Create model from template')
            for action in self.create_from_template_actions:
                submenu.addAction(action)
            menu.addMenu(submenu)

        if node.tag == 'model':
            # If the users right clicks a model, give them the option to
            # estimate it only if the model has a (non empty) specification
            # subnode. If the model holds subgroups -- inform the user how to
            # estimate them.
            spec_node = node.find('specification')

            submodels = None
            if spec_node is not None:
                submodels = spec_node.getchildren()
            if spec_node is not None and submodels:
                # check if its groups by type checking the first node
                # note: this is not a reliable method if models can have mixed
                # submodels and submodel groups.
                if submodels[0].tag == 'submodel':
                    menu.addAction(self.action_run_estimation)
                else:
                    menu.addAction(self.action_show_how_to_estimate_groups)

        if node.tag == 'submodel' and not node.get('inherited'):
            menu.addAction(self.action_edit_submodel)

        if node.tag == 'submodel_group':
            menu.addAction(self.action_run_estimation_group)

        # In this menu, the first custom action is always the default action        
        if not menu.isEmpty():
            menu.setDefaultAction(menu.actions()[0])

