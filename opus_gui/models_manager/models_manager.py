# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_gui.models_manager.controllers.tabs.estimation_gui_element import EstimationGuiElement
from opus_gui.abstract_manager.abstract_manager import AbstractManager
from opus_gui.models_manager.controllers.xml_configuration.xml_controller_models import XmlController_Models

def get_model_nodes(project):
    '''
    Get a list of all model nodes in the project.

    @param project (OpusProject) the project to fetch values from
    @return the list of available model nodes (list(Element))
    '''
    return project.findall('model_manager/models/model')

def get_model_names(project):
    '''
    Get a list of model names in the project.

    @param project (OpusProject) the project to fetch values from
    @return the list of available model nodes (list(Element))
    '''
    return [node.get('name') for node in get_model_nodes(project)]

class ModelsManager(AbstractManager):
    def __init__(self, base_widget, tab_widget, project):
        AbstractManager.__init__(self, base_widget, tab_widget, project, 'model_manager')
        self.xml_controller = XmlController_Models(self)

    def add_estimation_element(self, estimation):
        tab_widget = EstimationGuiElement(self.base_widget, self, estimation)
        self._attach_tab(tab_widget = tab_widget)
