# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from lxml import etree

from PyQt4.QtGui import QMenu, QCursor, QFont
from PyQt4.QtCore import SIGNAL

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
        p = ('estimation', "Run Estimation Group", self.run_estimation_group_for_selected)
        self.action_run_estimation_group = self.create_action(*p)
        p = ('submodel', "Edit Submodel", self._open_submodel_editor_for_selected)
        self.action_edit_submodel = self.create_action(*p)
        font = QFont()
        font.setBold(True)
        self.action_edit_submodel.setFont(font)

        # Create a list of available template nodes
        self.create_from_template_actions = []
        template_nodes = self.project.findall('model_manager/templates/model_template')
        templates = dict((node.get('name'), node) for node in template_nodes)

        for template_name, template_node in templates.items():
            callback = lambda x = template_node: self._show_dialog_for_template_node(x)
            action = self.create_action('clone', template_name, callback)
            self.create_from_template_actions.append(action)

        self.editor = None

        self.view.connect(self.view, SIGNAL('doubleClicked(const QModelIndex&)'), self._on_double_click)

    def add_model_view_delegate(self):
        ''' See XmlController for documentation '''
        # switch out the model for a custom one
        self.model = XmlModel_Models(self.xml_root, self.manager.project)
        self.view = XmlView(self.manager.base_widget)
        self.delegate = XmlItemDelegate(self.view)

    def _on_double_click(self, index):
        node = index.internalPointer().node
        if node is None:
            return
        if node.get('type') == 'submodel' and not node.get('inherited'):
            self._open_submodel_editor_for_selected()

    def run_estimation_for_selected(self):
        '''
        Create an Estimation Run Dialog for for running all the submodels.
        '''
        assert self.has_selected_item()
        model_name = self.selected_item().node.get('name')
        xml_config = self.manager.project.xml_config
        estimation_element = OpusEstimation(xml_config, model_name)
        self.manager.add_estimation_element(estimation_element)

    def run_estimation_group_for_selected(self):
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

        model_name = model_node.get('name')
        group_name = model_node.get('name')

        estimation_element = OpusEstimation(xml_config, model_name, group_name)
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
        assert self.has_selected_item()
        submodel_node = self.selected_item().node
        submodel_parent = submodel_node.getparent()
        if self.editor is None:
            self.editor = SubModelEditor(self.project)
        editor = self.editor
        editor.init_for_submodel_node(submodel_node)
        if editor.exec_() == editor.Accepted:
            # Delete the old and insert the new, edited, submodel node
            self.model.remove_node(submodel_node)
            self.model.insert_node(editor.submodel_node, submodel_parent)
            self.project.dirty = True

    def process_custom_menu(self, point):
        ''' See XmlConfig.processCustomMenu for documentation '''
        index = self.select_item_at(point)
        if not index:
            return

        node = self.selected_item().node
        menu = QMenu(self.view)

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

        self.add_default_menu_items_for_node(node, menu)

        if not menu.isEmpty():
            menu.exec_(QCursor.pos())
