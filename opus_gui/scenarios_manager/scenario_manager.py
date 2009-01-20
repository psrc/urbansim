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

from opus_gui.scenarios_manager.controllers.tabs.simulation_gui_element import SimulationGuiElement
from opus_gui.abstract_manager.abstract_manager import AbstractManager
from opus_gui.scenarios_manager.controllers.xml_configuration.xml_controller_scenarios import XmlController_Scenarios

from opus_gui.main.controllers.mainwindow import get_mainwindow_instance

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