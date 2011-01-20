# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_gui.scenarios_manager.scenario_manager_functions import * #@UnusedWildImport

from opus_gui.scenarios_manager.controllers.tabs.simulation_gui_element import SimulationGuiElement
from opus_gui.abstract_manager.abstract_manager import AbstractManager
from opus_gui.scenarios_manager.controllers.xml_configuration.xml_controller_scenarios import XmlController_Scenarios

from opus_gui.main.controllers.instance_handlers import get_mainwindow_instance

class ScenariosManager(AbstractManager):
    def __init__(self, base_widget, tab_widget, project):
        AbstractManager.__init__(self, base_widget, tab_widget, project,
                                 'scenario_manager')
        self.xml_controller = XmlController_Scenarios(self)

    def addNewSimulationElement(self, model):
        ''' Initialize and add a simulation runner tab '''
        tab_widget = SimulationGuiElement(get_mainwindow_instance(),
                                          self, model, self.project.xml_config)
        self._attach_tab(tab_widget)

    def validate_models_to_run(self):
        if self.xml_controller is not None:
            self.xml_controller.validate_models_to_run()
