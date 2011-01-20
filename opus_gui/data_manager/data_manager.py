# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_gui.abstract_manager.abstract_manager import AbstractManager
from opus_gui.data_manager.controllers.xml_configuration.xml_controller_data_tools import XmlController_DataTools
from opus_gui.data_manager.controllers.files.file_controller_opus_data import FileController_OpusData

class DataManager(AbstractManager):
    ''' Handler for GUI elements belonging to the Generals tab '''

    def __init__(self, base_xml_widget, base_file_widget, tab_widget, project):
        AbstractManager.__init__(self, base_xml_widget, tab_widget, project, 'data_manager')
        self.xml_controller = XmlController_DataTools(self)
        self.file_tree = FileController_OpusData(self, self.project.data_path(), base_file_widget)

    def close(self):
        ''' See AbstractManager for documentation '''
        # Make sure to also close the FileController when closing data manager
        self.file_tree.close()
        AbstractManager.close(self)
