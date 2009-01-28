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

from opus_gui.models_manager.controllers.tabs.estimation_gui_element import EstimationGuiElement
from opus_gui.abstract_manager.abstract_manager import AbstractManager
from opus_gui.models_manager.controllers.xml_configuration.xml_controller_models import XmlController_Models

def get_model_nodes(project):
    '''
    Get a list of all model nodes in the project.

    @param project (OpusProject) the project to fetch values from
    @return the list of available model nodes (list(Element))
    '''
    model_manager_node = project.find('model_manager/model_system')
    return [node for node in (model_manager_node or []) if
            node.get('type') == 'model']

def get_model_names(project):
    '''
    Get a list of model names in the project.

    @param project (OpusProject) the project to fetch values from
    @return the list of available model nodes (list(Element))
    '''
    model_nodes = get_model_nodes(project)
    return [node.tag for node in model_nodes]


class ModelsManager(AbstractManager):
    def __init__(self, base_widget, tab_widget, project):
        AbstractManager.__init__(self, base_widget, tab_widget, project,
                                 'model_manager')
        self.xml_controller = XmlController_Models(self)

    def addEstimationElement(self, estimation):
        tab_widget = EstimationGuiElement(self.base_widget, self, estimation)
        self._attach_tab(tab_widget = tab_widget)
