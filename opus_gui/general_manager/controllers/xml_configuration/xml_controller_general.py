# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlController
from opus_gui.main.controllers.instance_handlers import get_mainwindow_instance

class XmlController_General(XmlController):
    def __init__(self, manager):
        XmlController.__init__(self, manager)