# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from PyQt4.QtGui import QMenu, QCursor

from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlController
from opus_gui.main.controllers.instance_handlers import get_mainwindow_instance

class XmlController_General(XmlController):
    def __init__(self, manager):
        XmlController.__init__(self, manager)

    def editAllVariables(self):
        ''' Start the variable library GUI '''
        get_mainwindow_instance().editAllVariables()

    def processCustomMenu(self, point):
        ''' See XmlConfig.processCustomMenu for documentation '''
        item = self.selectItemAt(point)
        if not item: return

        node = item.node

        menu = QMenu(self.view)
        if node.get('type') in ('variable_definition', 'expression_library'):
            menu.addAction(get_mainwindow_instance().actVariableLibrary)

        self.addDefaultMenuItems(node, menu)

        if not menu.isEmpty():
            menu.exec_(QCursor.pos())

