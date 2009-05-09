# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_gui.abstract_manager.abstract_manager import AbstractManager
from opus_gui.general_manager.controllers.xml_configuration.xml_controller_general import XmlController_General

class GeneralManager(AbstractManager):

    ''' Handler for GUI elements belonging to the Generals tab '''

    def __init__(self, base_widget, tab_widget, project):
        AbstractManager.__init__(self, base_widget, tab_widget, project, 'general')
        self.xml_controller = XmlController_General(self)
