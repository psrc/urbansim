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

from PyQt4.QtGui import QMenu, QCursor

from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlController
from opus_gui.main.controllers.mainwindow import get_mainwindow_instance

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

