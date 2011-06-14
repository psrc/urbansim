# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import StringIO
from lxml import etree
from lxml.etree import Element

from PyQt4.QtGui import QMenu, QCursor

from opus_gui.scenarios_manager.run.run_simulation import OpusModel
from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlController
from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlView
from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlItemDelegate
from opus_gui.scenarios_manager.models.xml_model_scenarios import XmlModel_Scenarios
from opus_gui.models_manager.models_manager_functions import get_model_names
from opus_gui.scenarios_manager.scenario_manager import update_models_to_run_lists
from opus_gui.util.icon_library import IconLibrary
from opus_gui.util.convenience import get_unique_name


class XmlController_Scenarios(XmlController):

    def __init__(self, manager):
        ''' See XmlController.__init__ for documentation '''
        XmlController.__init__(self, manager)

        self.actAddModel = self.create_action('make_editable', 'Add Model', self.addModel)
        self.actRunScenario = self.create_action('accept', 'Run This Scenario', self.runScenario)
        self.actMoveNodeUp = self.create_action('arrow_up', "Move Up", self.moveNodeUp)
        self.actMoveNodeDown = self.create_action('arrow_down', "Move Down", self.moveNodeDown)
        self.actExecutable = self.create_action('executable', "Executable", self.toggleExecutable)
        self.actModelsToRun = self.create_action('add', "Add models_to_run node", self.addModelsToRun)
        self.actExecutable.setCheckable(True)

        # CK - what's this? Removing for now...
#        self.actOpenXMLFile = self.create_action(self.calendarIcon,"Open XML File", self.openXMLFile)
#        self.actEditXMLFileGlobal = self.create_action(self.calendarIcon,"Edit XML File Global", self.editXMLFileGlobal)
#        self.actEditXMLFileLocal = self.create_action(self.calendarIcon,"Edit XML File Local", self.editXMLFileLocal)

        # validate_models_to_run_lists()

    def add_model_view_delegate(self):
        ''' See XmlModel for documentation '''
        # Use the scenarios model
        self.model = XmlModel_Scenarios(self.xml_root, self.manager.project)
        self.view = XmlView(self.manager.base_widget)
        self.delegate = XmlItemDelegate(self.view)

    def runScenario(self):
        ''' Run the selected scenario. '''
        assert self.has_selected_item()
        scenario_node = self.selected_item().node

        newModel = OpusModel(self.manager, self.manager.project.xml_config,
                             scenario_node.get('name'))
        self.manager.addNewSimulationElement(newModel)

    def validate_models_to_run(self):
        ''' Mark up missing models in models to run lists '''
        self.model.validate_models_to_run()

    def moveNodeUp(self):
        ''' Move the selected node up one step '''
        assert self.has_selected_item()
        self.view.setCurrentIndex(self.model.move_up(self.selected_index()))

    def moveNodeDown(self):
        ''' Move the selected node down one step '''
        assert self.has_selected_item()
        self.view.setCurrentIndex(self.model.move_down(self.selected_index()))

    def toggleExecutable(self):
        ''' Toggle the "executable" attribute'''
        assert self.has_selected_item()
        item = self.selected_item()
        node = item.node
        node_executable = (node.get('executable') == 'True')

        if node_executable:
            node.set('executable', 'False')
        else:
            node.set('executable', 'True')
        self.model.dirty = True

    def process_custom_menu(self, point):
        ''' See XmlController for documentation '''
        item = self.select_item_at(point)
        if not item:
            return
        menu = QMenu()
        node = item.node

        if node.get('type') == 'scenario':
            node_executable = (node.get('executable') == 'True')
            menu.addAction(self.actExecutable)
            
            # Workaround: disabled items do not show check marks
            if node.get('inherited') is None:
                self.actExecutable.setEnabled(True)
                self.actExecutable.setText('Executable')
                self.actExecutable.setChecked(node_executable)
            else:
                self.actExecutable.setDisabled(True)
                self.actExecutable.setText('Executable: %s' % ('Yes' if node_executable else 'No'))
                
            if node_executable:
                menu.addAction(self.actRunScenario)
            if node.find('models_to_run') is None:  
                #if there isn't a child node models_to_run
                menu.addAction(self.actModelsToRun)                
        elif node.get('type') in ['selectable', 'model_choice']:
            menu.addAction(self.actMoveNodeUp)
            menu.addAction(self.actMoveNodeDown)
        elif node.tag == 'models_to_run': # special case of a selectable list
            models_menu = QMenu(menu)
            models_menu.setTitle('Add model to run')
            models_menu.setIcon(IconLibrary.icon('add'))
            available_model_names = get_model_names(self.project)
            for model_name in available_model_names:
                cb = lambda x = model_name, y = self.selected_index(): self.addModel(y, x)
                action = self.create_action('model', model_name, cb)
                models_menu.addAction(action)
            menu.addMenu(models_menu)

        self.add_default_menu_items_for_node(node, menu)

        if not menu.isEmpty():
            menu.exec_(QCursor.pos())
    
    def addModelsToRun(self):
        assert self.has_selected_item()
        item = self.selected_item()
        node = item.node
        self.model.add_node(node, etree.parse(StringIO.StringIO('<models_to_run config_name="models" type="selectable_list"/>')).getroot())
                        
    def addModel(self, models_to_run_list_index, model_name):
        '''
        Add a model to a models_to_run list.
        @param scenario_index (QModelIndex): index of the list to insert under
        @param models_name (String): name of model to add
        '''
        unique_name = get_unique_name(model_name, get_model_names(self.project))
        attribs = {'type': 'selectable', 'return_value': model_name, 'name': unique_name}
        model_node = Element('selectable', attribs)
        model_node.text = 'True'
        last_row_num = self.model.rowCount(models_to_run_list_index)
        self.model.insertRow(last_row_num, models_to_run_list_index, model_node)
        # Validate models to run
        update_models_to_run_lists()
