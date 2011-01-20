# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_gui.models_manager.controllers.tabs.estimation_gui_element import EstimationGuiElement
from opus_gui.abstract_manager.abstract_manager import AbstractManager
from opus_gui.models_manager.controllers.xml_configuration.xml_controller_models import XmlController_Models

class ModelsManager(AbstractManager):
    def __init__(self, base_widget, tab_widget, project):
        AbstractManager.__init__(self, base_widget, tab_widget, project, 'model_manager')
        self.xml_controller = XmlController_Models(self)

    def add_estimation_element(self, estimation):
        tab_widget = EstimationGuiElement(self.base_widget, self, estimation)
        self._attach_tab(tab_widget = tab_widget)

